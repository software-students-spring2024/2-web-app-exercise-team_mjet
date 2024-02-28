#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, redirect, url_for

# from markupsafe import escape
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import flask_login #this will be used for user authentication
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

# instantiate the app
app = Flask(__name__)
bcrypt = Bcrypt(app) 
#these 2 are for flask login
login_manager = LoginManager()
login_manager.init_app(app)

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]  # store a reference to the database

# the following try/except block is a way to verify that the database connection is alive (or not)
try:
    # verify the connection works by pinging the database
    cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(" * MongoDB connection error:", e)  # debug

# set up the routes


# # turn on debugging if in development mode
# if os.getenv("FLASK_ENV", "development") == "development":
#     # turn on debugging, if in development
#     app.debug = True  # debug mnode

class User(flask_login.UserMixin):
    pass


#this callback is used to reload the user object from the user ID stored in the session.It should take the str ID of a user, and return the corresponding user object
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    """
    Route for the home page
    """
    return render_template("index.html")  # render the hone template


# route to accept the form submission to delete an existing post
@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    """
    Route for GET AND POST for signup page
    """
    if request.method == "POST":
        username = request.form["fusername"]
        password = request.form["fpassword"]
        user = db.users.find_one({"username": username})
        if user:
            return render_template("signup.html", error="Username already in use.")
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
            new_user = {'username': username, 'password': hashed_password, 'items': []}
            db.users.insert_one(new_user)
            return redirect(url_for("log_in"))
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def log_in():
    """
    Route for GET AND POST for login page
    """
    if request.method == "POST":
        username = request.form["fusername"]
        password = request.form["fpassword"]
        user = db.users.find_one({"username": username})
        if user:
            print("do something")
        else:
            return render_template('login.html', error="User not found.")
    return render_template("login.html")






# run the app
if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=FLASK_PORT)