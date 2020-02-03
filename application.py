import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, usd, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///RSdatabase.db")


@app.route("/")
@login_required
def index():
    """Show homepage"""
    return render_template("home.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    try:

        if not len(request.form.get("username")) >= 1:

            return jsonify(False)

        elif False:

            return jsonify(False)

        else:

            return jsonify(True)

    except:

        return jsonify(False)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if get request

    if request.method == "POST":

        # init variables

        username = request.form.get("username")

        password = request.form.get("password")

        passwordc = request.form.get("confirmation")

        firstname = request.form.get("firstname")

        lastname = request.form.get("lastname")

        email = request.form.get("email")

        # if any field is empty, return apology

        if username == "" or password == "" or passwordc == "":

            return apology("Oops. You can only register by filling in all fields")

        # if password is not password-confirmed, return apology

        if password != passwordc:

            return apology("Oops. You entered 2 different passwords. Make sure you type the same twice.")

        # else insert new user into database

        else:

            hp = generate_password_hash(password)

            db.execute("INSERT INTO users (username, hash, email, firstname, lastname) VALUES (:usr, :passw, :email, :fname, :lname)", usr=username, passw=hp, email=email, fname=firstname, lname=lastname)

            return redirect("/login")

        #if user already exists, return apology

        #if not result:

            #return apology("Registration failed. It seems this username is already in use by someone. Maybe you?")

    else:

        return render_template("register.html")


@app.route("/profile")
def profile():
    """Show user's profile"""

    # get user's db entry
    rows = db.execute("SELECT * FROM users WHERE id = :userid",
                      userid=session["user_id"])

    # Ensure the profile is found
    if len(rows) != 1:
        return apology("oops something wrong with this profile...", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to login form
    return render_template("profile.html", username=rows[0]["username"], firstname=rows[0]["firstname"], lastname=rows[0]["lastname"], email=rows[0]["email"])


@app.route("/events")
def events():
    """Show user's events"""

    # get user's db entry
    rows = db.execute("SELECT * FROM users WHERE id = :userid",
                      userid=session["user_id"])

    # Ensure the profile is found
    if len(rows) != 1:
        return apology("oops something wrong with this profile...", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # get user's events from database
    events = db.execute("SELECT * FROM events WHERE userid = :userid",
                      userid=session["user_id"])

    # Redirect user to login form
    return render_template("events.html", username=rows[0]["username"], events=events)

@app.route("/newevent", methods=["GET", "POST"])
def newevent():
    """Show user's events"""

    if request.method == "GET":

        return render_template("newevent.html")

    else:

        # log new event to database

        title = request.form.get("title")

        date = request.form.get("date")

        #location = str(request.form.get("venue")) + ', ' str(request.form.get("house")) + ', ' + str(request.form.get("street")) + ', ' + str(request.form.get("city")) + ', ' + str(request.form.get("zip")) + ', ' + str(request.form.get("country"))
        location = request.form.get("venue")

        starttime = request.form.get("starttime")

        endtime = request.form.get("endtime")

        tc = request.form.get("table_cloth")

        ls = request.form.get("led_strip")

        ch = request.form.get("chandelier")

        db.execute("INSERT INTO events (title, date, location, userid, table_cloth, led_strip, chandelier) \
            VALUES (:ttl, :dt, :loc, :uid, :tc, :ls, :ch)", ttl=title, dt=date, loc=location, uid=session["user_id"], tc=tc, ls=ls, ch=ch)

        # return to events

        # get user's db entry
        rows = db.execute("SELECT * FROM users WHERE id = :userid",
                          userid=session["user_id"])

        # Ensure the profile is found
        if len(rows) != 1:
            return apology("oops something wrong with this profile...", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # get user's events from database
        events = db.execute("SELECT * FROM events WHERE userid = :userid",
                          userid=session["user_id"])

        print(events)

        # Redirect user to login form
        return render_template("events.html", username=rows[0]["username"], events=events)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html")
    #, e.name, e.code


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
