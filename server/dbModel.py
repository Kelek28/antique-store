from main import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32))


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    image_url = db.Column(db.String(512))
    price = db.Column(db.Integer)
    set_id = db.Column(db.Integer, db.ForeignKey('set.set_id'))
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.purchase_id'))


class Set(db.Model):
    set_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    price = db.Column(db.Integer)


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.Date)


db.create_all()
db.session.commit()
