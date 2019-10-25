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
    q = "SELECT * FROM user_tbl where username = '%s';" % username
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
    q = "SELECT user_id FROM user_tbl where username = '%s';" % username
    data = exec(q).fetchone()
    return data


#getUserIDStr for str instead of tuple output
def getUserIDStr(username):
    user_id = getUserID(username)
    return str(user_id[0])


#getUserInfo
def getUserInfo(user_id):
    q = "SELECT username FROM user_tbl where user_id = '%s';" % user_id
    data = exec(q).fetchone()
    return data

#==========================user tests===========================

#addUser - doesn't matter if commented out because checks if user already exists
#addUser("Elizabeth","wow")
#addUser("Emily","this")
#addUser("Jackie","actually")
#addUser("Yaru","works")


#verifyUser
#print(verifyUser("Elizabeth","wow"))    #True
#print(verifyUser("Elizabeth","wo"))     #False


#getUser
#print(getUserID("Elizabeth"))
#print(getUserIDStr("Emily"))
#print(getUserID("wow"))        #None

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


#addNewBlog
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

#getBlogID, unused
def getBlogID(username, title):
    user_id = getUserIDStr(username)
    q = "SELECT blog_id FROM blog_tbl WHERE user_id =" + user_id + " AND title=" + title + ";"
    data = exec(q).fetchone()
    return data


#getBlogIDStr for str instead of tuple output, unused 
def getBlogIDStr(username, title):
    blog_id = getBlogID(username, title)
    return str(user_id[0])


#getBlogTitle
def getBlogTitle(blog_id):
    q = "SELECT title FROM blog_tbl WHERE blog_id =" + blog_id + ";"
    data = exec(q).fetchone()
    return data

def getUserfromBlog(id):
    id = int(id)
    q = "SELECT user_id FROM blog_tbl where blog_id = %d" % id
    data = exec(q).fetchone()
    return data

def getAllBlogs(user_id):
    user_id = int(user_id)
    q = "SELECT title, blog_id FROM blog_tbl where user_id= %d" % user_id
    data = exec(q).fetchall()
    return data
#==========================blog get methods===========================

##addNewBlog
#addNewBlog("Elizabeth", "Doss", "2019-10-25 04:22")
#addNewBlog("Jackie", "Lin", "2019-10-25 04:58")
#addNewBlog("Yaru", "Luo", "2019-10-25 04:59")
#addNewBlog("Yaru", "Lao", "2019-10-25 05:27")


##updateBlog
#updateBlog("Elizabeth", "Doss", "2019-10-25 05:09")
#updateBlog("Yaru", "Luo", "2019-10-25 05:20")


##DOESN'T WORK
##sqlite3.OperationalError: no such column: Doss
#print(getBlogID("Elizabeth", "Doss"))
#print(getBlogID("Yaru", "Lao"))

#==========================entry functions===========================
