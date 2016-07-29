##Project: Game API
Part of Full Stack Nanodegree on Udacity.com
Link to Nanodegree - https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

View the details [here](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454012/modules/356635917875461/lessons/3566359178239847/concepts/72231259940923).
Link to the app's api explorer is [here](https://apis-explorer.appspot.com/apis-explorer/?base=https://hangman-1469790942131.appspot.com/_ah/api#p/).

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.


##Game Description:
Hangman is a game where the player needs to guess the letter of a word.
He can uses the number of dashes to know the no. of letter in the word and already guessed word to correctly guess the whole word.
Each game begins with a random 'target' word.
'Guesses' are sent to the `make_move` endpoint which will reply
with either: list of 'alphabets_history' and list of 'game_history', attempts_remaining.
Many different Hangman games can be played by many different Users at any
given time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

##Score Keeping
Score is kept when the game is over. It is stored if the user, won or lost the game and the no. of guesses he made in the game.
High score includes entries that won and in descending order based on number of incorrect guesses user took to solve the hangman.
 - User ranking is based on sum of number of incorrect guesses

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will
    raise a ConflictException if a User with that user_name already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. User can also choose the attempts he wants,
    if not provided by default it is taken as 5.
    Also adds a task to a task queue to update the average moves remaining
    for active games.

 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

 - **get_game_history**
    - Path: 'game/game_history/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: The history of the game containing steps-by-steps alphabet guesses,
    the state of the word and the state of the game (Won, Lost or Turns Remaining)
    - Description: Return the game history of a particular game.

 - **cancel_game**
    - Path: 'gamecancel/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key
    - Returns: GameForm with cancelled game state.
    - Description: """Cancel a particular game"""


 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.

 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).

 - **get_high_scores**
    - Path: 'scores_high'
    - Method: GET
    - Parameters: number_of_results
    - Returns: ScoreForms.
    - Description: Return high scores.
    High score includes entries that won and in descending order of no. of incorrect guesses made

 - **get_user_rankings**
    - Path: 'scores_user_ranking'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Return a List of tuples of user_name and performance in descending order.
    High score includes entries that won and in descending order based on number of incorrect guesses user took to solve the hangman.
    - User ranking is based on sum of number of incorrect guesses


 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms.
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_user_games**
    - Path: 'games/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms.
    - Description: Returns all of an individual User's games.
    Will raise a NotFoundException if the User does not exist.

 - **get_active_game_count**
    - Path: 'games/active'
    - Method: GET
    - Parameters: None
    - Returns: StringMessage
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.

##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.

 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.

##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name, game_history, alphabets_history, game_cancel).
 - **NewGameForm**
    - Used to create a new game (user_name, attempts)
 - **MakeMoveForm**
    - Inbound make move form (guess).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
