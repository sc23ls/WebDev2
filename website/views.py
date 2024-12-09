from typing import Sequence
from flask import render_template, flash, request, redirect, json, session, url_for, jsonify
from website import app
from flask_login import login_required, current_user
from .forms import editForm
from werkzeug.security import generate_password_hash
from datetime import datetime
from . import db
from .models import *
from flask_admin.contrib.sqla import ModelView


@app.post('/create_product')
def create_product():
    data = json.loads(request.data)
    title = data.get('title')
    price = float(data.get('price'))
    description = data.get('description')
    category = data.get('category')
    image = data.get('image')
    stock = bool(data.get('stock'))

    p = Products(title=title, price=price, description=description,
                 category=category, image=image, stock=stock)
    db.session.add(p)
    db.session.commit()
    return {}, 200


@app.route('/')
def home():
    products = db.session.execute(db.select(Products)).scalars()
    return render_template('index.html', title='Home', user=current_user, products=products)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account', user=current_user)


@app.route('/all_items')
@login_required
def all_items():
    products = db.session.execute(db.select(Products)).scalars()
    return render_template('all_items.html', title='All Items', user=current_user, products=products)


@app.route('/hoodies')
@login_required
def hoodies():
    products = db.session.execute(db.select(Products).where(
        Products.category == 'Hoodies')).scalars()
    return render_template('hoodies.html', title='Hoodies', user=current_user, products=products)


@app.route('/bottoms')
@login_required
def bottoms():
    products = db.session.execute(db.select(Products).where(
        Products.category == 'Bottoms')).scalars()
    return render_template('bottoms.html', title='Bottoms', user=current_user, products=products)


@app.route('/item/<int:product_id>')
@login_required
def item_detail(product_id):
    item = db.session.execute(db.select(Products).where(
        Products.id == product_id)).scalar()
    if item is None:
        return render_template('404.html', title='404_page_not_found', user=current_user, message='Uh oh! Page does not exist')
    return render_template('product_page.html', title=item.title, item=item, user=current_user)


@app.route('/basket')
@login_required
def basket():
    basket = session.get('basket', {})
    total = sum(item['price'] * item['quantity'] for item in basket.values())

    return render_template('basket.html', user=current_user, basket=basket, total=total)


@app.post('/add_to_basket/<int:id>')
def add_to_basket(id: int):
    item: Products = db.session.execute(
        db.select(Products).where(Products.id == id)).scalar()
    if item is None:
        return render_template('404.html', user=current_user, message="Product does not exist")

    if 'basket' not in session:
        session['basket'] = {}

    basket = session['basket']

    if str(id) in basket:
        basket[str(id)]['quantity'] += 1
    else:
        basket[str(id)] = {
            'title': item.title,
            'price': item.price,
            'quantity': 1
        }

    session['basket'] = basket
    return {}


@app.delete('/delete_from_basket/<int:id>')
def delete_from_basket(id: int):
    if 'basket' not in session:
        return {}, 404

    basket = session['basket']

    if str(id) not in basket:
        return {}, 404
    else:
        basket[str(id)]['quantity'] -= 1
        if basket[str(id)]['quantity'] <= 0:
            del basket[str(id)]

    session['basket'] = basket
    return {}


@app.route('/checkout', methods=['GET'])
def checkout():
    basket = session.get('basket', {})

    if not basket:
        flash("Basket is empty")
        return redirect(url_for('basket'))

    total = sum(item['price'] * item['quantity'] for item in basket.values())
    order = Orders(customer_id=current_user.id,
                   total_cost=total, created=datetime.now())
    db.session.add(order)
    db.session.commit()

    for key, item in basket.items():
        db.session.add(OrderProducts(order_id=order.id,
                       product_id=key, quantity=item['quantity']))

    db.session.commit()

    session.pop('basket', None)
    return redirect(url_for('my_orders'))


@app.route('/change_information/<int:id>', methods=['GET', 'POST'])
def edit(id):
    UserID = User.query.get(id)
    form = editForm(obj=UserID)
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        shipping_address = request.form.get('shipping_address')
        password = request.form.get('password')

        if len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(name) < 2:
            flash("Name must be more than 1 character", category="error")
        elif len(password) < 7:
            flash("Password must be atleast 7 characters", category="error")
        elif len(shipping_address) < 2:
            flash("Please enter a valid shipping address", category="error")
        else:
            # editing the data
            UserID.name = name
            UserID.email = email
            UserID.shipping_address = shipping_address
            UserID.password = generate_password_hash(password)

            db.session.add(UserID)
            db.session.commit()
            flash("Information changed successfully!", category="success")
            return redirect('/account')
    return render_template('change_information.html',
                           title='Edit Information',
                           UserID=UserID,
                           form=form,
                           user=current_user)


@app.post('/favourite/<int:product_id>')
@login_required
def favourite_product(product_id):
    product = db.session.execute(db.select(Products).where(
        Products.id == product_id)).scalar()
    existing_favourite = db.session.execute(db.select(Favourite).where(
        Favourite.user_id == current_user.id).where(Favourite.product_id == product_id)).scalar()

    if product is None:
        return jsonify({'message': "Uh oh! Product does not exits"}), 404

    if existing_favourite:
        db.session.delete(existing_favourite)
        product.favourites_count -= 1
    else:
        favourite = Favourite(user_id=current_user.id, product_id=product_id)
        db.session.add(favourite)
        if product.favourites_count is None:
            product.favourites_count = 0
        product.favourites_count += 1

    db.session.commit()
    return jsonify({'favourites': product.favourites_count})


@app.route('/favourites', methods=["GET"])
def favourites():
    favourites = db.session.execute(
        db.select(Favourite).where(Favourite.user_id == current_user.id)
    ).scalars()
    products = [
        db.session.execute(
            db.select(Products).where(Products.id == fav.product_id)
        ).scalar() for fav in favourites
    ]

    return render_template('favourites.html', user=current_user, products=products)


@app.route('/my_orders')
def my_orders():
    orders = db.session.execute(
        db.select(Orders).where(Orders.customer_id == current_user.id)
    ).scalars()

    return render_template('my_orders.html', user=current_user, orders=orders)


@app.template_filter()
def format_date(value):
    return datetime.strftime(value, "%d/%m/%Y")


@app.route('/order_details/<int:id>')
def order_details(id: int):
    order = db.session.execute(
        db.select(Orders).where(Orders.id == id)).scalar()
    order_prods: Sequence[OrderProducts] = db.session.execute(
        db.select(OrderProducts).where(OrderProducts.order_id == id)
    ).scalars().all()
    products = []
    for ord_prod in order_prods:
        product = (db.session.execute(db.select(Products).where(
            Products.id == ord_prod.product_id)).scalar(), ord_prod.quantity)
        products.append(product)
    print(products)

    return render_template('order_details.html', user=current_user, products=products, order=order)
