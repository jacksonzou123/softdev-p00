#Team Bits Please
#SoftDev1 pd1
#P00: Da Art of Storytellin'
#2019-10-28

from flask import Flask, render_template, session, url_for, request, redirect, flash
from utl import tester, db_builder
import os

app = Flask(__name__)
#session secret key, code from Stack Overflow
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return redirect(url_for('sign')) #else go to sign-in options

@app.route("/welcome")
def sign():
    return render_template('welcome.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/adduser", methods=['POST'])
def adduser():
    username = request.form['username']
    password = request.form['password']
    #print(request.method)
    #print(username)
    #print(password)
    added = tester.addUser(username, password)
    if (added):
        id = tester.getUser(username)
        session["userid"] = id
        #print(session["userid"])
        flash('You have been registered successfully. Please log in.', 'green')
        return redirect(url_for('login'))
    flash('Username already taken.', 'red')
    return redirect(url_for('register'))

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/auth", methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    verified = tester.verifyUser(username, password)
    if (verified):
        id = tester.getUser(username)
        session["userid"] = id
        flash('You have logged in successfully.', 'green')
        return redirect(url_for('profile', id=id))
    flash('Error with logging in', 'red')
    return redirect(url_for('login'))

## USER MAY NOT PROCEED PAST HERE WITHOUT BEING LOGGED IN ##

#checks if user is logged in

@app.route("/user")
def profile():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    print(request.args['id'])
    return render_template('profile.html')

@app.route("/about")
def about():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return render_template('about.html')

@app.route("/search")
def search():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    #QUERY STRING
    #IF NO QUERY STRING RET ONLY FORM
    return "search form"

@app.route("/query")
def query():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return "process search form"

@app.route("/createblog")
def createblog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return "create a new blog"

@app.route("/updateblog")
def updateblog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return "process create blog form"

@app.route("/blog")
def blog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    #QUERY STRING
    return "View blog"

@app.route("/entry")
def entry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    #QUERY STRING
    return "View blog entry"

@app.route("/editentry")
def editentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return "Create or edit blog entry"

@app.route("/updateentry")
def updateentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    return "process edit entry form"

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'green')
    return redirect(url_for('root'))

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
