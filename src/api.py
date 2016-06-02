from flask import Blueprint, request, redirect, render_template, jsonify, session, make_response, flash
from flask.views import MethodView
from src.models import Restaurant, MenuItem, User
from src import app
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import os

CLIENT_ID = json.loads(
    open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'client_secrets.json'), 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"

restaurants = Blueprint('restaurants', __name__, template_folder='templates')
menu = Blueprint('menu', __name__, template_folder='templates')


class RestaurantView(MethodView):
    def get(self, restaurant_id):
        print 'came'
        if restaurant_id is None:
            restaurant = Restaurant.objects.all()
            if 'username' not in session:
                return render_template('public_list.html', restaurant=restaurant)
            else:
                print session['username']
                return render_template('list.html', restaurant=restaurant, user=getUserInfo(session['user_id']),
                                       session=session)
        else:
            if 'username' not in session:
                return redirect('/login/')
            print restaurant_id
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            return render_template('form.html', restaurant=restaurant)

    def post(self, restaurant_id):
        if restaurant_id is None:
            if 'username' not in session:
                return redirect('/login/')
            restaurant_name = request.form['newRestaurantName']
            if restaurant_name:
                res = Restaurant(name=request.form['newRestaurantName'], restaurant_user_id=session['user_id'])
                res.save()
                return redirect('/restaurant/')
            return render_template('form.html')
        else:
            print restaurant_id
            restaurant_name = request.form['newRestaurantName']
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            restaurant.update(name=restaurant_name)
            return redirect('/restaurant/')


class MenuView(MethodView):
    def get(self, restaurant_id, menu_id):
        if menu_id is None:
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            # flash("Menu Items")
            if 'username' not in session:
                return render_template('public_list_menu.html', restaurant=restaurant)
            else:
                return render_template('list_menu.html', restaurant=restaurant, user=getUserInfo(session['user_id']))
        else:
            if 'username' not in session:
                return redirect('/login/')
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            menuitem = restaurant[0].menuitems.filter(menu_id=menu_id)
            return render_template('menu_form.html', restaurant=restaurant, menuitem=menuitem)

    def post(self, restaurant_id, menu_id=None):
        if menu_id is None:
            if 'username' not in session:
                return redirect('/login/')
            menu_name = request.form['newMenuName']
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            print menu_name
            if menu_name:
                res = MenuItem(name=request.form['newMenuName'], menu_user_id=session['user_id'])
                restaurant.menuitems.append(res)
                restaurant.save()
                return redirect('/menu/' + str(restaurant_id) + '/')
            return render_template('menu_form.html', restaurant=restaurant)
        else:
            print restaurant_id
            print menu_id

            menu_name = request.form['newMenuName']
            print menu_name
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            res3 = (restaurant.menuitems.filter(menu_id=menu_id))
            res3.update(name=menu_name)
            res3.save()
            return redirect('/menu/' + str(restaurant_id) + '/')


user_view = RestaurantView.as_view('list')
restaurants.add_url_rule('/restaurant/', defaults={'restaurant_id': None},
                         view_func=user_view, methods=['GET', ])
restaurants.add_url_rule('/restaurant/', defaults={'restaurant_id': None}, view_func=user_view, methods=['POST'])
restaurants.add_url_rule('/restaurant/<int:restaurant_id>/', view_func=user_view,
                         methods=['GET', 'POST', ])

# res = Restaurant.objects.filter(restaurant_id = 23).update(set__menuitems__0 = menuItem2)
menu_view = MenuView.as_view('list1')
menu.add_url_rule('/menu/<int:restaurant_id>/', defaults={'menu_id': None},
                  view_func=menu_view, methods=['GET', ])
menu.add_url_rule('/menu/<int:restaurant_id>/', view_func=menu_view, methods=['POST'])
menu.add_url_rule('/menu/<int:restaurant_id>/<int:menu_id>/', view_func=menu_view,
                  methods=['GET', 'POST', 'DELETE'])


@app.route('/restaurant/new/')
def asd():
    if 'username' not in session:
        return redirect('/login/')
    return render_template('form.html')


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete(restaurant_id):
    if 'username' not in session:
        return redirect('/login/')
    if request.method == 'GET':
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
        return render_template('delete.html', restaurant=restaurant)
    else:
        res = Restaurant.objects.filter(restaurant_id=restaurant_id).delete()
        # if res:
        #     flash("Successfully Deleted")
        # else:
        #     flash("Not Deleted")
        return redirect('/restaurant/')


@app.route('/menu/<int:restaurant_id>/new/')
def asd1(restaurant_id):
    if 'username' not in session:
        return redirect('/login/')
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
    return render_template('menu_form.html', restaurant=restaurant)


@app.route('/menu/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deletemenu(restaurant_id, menu_id):
    if 'username' not in session:
        return redirect('/login/')
    if request.method == 'GET':
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
        menuitem = restaurant[0].menuitems.filter(menu_id=menu_id)
        return render_template('menu_delete.html', restaurant=restaurant, menu=menuitem)
    else:
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        res3 = (restaurant.menuitems.filter(menu_id=menu_id))
        res3.delete()
        res3.save()
        # if res3:
        #     flash("Successfully Deleted Menu Item")
        # else:
        #     flash("Not Deleted")
        return redirect('/menu/' + str(restaurant_id) + '/')


@app.route('/')
def start():
    return redirect('/restaurant/')


@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def menujson(restaurant_id):
    res = Restaurant.objects.get(restaurant_id=restaurant_id)
    res1 = res.menuitems
    return jsonify(MenuItem=[i.serialize for i in res1])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menujson1(restaurant_id, menu_id):
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
    menuitem = restaurant[0].menuitems.filter(menu_id=menu_id)
    return jsonify(MenuItem=[menuitem[0].serialize])


@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state
    print state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'client_secrets.json'), scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    session['provider'] = 'google'
    if getUserId(session['email']):
        session['user_id'] = getUserId(session['email'])
    else:
        session['user_id'] = create_user(session)

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their session


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fb_client_secrets.json'), 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'fb_client_secrets.json'), 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    # The token must be stored in the session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserId(session['email'])
    if not user_id:
        user_id = create_user(session)
    session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += session['username']

    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in session:
        if session['provider'] == 'google':
            gdisconnect()
        if session['provider'] == 'facebook':
            fbdisconnect()
            del session['facebook_id']
            del session['email']
            del session['picture']
            del session['user_id']
            del session['username']
        del session['provider']
        flash("You have successfully been logged out.")
        return redirect('/')
    else:
        flash("You were not logged in")
        return redirect('/')


def create_user(session):
    User1 = User(name=session['username'], email=session['email'],
                 picture=session['picture'])
    User1.save()

    return getUserId(session['email'])


def getUserInfo(user_id):
    user = User.objects.get(user_id=user_id)
    return user


def getUserId(email):
    try:
        user = User.objects.get(email=email)
        user.save()
        return user.user_id
    except:
        return None
