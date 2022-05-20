from dbModel import *
from main import db


def getUsers():
    return User.query.all()


def getUserByEmail(email):
    return User.query.filter_by(email=email).first()


def deleteItemById(id):
    Product.query.filter_by(product_id=id).delete()
    db.session.commit()


def addUser(email, first_name, last_name, password_hash, role, user_id=None):
    if user_id:
        user = User(user_id=user_id,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password_hash=password_hash,
                    role=role)
    else:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password_hash=password_hash,
                    role=role)
    db.session.add(user)
    db.session.commit()


def editUserDetails(email, newEmail, newFirstName, newLastName):
    user = getUserByEmail(email)
    user.email = newEmail
    user.first_name = newFirstName
    user.last_name = newLastName
    db.session.commit()


def getProducts():
    return Product.query.all()


def getProductById(product_id):
    return Product.query.get(product_id)


def getProductsByPurchaseId(purchase_id):
    return Product.query.filter_by(purchase_id=purchase_id).all()


def getProductsBySetId(set_id):
    return Product.query.filter_by(set_id=set_id).all()


def addProduct(description, image_url, price, set_id, product_id=None):
    if product_id:
        product = Product(product_id=product_id,
                          description=description,
                          image_url=image_url,
                          price=price,
                          set_id=set_id)
    else:
        product = Product(description=description,
                          image_url=image_url,
                          price=price,
                          set_id=set_id)
    db.session.add(product)
    db.session.commit()


def addProductToSet(product_id, set_id):
    product = getProductById(product_id)
    product.set_id = set_id
    db.session.commit()


def addImageUrlToProduct(product_id, image_url):
    product = getProductById(product_id)
    product.image_url = image_url
    db.session.commit()


def addPurchaseIdToProduct(product_id, purchase_id):
    product = getProductById(product_id)
    product.purchase_id = purchase_id
    db.session.commit()


def getSets():
    return Set.query.all()


def getSetById(set_id):
    return Set.query.get(set_id)


def addSet(description, price, set_id=None):
    if set_id:
        new_set = Set(set_id=set_id,
                      description=description,
                      price=price)
    else:
        new_set = Set(description=description,
                      price=price)
    db.session.add(new_set)
    db.session.commit()


def getPurchases():
    return Purchase.query.all()


def getPurchaseById(purchase_id):
    return Purchase.query.get(purchase_id)


def getPurchase(user_id, date):
    return Purchase.query.filter_by(user_id=user_id, date=date).first()


def addPurchase(date, user_id=None, purchase_id=None):
    if purchase_id:
        if user_id:
            purchase = Purchase(purchase_id=purchase_id,
                                user_id=user_id,
                                date=date)
        else:
            purchase = Purchase(purchase_id=purchase_id,
                                date=date)
    else:
        if user_id:
            purchase = Purchase(user_id=user_id,
                                date=date)
        else:
            purchase = Purchase(date=date)
    db.session.add(purchase)
    db.session.commit()
    return purchase.purchase_id
