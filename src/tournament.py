from src import db
from src.models import Player, Match
from operator import itemgetter


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    if db:
        return True
    else:
        return False


def deleteMatches():
    Match.objects.delete()
    """Remove all the match records from the database."""


def deletePlayers():
    Player.objects.delete()
    """Remove all the player records from the database."""


def countPlayers():
    """Returns the number of players currently registered."""
    return Player.objects.count()


def registerPlayer(name):
    if name:
        player = Player(name=name)
        player.save()

    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    player = Player.objects.all()
    playerList = list()
    pipeline = [
        {'$group':
             {'_id': {'winner': '$winner'},
              'number': {'$sum': 1}
              }
         }]
    match = Match.objects.aggregate(*pipeline)
    list1 = list(match)

    pipeline = [
        {'$group':
             {'_id': {'loser': '$loser'},
              'number': {'$sum': 1}
              }
         }]
    match = Match.objects.aggregate(*pipeline)
    list2 = list(match)

    for item in player:
        winner = 0
        matches = 0
        for match in list1:
            if (match['_id']['winner'] == str(item.id)):
                winner = match['number']
                matches = match['number']
                break;

        for match in list2:
            if (match['_id']['loser'] == str(item.id)):
                matches = matches + match['number']
                break;

        playerList.append((
            str(item.id), item.name, winner, matches)
        )

        playerList = sorted(playerList, key=itemgetter(2), reverse=True)

        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place, or a player
        tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
    return playerList


def reportMatch(winner, loser):
    match = Match(winner=winner, loser=loser)
    match.save()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    players = playerStandings()
    playerList = list()
    for item in xrange(0, len(players), 2):
        tup = tuple((str(players[item][0]), players[item][1], str(players[item + 1][0]), players[item + 1][1]))
        playerList.append(tup)

    return playerList
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
