#Team Bits Please
#SoftDev 1 pd1
#P00 -- Da Art of Storytellin'
#2019-10-28

import sqlite3
import random
import sys
from utl.db_builder import exec

#for creating randomly generated id numbers
limit = sys.maxsize
#==========================user functions===========================

#helper function
def addUserHelper(username, password, data):
    rand = random.randrange(limit)
    while (rand in data):
        rand = random.randrange(limit)
    #print(rand)
    command = "INSERT INTO user_tbl VALUES(" + str(rand) + ",\"" + username + "\",\"" + password + "\")"
    #print(command)
    exec(command)


#addUser
def addUser(username, password):
    q = "SELECT * FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    if (data is None):
        q = "SELECT user_id FROM user_tbl;"
        data = exec(q).fetchall()
        addUserHelper(username,password,data)
        return True
    return False #if username already exists


#helper function
def verifyUserHelper(username, password, data):
    myEntry = (username, password)
    #print(myEntry)
    if (myEntry in data):
        return True
    return False


#verifyUser
def verifyUser(username, password):
    q = "SELECT username,password FROM user_tbl;"
    data = exec(q).fetchall()
    return verifyUserHelper(username,password,data)

#==========================user get methods===========================

#getUserID
def getUserID(username):
    q = "SELECT user_id FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    return data


#getUserIDStr for str instead of tuple output
def getUserIDStr(username):
    user_id = getUserID(username)
    return str(user_id[0])


#getUserInfo
def getUserInfo(user_id):
    q = "SELECT username FROM user_tbl WHERE user_id = '%s';" % user_id
    data = exec(q).fetchone()
    return data

#==========================user tests===========================

##addUser - doesn't matter if commented out because checks if user already exists
#addUser("Elizabeth","wow")
#addUser("Emily","this")
#addUser("Jackie","actually")
#addUser("Yaru","works")

#==========================blog functions===========================

#joins user_id for user_tbl and blog_tbl
#command="SELECT user_tbl.user_id FROM user_tbl LEFT JOIN blog_tbl ON user_tbl.user_id = blog_tbl.user_id"
#exec(command)


#helper function
def addBlogHelper(user_id, title, data):
    rand = random.randrange(limit)
    while (rand in data):
        rand = random.randrange(limit)
    #print(rand)
    #print(command)
    command = "INSERT INTO blog_tbl VALUES(%s, %s, '%s')" % (rand, user_id, title)
    #print(command)
    exec(command)
    return rand;


#addBlog
def addBlog(user_id, title):
    user_id = int(user_id)
    q = "SELECT * FROM blog_tbl WHERE user_id = %d AND title = '%s'" % (user_id, title)
    data = exec(q).fetchone()
    if (data is not None):
        return None
    q = "SELECT blog_id FROM blog_tbl WHERE user_id = %d;" % user_id
    data = exec(q).fetchall()
    return addBlogHelper(user_id, title, data)

#==========================blog get methods===========================

#getBlogID
def getBlogID(username, title):
    user_id = getUserIDStr(username)
    q = "SELECT blog_id FROM blog_tbl WHERE user_id =" + user_id + " AND title=" + title + ";"
    data = exec(q).fetchone()
    return data


#getBlogIDStr for str instead of tuple output
def getBlogIDStr(username, title):
    blog_id = getBlogID(username, title)
    return str(user_id[0])


#getBlogTitle
def getBlogTitle(blog_id):
    q = "SELECT title FROM blog_tbl WHERE blog_id ='%s';" % blog_id
    data = exec(q).fetchone()
    return data

#getBlogTitleStr for str instead of tuple output
def getBlogTitleStr(blog_id):
    title = getBlogTitle(blog_id)
    if (title is None):
        return ""
    return str(title[0])

#getUserfromBlog
def getUserfromBlog(blog_id):
    q = "SELECT user_id FROM blog_tbl WHERE blog_id = '%s'" % blog_id
    data = exec(q).fetchone()
    return data

#getUserfromBlogStr for str instead of tuple output
def getUserfromBlogStr(blog_id):
    user = getUserfromBlog(blog_id)
    return str(user[0])

#getUserBlogs
def getUserBlogs(user_id):
    q = "SELECT title, blog_id FROM blog_tbl WHERE user_id= '%s'" % user_id
    data = exec(q).fetchall()
    return data
#==========================blog tests===========================

##addBlog
#addBlog(1311963876, "Dogs")
#addBlog(2039603925, "Lions")
#addBlog(526656026, "Turtle")
#addBlog(389070385, "LionCity")
#addBlog(2039603925, "Greatest Lion")


#==========================entry functions===========================

#joins blog_id for blog_tbl and entry_tbl
#command="SELECT blog_tbl.blog_id FROM blog_tbl LEFT JOIN entry_tbl ON blog_tbl.blog_id = entry_tbl.blog_id"
#exec(command)

#addEntryHelper
def addEntryHelper(blog_id, title, content, data):
    rand = random.randrange(limit)
    while (rand in data):
        rand = random.randrange(limit)
    command = "INSERT INTO entry_tbl VALUES(%s, %s, '%s', '%s')" % (rand, blog_id, title, content)
    #print(command)
    return exec(command)

#addEntry
def addEntry(blog_id, title, content):
    blog_id = int(blog_id)
    q = "SELECT * FROM entry_tbl WHERE blog_id = %d AND title='%s'" % (blog_id, title)
    data = exec(q).fetchone()
    if (data is not None):
        return None
    q = "SELECT blog_id FROM blog_tbl"
    data = exec(q).fetchall()
    return addEntryHelper(blog_id, title, content, data);

def editEntry(entry_id, title, content):
    entry_id = int(entry_id)
    q = "SELECT * FROM entry_tbl WHERE title='%s' AND entry_id != %d" % (title, entry_id)
    data = exec(q).fetchall()
    #print(len(data))
    if (len(data) > 0):
        return False
    q = "UPDATE entry_tbl SET title = '%s', content = '%s' WHERE entry_id = %d" % (title, content, entry_id)
    exec(q)
    return True


#==========================entry get methods===========================

#getEntryID
def getEntryID(blog_id, title):
    q = "SELECT entry_id FROM entry_tbl WHERE blog_id ='%s' AND title='%s';" % (blog_id, title)
    data = exec(q).fetchone()
    return data

#getEntryIDStr for str instead of tuple output
def getEntryIDStr(blog_id, title):
    entry_id = getEntryID(blog_id, title)
    return str(user_id[0])

#getEntryTitle
def getEntryTitle(entry_id):
    q = "SELECT title FROM entry_tbl WHERE entry_id ='%s';" % entry_id
    data = exec(q).fetchone()
    if (data is None):
        return ""
    return str(data[0])

#getEntryContent
def getEntryContent(entry_id):
    q = "SELECT content FROM entry_tbl WHERE entry_id ='%s';" % entry_id
    data = exec(q).fetchone()
    if (data is None):
        return ""
    return str(data[0])

#getAllEntries
def getAllEntries(blog_id):
    q = "SELECT title, content, entry_id FROM entry_tbl WHERE blog_id= '%s'" % blog_id
    data = exec(q).fetchall()
    return data

def getBlogfromEntry(entry_id):
    q = "SELECT blog_id FROM entry_tbl WHERE entry_id = '%s'" % entry_id
    data = exec(q).fetchone()
    return str(data[0])

#==========================entry tests===========================

##addEntry
#addEntry(230029172, "Dogs wow!", "Dogs are really cute!")
#addEntry(1216538388, "Lions > all", "Lions are really fierce!")

#==========================search function===========================

#getAllBlogs
def getAllBlogs():
    q = "SELECT title FROM blog_tbl"
    data = exec(q).fetchall()
    return data

#findBlog
def findBlog(search):
    search = search.lower()
    data = getAllBlogs()
    blogsList = []
    for blogT in data:
        title = str(blogT[0])
        titleSmall = title.lower()
        if search in titleSmall:
            blogsList.append(title)
            #print(blogsList)
    blogIDList = []
    for goodTitles in blogsList:
        q = "SELECT blog_id, title, user_id FROM blog_tbl WHERE title='%s'" % goodTitles
        data = exec(q).fetchone()
        data = data + getUserInfo(getUserfromBlog(str(data[0])))
        blogIDList.append(data)

    return blogIDList   #list of tuples

#findBlogStr for list of str not list of tuples
def findBlogStr(search):
    blogIDList = findBlog(search)
    strBlogIDS = []
    for blog_ids in blogIDList:
        newID = str(blog_ids[0])
        strBlogIDS.append(newID)
    return strBlogIDS

#search test
#print(findBlogStr("LION"))
#search test
#print(findBlog("LION"))
