# Project: Item Catalog
Part of Full Stack Nanodegree on Udacity.com

Link to Nanodegree - https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

Go to - http://localhost:5000/ to see all restaurants and their menu items

# JSON Endpoints
1. All Menus of a restaurant - http://localhost:5000/restaurant/<int:restaurant_id>/menu/JSON/, For example - http://localhost:5000/restaurant/1/menu/JSON/

2. Single Menu of a restaurant - http://localhost:5000/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/, For example - http://localhost:5000/restaurant/1/menu/1/JSON/

# Installation Steps
Step1 - Install pip Make a virtualenv for this project pip install virtualenv virtualenv myproject source myproject/bin/activate

Step2 - Install the required dependencies: pip install -r requirements.txt

Step3 - Installation steps for mongodb - https://docs.mongodb.com/manual/installation/

Turn on mongodb by running mongod command in terminal

Step4 - Run the tournament test:
python manage.py runserver

Then go to http://localhost:5000/ to see all restaurants and their menu items
