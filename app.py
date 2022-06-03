from cs50 import SQL
from flask import Flask, flash, jsonify, render_template, redirect, request, session
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Shamelessly copy from Pset9
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use SQLite database
db = SQL("sqlite:///jokes.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    """ Render index.html """
    return render_template("index.html")


@app.route("/delete", methods=["POST"])
def delete():
    if not request.form.get("joke"):
        return jsonify(error=True)
    else:
        db.execute("DELETE FROM favorites WHERE joke_id = (SELECT id FROM jokes WHERE joke = ?)", request.form.get("joke"))

    return jsonify(success=True)


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """ Add/Show users' favorites """

    if request.method == "POST":

        if not request.form.get("jokeId"):
            return jsonify({"message": "You didn't generate a joke"})
        elif db.execute("SELECT * FROM favorites WHERE user_id = ? AND joke_id = ?", session["user_id"], request.form.get("jokeId")):
            return jsonify({"message": "Joke already added"})
        else:
            db.execute("INSERT INTO favorites (user_id, joke_id) VALUES (?, ?)", session["user_id"], request.form.get("jokeId"));
            return jsonify({"message": "Joke successfully added"})

    jokes = db.execute("SELECT joke, punchline FROM jokes JOIN favorites ON jokes.id = favorites.joke_id WHERE favorites.user_id = ?", session["user_id"])

    return render_template("favorites.html", jokes = jokes)


@app.route("/generate")
def generate():
    """ Generate a joke """

    joke = db.execute("SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1")[0];

    return jsonify(joke)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if not session.get("user_id") is None:
        return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash(u"Must provide username", "error")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash(u"Must provide password", "error")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash(u"Invalid username/password", "error")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Alert user a success login
        flash("Logged in!")

        # Redirect user to favorites page
        return redirect("/favorites")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if not session.get("user_id") is None:
        return redirect("/")

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash(u"Must provide username", "error")
            return redirect("/register")


        # Ensure password was submitted
        elif not request.form.get("password"):
            flash(u"Must provide password", "error")
            return redirect("/register")

        # Ensure password and password confirmation were matched
        elif not request.form.get("password") == request.form.get("confirmation"):
            flash(u"Passwords do not match", "error")
            return redirect("/register")

        # Ensure username was not existed
        elif db.execute("INSERT OR IGNORE INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')) == None:
            flash(u"Username already taken", "error")
            return redirect("/register")

        # Redirect user back to /login
        return redirect("/login")

    # Open registration page
    return render_template("register.html")
