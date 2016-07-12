# Project: Item Catalog
Part of Full Stack Nanodegree on Udacity.com

Link to Nanodegree - https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

Go to - http://localhost:5000/ to see all restaurants and their menu items

# JSON Endpoints
1. All Menus of a restaurant - http://localhost:5000/restaurant/<int:restaurant_id>/menu/JSON/, For example - http://localhost:5000/restaurant/1/menu/JSON/

2. Single Menu of a restaurant - http://localhost:5000/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/, For example - http://localhost:5000/restaurant/1/menu/1/JSON/

# Installation Steps
1. Step1 - Install pip 
2. Steps2 - Install Virtual Environment - pip install virtualenv 
3. Steps3 - Make a virtualenv for this project - virtualenv myproject
4. Steps4 - start using the virtual environment - source myproject/bin/activate
5. Steps5 - Install the required dependencies: pip install -r requirements.txt
6. Steps6 - Installation steps for mongodb - https://docs.mongodb.com/manual/installation/
7. Steps7 - Turn on mongodb by running mongod command in terminal
8. Steps8 - Run the server by first going in src folder and then using the command - python manage.py runserver
9. Steps9 - Then go to http://localhost:5000/ to see all restaurants and their menu items
