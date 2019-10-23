#Team Bits Please
#SoftDev 1 pd1
#P00 -- Da Art of Storytellin'
#2019-10-28

import sqlite3
import random
import sys

db = sqlite3.connect('blog.db')
c = db.cursor()

#for creating randomly generated id numbers
limit = sys.maxsize

#helper function
def addUserHelper(username, password, data):
    rand = random.randrange(limit)
    while (rand in data):
        rand = random.randrange(limit)
    #print(rand)
    command = "INSERT INTO user_tbl VALUES(" + str(rand) + ",\"" + username + "\",\"" + password + "\")"
    #print(command)
    c.execute(command)

#addUser
def addUser(username, password):
    q = "SELECT user_id FROM user_tbl;"
    data = c.execute(q).fetchall()
    addUserHelper(username,password,data)

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
    data = c.execute(q).fetchall()
    return verifyUserHelper(username,password,data)

#addUser tests
addUser("Elizabeth","wow")
addUser("Emily","this")
addUser("Jackie","actually")
addUser("Yaru","works")

#verifyUser tests: TTTFF
print(verifyUser("Elizabeth","wow"))
print(verifyUser("Emily","this"))
print(verifyUser("Elizabeth","wow"))
print(verifyUser("Elizabeth","wo"))
print(verifyUser("Elizbeth","wow"))


#commit changes
db.commit()
db.close()
