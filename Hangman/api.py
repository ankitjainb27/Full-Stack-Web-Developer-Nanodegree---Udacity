# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

import re
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm, \
    ScoreForms, GameForms
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1), )
GET_NUMBER_OF_RESULTS = endpoints.ResourceContainer(
    number_of_results=messages.IntegerField(1), )
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1), )
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
CREATE_USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                                  email=messages.StringField(2),
                                                  send_remainder=messages.BooleanField(3))

MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'


@endpoints.api(name='hangman', version='v1')
class GuessANumberApi(remote.Service):
    """Game API"""

    @endpoints.method(request_message=CREATE_USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email, remainder=request.send_remainder)
        user.put()
        return StringMessage(message='User {} created!'.format(
            request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        game = Game.new_game(user.key, request.attempts)

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Hangman!, It is a three letter word')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/game_history/{urlsafe_game_key}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Return the game history of a particular game."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            win_loss = []
            i = 0
            length = len(game.game_history)
            # To make a list of win, loss or in progress
            for state in game.game_history:
                if state == game.target:
                    win_loss.append("Game Over - Won")
                else:
                    if i == (length - 1):
                        win_loss.append("Game Over - Lost")
                    else:
                        win_loss.append("In Progress")
                i += 1
            # Combine alphabets that user guesses, the game history at every step and the win_loss state at that move
            history = zip(game.alphabets_history, game.game_history, win_loss)
            # If want to convert to a List of List
            # x = []
            # for items in history:
            #     x.append(list(items))
            # print str(x)
            return StringMessage(message=str(history))
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form_with_history('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='gamecancel/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='PUT')
    def cancel_game(self, request):
        """Cancel a particular game"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            if game.game_over:
                return game.to_form_with_history('Game Not in Progress')
            else:
                game.game_cancel = True
                game.game_over = True
                game.put()
                return game.to_form_with_history('Game Cancelled')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        # Restrict from making move is game is over
        if game.game_over:
            return game.to_form_with_history('Game already over!')
        # Restrict from making move is game is cancelled
        if game.game_cancel:
            return game.to_form_with_history('Game Cancelled!')
        request.guess = request.guess.lower()
        # Restrict from making move if user entered more than one character
        if len(request.guess) != 1 and request.guess != " ":
            return game.to_form_with_history('Enter only single charater')
        if not re.search('[a-zA-Z]', request.guess):
            # Restrict from making move if user didn't enter alphabet
            return game.to_form_with_history('Enter only alphabets')
        # Restrict from making move if user re-enters an alphabet
        if len(game.alphabets_history) > 0 and request.guess in game.alphabets_history:
            return game.to_form_with_history('Character already done')

        game.alphabets_history.append(request.guess)

        guess_correct = False
        current_state = ""
        # Depending on the input the history is made and added in the db
        if len(game.game_history) == 0:
            for character in game.target:
                if character == request.guess:
                    current_state += request.guess
                    guess_correct = True
                else:
                    current_state += "_"
        else:
            current_state = str(game.game_history[-1])
            for x in xrange(len(current_state)):
                if game.target[x] == request.guess:
                    guess_correct = True
                    s = list(current_state)
                    s[x] = request.guess
                    current_state = "".join(s)
        if not guess_correct:
            game.attempts_remaining -= 1
        game.game_history.append(current_state)
        if current_state == game.target:
            game.end_game(True)
            return game.to_form_with_history('You win!')

        if game.attempts_remaining < 1:
            game.end_game(False)
            return game.to_form_with_history(' Game over!')
        else:
            game.put()
            return game.to_form_with_history(
                "Make Next Move, " + str(game.attempts_remaining) + " remaining")

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=GET_NUMBER_OF_RESULTS,
                      response_message=ScoreForms,
                      path='scores_high',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Return high scores"""
        # High score includes entries that won and in descending order of no. of guesses made
        scores = Score.query(Score.won == True).order(Score.guesses).fetch(request.number_of_results)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='scores_user_ranking',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Return the ranking of all users"""
        ranking = {}
        # User ranking is based on weighted score
        # To calculate it the formula
        # First we get a state, which is 1 for win and 0 for loss
        # Final formula is = sum(state*guess)/(sum(guess))
        for score in Score.query():
            state = {}
            if not ranking.get(str(score.user.get().name)):
                state['guesses'] = score.guesses
                if (score.won):
                    state['perf'] = 1.0
                else:
                    state['perf'] = 0.0
            else:
                current_state = ranking.get(score.user.get().name)
                state['guesses'] = score.guesses + current_state['guesses']
                if (score.won):
                    if not state['guesses'] == 0:
                        state['perf'] = (score.guesses + current_state['guesses'] * current_state['perf']) / (
                            state['guesses'] * 1.0)
                    else:
                        state['perf'] = 1.0
                else:
                    state['perf'] = (current_state['guesses'] * current_state['perf']) / (state['guesses'] * 1.0)
            ranking[score.user.get().name] = state
        ranking_list = []
        for key, value in ranking.iteritems():
            a = (str(key), value.get('perf'))
            ranking_list.append(a)
        ranking_list = sorted(ranking_list, key=lambda tup: tup[1], reverse=True)
        return StringMessage(message=str(ranking_list))

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='games/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of an individual User's games"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        formatted_query = ndb.query.FilterNode('game_over', '=', False)
        scores = Game.query(Game.user == user.key).filter(formatted_query)
        return GameForms(items=[score.to_form("") for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                            for game in games])
            average = float(total_attempts_remaining) / count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([GuessANumberApi])
