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
    confirm = request.form['confirm']
    if (username == '' or password == ''):
        flash('Fields cannot be left empty', 'red')
        return redirect(url_for('register'))
    #print(request.method)
    #print(username)
    #print(password)
    if (password != confirm):
        flash('Passwords do not match!', 'red')
        return redirect(url_for('register'))
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
                blogs = tester.getUserBlogs(id)
                return render_template('profile.html', username=username, owner=username, isOwner=isOwner, blogs = blogs) #success!
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red')
        else:
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red')
    return redirect(url_for('profile', id=session["userid"]))

@app.route("/about")
def about():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    return render_template('about.html', username=username)

@app.route("/search")
def search():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    #QUERY STRING
    username = tester.getUserInfo(session['userid'])[0]
    results = []
    if (request.args):
        if ('query' in request.args):
            query = request.args['query']
            results = tester.findBlog(query)
            print(results)
    return render_template('search.html', username=username, results=results)

@app.route("/query", methods=['POST'])
def query():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    query = request.form['keyword']
    return redirect(url_for('search', query=query))

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
            name = tester.getBlogTitleStr(id)
            if (name):
                isOwner = False
                user_id = tester.getUserfromBlog(id)[0]
                username = tester.getUserInfo(user_id)[0]
                if (int(user_id) == int(session['userid'])):
                    isOwner = True
                userlink = "/user?id=%s" % user_id
                session['blogid'] = id
                entries = tester.getAllEntries(id)
                return render_template('blog.html', username=username, isOwner=isOwner, title=name, userlink=userlink, entries=entries)
            flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
        else:
            flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    else:
        flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    return redirect(url_for('profile', id=session['userid']))

@app.route("/editentry")
def editentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    temp_title = ""
    temp_content = ""
    if (request.args):
        if ('id' in request.args):
            id = request.args['id']
            temp_title = tester.getEntryTitle(id)
            temp_content = tester.getEntryContent(id)
    return render_template('createentry.html', username=username, temp_title=temp_title, temp_content=temp_content)

@app.route("/updateentry", methods=['POST'])
def updateentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    heading = request.form['title']
    content = request.form['content']
    if (heading == '' or content == ''):
        flash('Fields cannot be empty', 'red')
        return redirect(url_for('editentry'))
    title = request.form['title']
    content = request.form['content']
    id = session['blogid']
    entry = tester.addEntry(id, title, content)
    if (entry == None):
        flash("You have already used this heading", 'red')
        return redirect(url_for('editentry'))
    return redirect(url_for('blog', id=id))

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'green')
    return redirect(url_for('root'))

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
