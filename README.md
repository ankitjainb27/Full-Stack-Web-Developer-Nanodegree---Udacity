# udacity_full_stack_developer

Assigment - https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true

# Installation Steps

1. Step1 -
Install pip
Make a virtualenv for this project
pip install virtualenv
virtualenv myproject
source myproject/bin/activate

2. Step2 -
Install the required dependencies: pip install -r requirements.txt

3. Step3 -
Installation steps for mongodb - https://docs.mongodb.com/manual/installation/

Turn on mongodb by running mongod command in terminal

4. Step4 -
Run the tournament test:

python manage.py runserver

It will run the tournament_test.py and print

1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.

Success!  All tests pass!

# Using Pycharm

Then set in Run configurations as given in this image -
https://drive.google.com/file/d/0B45KQAZloIqYMzVBM0VFWDJHQTA/view?usp=sharing
