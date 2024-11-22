"""
Dan's Coffee Shop
Flask Routes

Inspired by the Catamount Community Bank flask app written by Jim Eddy.
"""


from flask import Flask, render_template, request, url_for, redirect
from lessons.password_crack import hash_pw, authenticate
import sqlite3

app = Flask(__name__, static_folder='instance/static')
app.config.from_object('config')

# global variables that store data while switching between menus
username_logged_in = ''
username_locked_out = ''
access_level = ''
failed_logins ={}

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
    global username_logged_in, access_level, username_locked_out, failed_logins
    if request.method == 'POST':
        if 'home' in request.form.to_dict().keys():  # returns home if user clicked that button
            return redirect(url_for('home'))
        # gets username and password entered
        username = request.form.get('username')
        password = request.form.get('password')
        # connects to database and retrieves all user information
        connection = sqlite3.connect('dans_coffee_shop.db')
        cursor = connection.cursor()
        cursor.execute('''
                          SELECT * FROM user_info      
                            ''')
        user_data = cursor.fetchall()
        connection.commit()
        connection.close()

        # searches for user, changes value of user_exists if user is found
        user_exists = False
        saved_password = ''
        for user in user_data:
            print(user)
            if username == user[0]:
                user_exists = True
                username_logged_in = user[0]
                saved_password = user[1]
                access_level = user[2]

        if not user_exists:  # tells user they entered wrong username
            return redirect(url_for('user_not_found'))
        if username_logged_in in failed_logins.keys():  # locks user out if they have already tried signing in 3 times
            if failed_logins[username_logged_in] >= 3:
                username_locked_out = username_logged_in
                username_logged_in = ''
                access_level = ''
                return redirect(url_for('locked_out'))
        if authenticate(saved_password, password):  # logs user in if their password is correct
            return redirect(url_for('logged_in'))
        if username_logged_in not in failed_logins.keys():  # adds user to failed logins if it's their first login fail
            failed_logins[username_logged_in] = 1
        else:  # increments the number of failed logins this user has
            failed_logins[username_logged_in] = failed_logins[username_logged_in] + 1
        if failed_logins[username_logged_in] >= 3:  # locks user out if they failed 3 or more times
            username_locked_out = username_logged_in
            username_logged_in = ''
            access_level = ''
            return redirect(url_for('locked_out'))

        # resets global variables and informs user their password was incorrect
        username_logged_in = ''
        access_level = ''
        return redirect(url_for('incorrect_password'))
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/user_not_found", methods=['GET', 'POST'])
def user_not_found():
    if request.method == 'POST':
        if 'back' in request.form.to_dict().keys():
            return redirect(url_for('login'))
    return render_template('user_not_found.html')


@app.route("/incorrect_password", methods=['POST', 'GET'])
def incorrect_password():
    if request.method == 'POST':
        if 'back' in request.form.to_dict().keys():
            return redirect(url_for('login'))

    return render_template('incorrect_password.html')


@app.route("/locked_out", methods=['GET', 'POST'])
def locked_out():
    if request.method == 'POST':
        if 'back' in request.form.to_dict().keys():
            return redirect(url_for('login'))
        elif 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))
    return render_template('locked_out.html', username=username_locked_out)

@app.route("/logged_in", methods=['GET', 'POST'])
def logged_in():
    if request.method == 'POST':
        if 'home' in request.form.to_dict().keys():
            global username_logged_in, access_level
            username_logged_in = ''
            access_level = ''
            return redirect(url_for('home'))
    return render_template('logged_in.html', username=username_logged_in)

@app.route("/register",  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'home' in request.form.to_dict().keys():
            return redirect(url_for('home'))
        elif 'pw_gen' not in request.form.to_dict().keys():  # user clicked the submit button
            username = request.form.get('username')
            password = request.form.get('password')
            if '"' in username or '"' in password:  # prevents sql injection
                return redirect(url_for('registration_failed'))
            if 4 <= len(username) <= 12 and check_password_strength(password):  # checks constraints on new login info
                password_hash = hash_pw(password)  # hashes the password with a salt to be saved in the database
                # adds new user to the database
                connection = sqlite3.connect('dans_coffee_shop.db')
                cursor = connection.cursor()
                cursor.execute('''
                        INSERT INTO user_info (username, password, access_level)
                        VALUES ("''' + username + '''", "''' + password_hash + '''", "customer")
                    ''')
                connection.commit()
                connection.close()

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
            elif char in "!@#$%&*?(){}[]":
                has_special = True

        # returns the result. Will return false if at least one requirement was not satisfied
        return has_num and has_special and has_lower and has_upper
