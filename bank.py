"""
Catamount Community Bank
Flask Routes

Warning: This app contains deliberate security vulnerabilities
Do not use in a production environment! It is provided for security
training purposes only!

"""


from flask import Flask, render_template, request, url_for, flash, redirect
from lessons import sql_injection
from lessons.password_crack import hash_pw, authenticate

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')


@app.route("/", methods=['GET', 'POST'])
def home():
    """ Bank home page """
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page")


@app.route("/transactions", methods=['GET', 'POST'])
def transactions():
    """ Transaction injection attack """
    search_term = ''
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        q = sql_injection.create_search_query(1234, search_term)
    else:
        q = 'SELECT * FROM trnsaction WHERE trnsaction.account_id = 1234'
    rows = c.fetchall()
    return render_template('transactions.html',
                           search_term=search_term,
                           rows=rows,
                           query=q,
                           title="My Transactions",
                           heading="My Transactions")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/login_success/<int:id_>", methods=['GET', ])
def login_success(id_):
    return render_template('customer_home.html',
                           title="Customer Home",
                           heading="Customer Home")


@app.route('/catcoin_stock')
def cat_coin_stock():
    return render_template("catcoin_stock.html")


@app.route("/hashit", methods=['GET', ])
def hashit():
    """ Hash a password. DON'T EVER DO THIS LIKE THIS IN THE REAL WORLD!
        To use this route to generate a sha1 hash:
        1. Run the Flask app (werk.py)
        2. Open a browser and follow this format in the URL:
            http://localhost:8097/hashit?pw=testpassword
            where the password "testpassword" is passed into the "hashit" function and
            the sha1 hash of that string is returned in the browser (in this case):
                8bb6118f8fd6935ad0876a3be34a717d32708ffd
        3. Replace "testpassword" in the query string with another string to generate
            the sha1 hash of that string.
    """
    pw = request.args.get('pw')
    salt = request.args.get('salt')
    if salt is None:
        salt = ''
    return hash_pw(pw, salt)
