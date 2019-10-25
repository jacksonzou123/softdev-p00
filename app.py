#Team Bits Please
#SoftDev1 pd1
#P00: Da Art of Storytellin'
#2019-10-28

from flask import Flask, render_template, session, url_for, request, redirect, flash
from utl import db_builder, tester
import os
from datetime import date

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
    if (username == '' or password == ''):
        flash('Fields cannot be left empty', 'red')
        return redirect(url_for('register'))
    #print(request.method)
    #print(username)
    #print(password)
    added = tester.addUser(username, password)
    if (added):
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
        id = tester.getUserIDStr(username)
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
    #print(request.args['id'])
    if (request.args): #if url has query string
        if ('id' in request.args): #if url has id
            id = request.args['id']
            name = tester.getUserInfo(id)
            if (name): #if id is valid user id
                username = name[0]
                isOwner = False
                if (id == session['userid']):
                    isOwner = True
                blogs = tester.getAllBlogs(id)
                return render_template('profile.html', username=username, isOwner=isOwner, blogs = blogs) #success!
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red')
        else:
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red')
    return redirect(url_for('profile', id=session["userid"]))

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
    username = tester.getUserInfo(session['userid'])[0]
    return render_template('createblog.html', username=username)

@app.route("/updateblog", methods=['POST'])
def updateblog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    title = request.form['title']
    if (title == ''):
        flash('Fields cannot be empty', 'red')
        return redirect(url_for('createblog'))
    #print(title)
    id = tester.addBlog(session['userid'], title)
    if (id == None):
        flash('You have already used this title', 'red')
        return redirect(url_for('createblog'))
    return redirect(url_for('blog', id=id))

@app.route("/blog")
def blog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    #QUERY STRING
    if (request.args):
        if ('id' in request.args):
            id = request.args['id']
            name = tester.getBlogTitle(id)[0]
            if (name):
                title = name[0]
                isOwner = False
                user_id = tester.getUserfromBlog(id)[0]
                username = tester.getUserInfo(user_id)[0]
                if (int(user_id) == int(session['userid'])):
                    isOwner = True
                userlink = "/user?id=%s" % user_id
                return render_template('blog.html', username=username, isOwner=isOwner, title=name, userlink=userlink)
            flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
        else:
            flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    else:
        flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    return redirect(url_for('profile', id=session['userid']))

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
    return render_template('createentry.html')

@app.route("/updateentry")
def updateentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    heading = request.form['header']
    content = request.form['content']
    if (heading == '' or content == ''):
        flash('Fields cannot be empty', 'red')
        return redirect(url_for('editentry'))
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
