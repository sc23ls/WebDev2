from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    shipping_address = db.Column(db.String(200))

    orders = db.relationship('Orders', backref='user_orders', lazy='dynamic')
    favourites = db.relationship(
        'Favourite', backref='user_favourites', lazy='dynamic')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    price = db.Column(db.Float, index=True, nullable=False)
    description = db.Column(db.String(300), index=True, nullable=False)
    category = db.Column(db.String(300), index=True, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    stock = db.Column(db.Integer, index=True, nullable=False)
    favourites_count = db.Column(db.Integer)

    orders = db.relationship('OrderProducts', backref='orders', lazy='dynamic')
    favourites = db.relationship(
        'Favourite', backref='product_favourites', lazy='dynamic')

    def image_path(self):
        if self.image:
            return f'/static/productimages/{self.image}'
        return '/static/productimages/default.jpg'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_cost = db.Column(db.Float, index=True, nullable=False)
    created = db.Column(db.DateTime)

    products = db.relationship(
        'OrderProducts', backref='products', lazy='dynamic')


class OrderProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'product_id', name='unique_like'),)
