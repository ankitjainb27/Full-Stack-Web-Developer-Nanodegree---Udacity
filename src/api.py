from flask import Blueprint, request, redirect, render_template, url_for, flash, jsonify
from flask.views import MethodView
from src.models import Restaurant, MenuItem
from src import app

restaurants = Blueprint('restaurants', __name__, template_folder='templates')
menu = Blueprint('menu', __name__, template_folder='templates')


class RestaurantView(MethodView):
    def get(self, restaurant_id):
        if restaurant_id is None:
            restaurant = Restaurant.objects.all()
            # flash("See all messages")
            return render_template('list.html', restaurant=restaurant)
        else:
            print restaurant_id
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            return render_template('form.html', restaurant=restaurant)

    def post(self, restaurant_id):
        if restaurant_id is None:
            restaurant_name = request.form['newRestaurantName']
            if restaurant_name:
                res = Restaurant(name=request.form['newRestaurantName'])
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
            return render_template('list_menu.html', restaurant=restaurant)
        else:
            restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
            menuitem = restaurant[0].menuitems.filter(menu_id=menu_id)
            return render_template('menu_form.html', restaurant=restaurant, menuitem=menuitem)

    def post(self, restaurant_id, menu_id=None):
        if menu_id is None:
            menu_name = request.form['newMenuName']
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            print menu_name
            if menu_name:
                res = MenuItem(name=request.form['newMenuName'])
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
    return render_template('form.html')


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete(restaurant_id):
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
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
    return render_template('menu_form.html', restaurant=restaurant)


@app.route('/menu/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deletemenu(restaurant_id, menu_id):
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
