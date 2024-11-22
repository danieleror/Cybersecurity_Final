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
    if request.method == 'POST':
        if 'login' in request.form.to_dict().keys():
            return redirect(url_for('login'))
        elif 'register' in request.form.to_dict().keys():
            return redirect(url_for('register'))
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))

    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/register",  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))
        username = request.form.get('username')
        password = request.form.get('password')
        if 4 <= len(username) <= 12 and check_password_strength(password):
            password_hash = hash_pw(password)
            # TODO add new user to database
            return redirect(url_for('registration_success'))
        else:
            return redirect(url_for('registration_failed'))
    return render_template('register.html',
                           title="New User Registration",
                           heading="New User Registration")


@app.route("/registration_failed", methods=['GET', 'POST'])
def registration_failed():
    if request.method == 'POST':
        if 'back' in request.form.to_dict().keys():
            return redirect(url_for('register'))
        elif 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))
    return render_template('registration_failed.html')


@app.route("/registration_success", methods=['GET', 'POST'])
def registration_success():
    if request.method == 'POST':
        if 'login' in request.form.to_dict().keys():
            return redirect(url_for('login'))
        elif 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))
    return render_template('registration_success.html')


@app.route("/login_success/<int:id_>", methods=['GET', ])
def login_success(id_):
    return render_template('customer_home.html',
                           title="Customer Home",
                           heading="Customer Home")


def check_password_strength(pw) -> bool:
    # Checks given password to see if it follows constraints. Returns true or false accordingly
    if len(pw) < 8 or len(pw) > 25:
        return False  # returns false if not long enough
    else:
        has_upper = False
        has_lower = False
        has_num = False
        has_special = False
        # iterates through each character. sets each boolean to true once each requirement is found
        for char in pw:
            ascii_value = ord(char)
            if 48 <= ascii_value <= 57:
                has_num = True
            elif 65 <= ascii_value <= 90:
                has_upper = True
            elif 97 <= ascii_value <= 122:
                has_lower = True
            elif 33 <= ascii_value <= 47 or \
                 58 <= ascii_value <= 64 or \
                 91 <= ascii_value <= 96 or \
                 123 <= ascii_value <= 126:
                has_special = True

        # returns the result. Will return false if at least one requirement was not satisfied
        return has_num and has_special and has_lower and has_upper
