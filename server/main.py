from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import Flask, jsonify, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import dbInterface

app = Flask(__name__, template_folder='../client',
            static_folder="../client/static")

app.secret_key = '408a933de5a941fd847e78d0a5ed02f0'

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "../client/static/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

NOTIFY_SUCCESS = "alert-success"
NOTIFY_ERROR = "alert-danger"
NOTIFY_WARNING = "alert-warning"

db = SQLAlchemy(app)


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/signin', methods=['POST'])
def signIn():
    email = request.form.get("emailAddress")
    password = request.form.get("password")
    user = dbInterface.getUserByEmail(email)
    if user:
        if check_password_hash(user.password_hash, password):
            session['emailAddress'] = email
            session['firstName'] = user.first_name
            session['lastName'] = user.last_name
            session['role'] = user.role
            flash("Log-in successful", NOTIFY_SUCCESS)
            return redirect(url_for('profile'))
        flash("Wrong password", NOTIFY_ERROR)
        return redirect(url_for('login'))
    flash("User doesn't exist ", NOTIFY_WARNING)
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST'])
def signUp():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("emailAddress")
    password = request.form.get("password")
    role = "User"
    userExists = dbInterface.getUserByEmail(email)

    if not userExists:
        # generate hash with PBKDF2 algorithm using sha-256 with salt of length 8
        password_hash = generate_password_hash(password)
        # adds user to db
        dbInterface.addUser(email, firstName, lastName, password_hash, role)

        flash("Account created successfully", NOTIFY_SUCCESS)
        return redirect(url_for('login'))
    flash("Email already in use.", NOTIFY_ERROR)
    return redirect(url_for('register'))


@app.route('/confirm/<purchaseId>')
def confirmation(purchaseId):
    if purchaseId:
        purchase = dbInterface.getPurchaseById(purchaseId)
        if purchase:
            purchaseId = purchaseId
            products = dbInterface.getProductsByPurchaseId(purchaseId)
            totalCost = 0
            for product in products:
                totalCost += product.price
            # session.pop('purchaseId')
            return render_template('confirmationPage.html', purchaseId=purchaseId, purchase=purchase, products=products, totalCost=totalCost)
        return pageNotFound("")


@app.route('/additem/<productId>')
def addItemToCart(productId):
    # Check if item is already in cart
    if productId not in session['shoppingCart']:
        session['shoppingCart'].append(
            productId)
        session.modified = True
        flash("Item added successfully into cart", NOTIFY_SUCCESS)
        return jsonify(1)
    flash("Item already in cart", NOTIFY_ERROR)
    return jsonify(1)


@app.route('/buynow/<productId>')
def buyNow(productId):
    # Check if item is already in cart
    if productId not in session['shoppingCart']:
        session['shoppingCart'].append(
            productId)
        session.modified = True
        flash("Item added successfully into cart", NOTIFY_SUCCESS)
        return redirect(url_for('checkout'))
    flash("Item already in cart", NOTIFY_ERROR)
    return redirect(url_for('checkout'))


@app.route('/deleteitem/<productId>')
def deleteItemFromCart(productId):
    # Check if item is already in cart
    if productId in session['shoppingCart']:
        session['shoppingCart'].remove(
            productId)
        session.modified = True
        flash("Item successfully deleted from cart", NOTIFY_SUCCESS)
        return redirect(url_for('checkout'))
    flash("Item cannot be deleted try again", NOTIFY_ERROR)
    return redirect(url_for('checkout'))


@app.route('/profile')
def profile():
    return render_template('profilePage.html')


@app.route('/edit', methods=['POST'])
def editProfile():
    if dbInterface.getUserByEmail(request.form.get("emailAddress")):
        flash("Email address is used by another user", NOTIFY_WARNING)
        return redirect(url_for('profile'))
    dbInterface.editUserDetails(session['emailAddress'],
                                request.form.get("emailAddress"), request.form.get("firstName"), request.form.get("lastName"))
    # user.password_hash = generate_password_hash(request.form.get("password"))
    flash("Details changed successfully please relogin", NOTIFY_SUCCESS)

    return redirect(url_for('logout'))


@app.route('/')
def home():
    if 'shoppingCart' not in session:
        session['shoppingCart'] = []
    return render_template('homePage.html')


@app.route('/acceptcookie')
def acceptCookie():
    session['cookieAccepted'] = 1
    return jsonify(1)


@ app.route('/checkout')
def checkout():
    products = []
    total_cost = 0
    for productId in session['shoppingCart']:
        product = dbInterface.getProductById(productId)
        products.append(product)
        total_cost += product.price
    return render_template('checkoutPage.html', items=products, total_cost=total_cost)


@ app.route('/additem', methods=["POST"])
def addItem():
    if request.method == 'POST':
        description = request.form.get("description")
        price = request.form.get("price")
        imageUrl = request.form.get("file")
        if imageUrl.strip() == "":
            imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px" \
                       "-No_image_available.svg.png "
        dbInterface.addProduct(description, imageUrl, price, None)
        flash("Item {} created!".format(description), NOTIFY_SUCCESS)

        return redirect(url_for('items'))


@app.route('/deletelisting/<productId>', methods=["GET"])
def deleteListing(productId):
    # Delete item with specific id
    print(productId)
    dbInterface.deleteItemById(productId)
    flash("Item deleted!", NOTIFY_SUCCESS)
    return jsonify(1)


@app.route('/pay', methods=['POST'])
def purchase():
    if session['shoppingCart']:
        date = datetime.date.today()
        # need to check if item is still in stock before purchase
        if 'emailAddress' in session:
            userEmail = session['emailAddress']
            userId = dbInterface.getUserByEmail(userEmail).user_id
            purchaseId = dbInterface.addPurchase(date, userId)
        else:
            purchaseId = dbInterface.addPurchase(date)
        for productId in session['shoppingCart']:
            dbInterface.addPurchaseIdToProduct(productId, purchaseId)
        session['purchaseId'] = purchaseId
        session.pop('shoppingCart')
        session['shoppingCart'] = []
        return redirect(url_for('confirmation', purchaseId=hash(purchaseId)))


@app.errorhandler(404)
def pageNotFound(e):
    flash("Invalid Address!", NOTIFY_ERROR)
    return render_template('homepage.html'), 404


@app.route('/items/<productId>')
def productDetails(productId):
    product = dbInterface.getProductById(productId)
    setId = product.set_id
    setObj = None
    setProducts = None
    if setId:
        setObj = dbInterface.getSetById(setId)
        setProducts = dbInterface.getProductsBySetId(setId)
    return render_template('itemPage.html', product=product, setObj=setObj, setProducts=setProducts)


@app.route('/logout')
def logout():
    session.pop('emailAddress', default=None)
    session.pop('firstName', default=None)
    session.pop('lastName', default=None)
    session.pop('role', default=None)
    flash("Logout successfull", NOTIFY_SUCCESS)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    if 'emailAddress' in session:
        return redirect(url_for('profile'))
    return render_template('loginPage.html')


@app.route('/register')
def register():
    return render_template('registerPage.html')


@app.route('/items')
def items():
    # print(session['role'])
    return render_template('itemCard.html', items=dbInterface.getProducts())


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    session['shoppingCart'] = []
