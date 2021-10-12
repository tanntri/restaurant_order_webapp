from app import app, db, forms, models
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy import func
from datetime import datetime, date

# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)

# tax rate to calculate total price from subtotal
TAX_RATE = 0.0685


def get_datetime():
    ''' Function to get current date and time '''
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    date_time = {
        'date': date,
        'time': time,
    }
    return date_time


def get_orders_of_day(string_date):
    ''' Function to get the list of orders of chosen date '''

    # query the database for orders with matching date with chosen date
    the_day_orders = models.Transactions.query.filter_by(
        date=string_date).all()
    order_ids_of_this_date = []
    all_orders_this_date = []

    # loop through the orders in the chosen date to get unique order id
    for order in the_day_orders:
        if order.orders_id not in order_ids_of_this_date:  # if order id is not in order id list, append it
            order_ids_of_this_date.append(
                order.orders_id)  # this is to get only unique order id

    # loop through list of unique order id
    for id in order_ids_of_this_date:
        orders_by_id = []
        for order in the_day_orders:  # loop through orders in the chosen date
            if order.orders_id == id:  # if order id matches, make dictionary of order detail and append to list
                food_info = {  # this allows to make list consists of same order id
                    'table': order.table,
                    'date': order.date,
                    'time': order.time,
                    'orders_id': order.orders_id,
                    'name': order.name,
                    'price': order.price,
                    'amount': order.amount,
                    'subtotal': order.subtotal,
                    'total': order.total
                }
                orders_by_id.append(food_info)
        all_orders_this_date.append(orders_by_id)
    return all_orders_this_date  # return order list to be displayed


# user loader is required to login users
@login_manager.user_loader
def load_user(user_id):
    return models.Staff.query.get(user_id)


# route to show the orders ongoing that haven't been paid yet
@app.route('/admin')
@login_required
def current_orders():
    all_order_list = models.OrdersOngoing.query.all(
    )  # get list of ongoing orders
    tables_occupied = db.session.query(  # get list of table currently occupied
        models.OrdersOngoing.table.distinct()).all()
    occupied_table_list = []

    for table in tables_occupied:  # append to table list
        occupied_table_list.append(table[0])

    tables_orders_list = []  # list of orders separated by table
    for table in occupied_table_list:  # loop through list of occupied table number
        table_orders = []
        for orders in all_order_list:  # loop through all orders
            if orders.table == table:  # if table number of the order is equal to table number
                order_info = {  # append the dict of order info to the list
                    'food_id': orders.food_id,
                    'name': orders.name,
                    'table': orders.table,
                    'amount': orders.amount,
                    'price': orders.price
                }
                table_orders.append(order_info)
        tables_orders_list.append(
            table_orders)  # append list of order infos to orders of tables

    return render_template(
        'admin/current_orders.html',  # render page
        tables_orders_list=tables_orders_list,
        tax_rate=TAX_RATE)


######## register path. commented out because we don't need more admins #########


# @app.route('/register', methods=["GET", "POST"])
# def register():
#     form = forms.RegisterForm()  # assign RegisterForm to form
#     if form.validate_on_submit():  # if method == 'POST'
#         if models.Staff.query.filter_by(email=form.email.data).first(
#         ):  # query User table and see if email inputted in the form already existed
#             # User already exists
#             flash("You've already signed up with that email, log in instead!")
#             #       )  # shows flash message
#             print('user exists')
#             return redirect(url_for('login'))  # redirect user to login page

#         hashed_and_salted_pwd = generate_password_hash(  # encrypt password using hash and salt
#             form.password.data,  # use password inputted in the form
#             method='pbkdf2:sha256',  # use sha256 method to encrypt password
#             salt_length=5  # how many times salting the password
#         )
#         new_staff = models.Staff(  # create new user
#             email=form.email.data,  # use email inputted in the form
#             password=hashed_and_salted_pwd  # use encrypted password
#         )
#         db.session.add(new_staff)  # add new user to the database
#         db.session.commit()  # commit change in database
#         login_user(new_staff)  # login user
#         return redirect(
#             url_for('admin_menus', is_loggedin=current_user.is_authenticated)
#         )  # redirect to home page
#     return render_template("admin/register.html",
#                            is_loggedin=current_user.is_authenticated,
#                            form=form)  # if method is GET, then render the page


# login functionality
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  # if currently logged in and try to access this page, redirect to current order page
        return redirect(url_for('current_orders'))
    form = forms.LoginForm()  # assign LoginForm to form for rendering
    if form.validate_on_submit():  # if method == 'POST'
        email = form.email.data  # assign value from email field of the form to variable email
        password = form.password.data  # assign value from password field of the form to variable password

        staff = models.Staff.query.filter_by(email=email).first(
        )  # query using email to see if staff exists in the database

        if not staff:  # if user doesn't exist
            flash("This email doesn't exist. Please try again"
                  )  # show flash message
            return redirect(url_for('login'))  # redirect back to login page
        elif not check_password_hash(
                staff.password, password
        ):  # check if hashed value of password inputted match the one in the database
            flash("Wrong password. Please try again"
                  )  # if not, show the flash message
            return redirect(url_for(
                'login'))  # redirect to login page to let user try again
        else:  # else. in this case means user enters correct email and password
            login_user(staff)  # login user
            return redirect(
                url_for('current_orders',
                        is_loggedin=current_user.is_authenticated)
            )  # redirect to home page
    return render_template(
        "admin/login.html",
        form=form)  # if method is GET, then just render login page


# function to log out the current user
@app.route('/logout')
def logout():
    logout_user()  # logout user
    return redirect(url_for('home'))  # redirect to homepage


# function to show menu of admin page, which allows admin to edit or delete menu items
@app.route('/admin/menu')
@login_required
def admin_menus():
    menus = models.Menu.query.all()
    return render_template('admin/admin_menus.html', menus=menus)


# function to add menu item
@app.route('/admin/add_item', methods=["GET", "POST"])
@login_required
def add_items():
    form = forms.AddItemForm(
    )  # assign AddItemForm to variable form to be passed to render page
    if form.validate_on_submit():  # if request.method == 'POST'
        new_item = models.Menu(
            name=form.name.
            data,  # get data from fields in the form, assign to variables
            category=form.category.data,
            description=form.description.data,
            price=form.price.data)
        db.session.add(new_item)  # add to database
        db.session.commit()  # commit database change
        return redirect(url_for('admin_menus'))  # redirect to menu page
    return render_template('admin/add_menu.html', form=form)  # render page


# function to change information of particular menu item
@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(
    item_id
):  # pass item id as a parameter to let the program know which item to be edited
    item = models.Menu.query.get(item_id)  # get item with matching item id
    edit_form = forms.EditItemForm(
        name=item.
        name,  # get the edit form and prefill them with data in the database
        category=item.category,
        description=item.description,
        price=item.price)
    if edit_form.validate_on_submit():  # if request.method == "POST"
        item.name = edit_form.name.data  # assign data from fields to data fields in the database
        item.category = edit_form.category.data
        item.description = edit_form.description.data
        item.price = edit_form.price.data
        db.session.commit()  # commit change in database
        return redirect(url_for('admin_menus'))  # redirect to menu page
    return render_template('admin/edit_menu.html', form=edit_form,
                           item=item)  # render page


# function to delete menu item from database
@app.route('/admin/delete_item/<int:item_id>')
@login_required
def delete_item(item_id):
    item = models.Menu.query.get(
        item_id)  # get menu item with matching item id
    db.session.delete(item)  # delete from database
    db.session.commit()  # commit change in the database
    return redirect(url_for('admin_menus'))


# function that delete item from current order, submit those orders to transaction database. supposedly the table paid for their order
@app.route('/admin/make_payment', methods=["GET", "POST"])
@login_required
def make_payment():
    table = int(
        request.form['submit']
    )  # get table number from value assigned to the submit button of the front end side

    # f = request.form
    # for key in f.keys():
    #     for value in f.getlist(key):
    #         print(key, ":", value)

    table_orders = models.OrdersOngoing.query.filter_by(table=table).all(
    )  # get orders that have matching table number with desired table number

    if request.method == 'POST':  # if method is POST
        for i in range(len(
                table_orders)):  # loop amount of food order of the table times
            if not models.Transactions.query.all(
            ):  # if transaction database is empty, assign order_id of 1
                paid_order = models.Transactions(
                    orders_id=1,
                    table=table,
                    date=get_datetime()
                    ['date'],  # call get_datetime() function to get current date
                    time=get_datetime()
                    ['time'],  # call get_datetime() function to get current time
                    name=request.form.get(
                        f'table {table} {i}',
                        False),  # get name of order from the form field name
                    price=request.form.get(
                        f'table {table} {i} price', False
                    ),  # get price of order from the form field name of price
                    amount=request.form.get(
                        f'table {table} {i} amount',  # get amount of the order from the form field name of amount
                        False),
                    subtotal=request.form.get(
                        f'table {table} subtotal',  # get subtotal of the order
                        False),
                    total=request.form.get(f'table {table} total',
                                           False))  # get total of the order
            else:  # if transaction database is not empty, assign table order of the previous max + 1
                paid_order = models.Transactions(
                    orders_id=db.session.query(
                        func.max(models.Transactions.orders_id)).scalar() + 1,
                    table=table,
                    date=get_datetime()
                    ['date'],  # call get_datetime() function to get current date
                    time=get_datetime()
                    ['time'],  # call get_datetime() function to get current time
                    name=request.form.get(
                        f'table {table} {i}',
                        False),  # get name of order from the form field name
                    price=request.form.get(
                        f'table {table} {i} price', False
                    ),  # get price of order from the form field name of price
                    amount=request.form.get(
                        f'table {table} {i} amount', False
                    ),  # get amount of order from the form field name of amount
                    subtotal=request.form.get(
                        f'table {table} subtotal',  # get subtotal of the order
                        False),
                    total=request.form.get(f'table {table} total',
                                           False))  # get total of the order
            db.session.add(paid_order)  # add to the database
        orders_to_delete = models.OrdersOngoing.query.filter_by(
            table=table).all()  # get order to delete from table number
        for order in orders_to_delete:  # loop through list of orders to be deleted and delete them from current order one by one
            db.session.delete(order)
        db.session.commit()  # commit change to the database
    return redirect(url_for('current_orders'))


# page to show the transactions of current date
@app.route('/admin/transactions', methods=["GET", "POST"])
@login_required
def transactions():
    form = forms.DateForm()  # assign DateForm to form variable to be passed
    if form.validate_on_submit():  # if request.method == 'POST'
        selected_date = form.selected_date.data.strftime(
            '%Y-%m-%d')  # convert chosen date from the form into string
        return redirect(  # redirect to transaction_date()
            url_for('transaction_date', selected_date=selected_date))
    form.selected_date.data = date.today(
    )  # if GET, pre-fill the date form with today's date
    string_date = date.today().strftime('%Y-%m-%d')  # convert date to string

    all_orders_this_date = get_orders_of_day(
        string_date)  # call the get_orders_of_day function with string of date

    return render_template(
        'admin/transactions.html',  # render template
        form=form,
        date=form.selected_date.data,
        all_orders_this_date=all_orders_this_date)


# page to show the transactions of chosen date
@app.route('/admin/transactions/<selected_date>', methods=["GET", "POST"])
@login_required
def transaction_date(selected_date):  # pass the chosen date as a parameter
    form = forms.DateForm()  # assign DateForm to form variable to be passed
    if form.validate_on_submit():  # if request.method == 'POST'
        selected_date = form.selected_date.data.strftime(
            '%Y-%m-%d')  # convert chosen date from the form into string
        return redirect(
            url_for('transaction_date', selected_date=selected_date))
    form.selected_date.data = datetime.strptime(
        selected_date,
        '%Y-%m-%d')  # if GET, fill the date form with chosen date

    string_date = form.selected_date.data.strftime(
        '%Y-%m-%d')  # convert the chosen date into string

    all_orders_this_date = get_orders_of_day(
        string_date
    )  # call get_orders_of_day() with parameter of string of the date

    return render_template(
        'admin/transactions.html',  # render page
        form=form,
        date=form.selected_date.data.date(),
        all_orders_this_date=all_orders_this_date)
