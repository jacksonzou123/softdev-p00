#Team Bits Please
#SoftDev1 pd1
#P00: Da Art of Storytellin'
#2019-10-28

from flask import Flask, render_template, session, url_for, request, redirect, flash
import os

app = Flask(__name__)
#session secret key, code from Stack Overflow
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if ("user" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return redirect(url_for('sign')) #else go to sign-in options

@app.route("/sign")
def sign():
    return render_template('sign.html')

@app.route("/select")
def select():
    return "process sign in form"

@app.route("/register")
def register():
    return "Register new user"

@app.route("/adduser")
def adduser():
    return "Process register form"

@app.route("/login")
def login():
    return "login"

@app.route("/auth")
def auth():
    return "Process login form"

## USER MAY NOT PROCEED PAST HERE WITHOUT BEING LOGGED IN ##

@app.route("/user")
def profile():
    #QUERY STRING
    return "user profile"

@app.route("/about")
def about():
    return "About page"

@app.route("/search")
def search():
    #QUERY STRING
    #IF NO QUERY STRING RET ONLY FORM
    return "search form"

@app.route("/query")
def query():
    return "process search form"

@app.route("/createblog")
def createblog():
    return "create a new blog"

@app.route("/updateblog")
def updateblog():
    return "process create blog form"

@app.route("/blog")
def blog():
    #QUERY STRING
    return "View blog"

@app.route("/entry")
def entry():
    #QUERY STRING
    return "View blog entry"

@app.route("/editentry")
def editentry():
    return "Create or edit blog entry"

@app.route("/updateentry")
def updateentry():
    return "process edit entry form"

@app.route("/logout")
def logout():
    return "Logout"

if __name__ == "__main__":
    app.debug = True
    app.run()
