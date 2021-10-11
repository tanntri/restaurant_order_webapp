from app import app, models, db
from flask import render_template, request, redirect, url_for

TAX_RATE = 0.0685


def show_menu():
    ''' funciton to get the list of menu items separated by category. Returns list of list '''
    menus = models.Menu.query.all()  # query all menu items
    appetizers = [menu for menu in menus if menu.category == 'Appetizer'
                  ]  # list of menu items with category of Appetizer
    soups = [menu for menu in menus if menu.category == 'Soup'
             ]  # list of menu items with category of Soup
    pizzas = [menu for menu in menus if menu.category == 'Pizza'
              ]  # list of menu items with category of Pizza
    pastas = [menu for menu in menus if menu.category == 'Pasta'
              ]  # list of menu items with category of Pasta
    rices = [menu for menu in menus if menu.category == 'Rice'
             ]  # list of menu items with category of Rice
    coffees = [menu for menu in menus if menu.category == 'Coffee'
               ]  # list of menu items with category of Coffee
    wines = [menu for menu in menus if menu.category == 'Wine'
             ]  # list of menu items with category of Wine
    desserts = [menu for menu in menus if menu.category == 'Dessert'
                ]  # list of menu items with category of Dessert
    beverages = [menu for menu in menus if menu.category == 'Beverage'
                 ]  # list of menu items with category of Beverage
    menus_lst = [
        appetizers,
        soups,
        pizzas,
        pastas,
        rices,
        desserts,
        coffees,
        wines,  # list of list of menu items separated by categories
        beverages
    ]

    return menus_lst  # return list of list


# page to show menu without ordering function
@app.route('/')
def home():
    return render_template('public/home_menu.html', menus_lst=show_menu())


# page to show menu with ordering function
@app.route('/order/<int:table>')
def order(table):
    return render_template('public/menus.html',
                           menus_lst=show_menu(),
                           table=table)


# page to show the shopping cart, let the user see their orders before confirming
@app.route('/cart', methods=["GET", "POST"])
def cart():
    menus = models.Menu.query.all()  # query all the menu
    if request.method == 'POST':  # if it is a POST request
        order_list = []
        for menu in menus:  # loop through all the menu items
            if int(
                    request.form[menu.name]
            ) > 0:  # if amount user input is > 1 (means customer ordered the dish)
                new_order = {                       # make a dictionary of order info
                    'food_id': menu.id,
                    'name': menu.name,
                    'table': request.form['table'],
                    'amount': int(request.form[menu.name]),
                    'price': menu.price,
                }
                order_list.append(
                    new_order)  # append the dictionary to list of food ordered
        subtotal = 0
        for order in order_list:  # loop through list of order
            subtotal += order['amount'] * order['price']  # calculate subtotal
        total = subtotal + subtotal * TAX_RATE  # calculate total
        return render_template(
            'public/cart.html',  # render page
            table=request.form['table'],
            order_list=order_list,
            subtotal='{:.2f}'.format(round(subtotal, 2)),
            total='{:.2f}'.format(round(total, 2)))
    return render_template('public/cart.html')


# function for when customer confirm the orders
@app.route('/confirm', methods=["POST"])
def confirm():
    menus = models.Menu.query.all()  # query through all the menu items
    for menu in menus:  # loop through all menu items
        if request.form.get(menu.name,
                            False):  # if name of menu exists in order list
            new_order = models.OrdersOngoing(
                food_id=menu.id,
                name=menu.name,
                table=request.form.get(f'{menu.name} table', False),
                amount=request.form.get(f'{menu.name} amount', False),
                price=menu.price)
            db.session.add(
                new_order)  # add the menu to current_orders database
            table = request.form.get(f'{menu.name} table', False)
    db.session.commit()  # commit change in database
    return redirect(url_for('order', table=table))
