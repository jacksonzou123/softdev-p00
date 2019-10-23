#Team Bits Please
#SoftDev 1 pd1 
#P00 -- Da Art of Storytellin'
#2019-10-28

import sqlite3   #enable control of an sqlite database

DB_FILE="blog.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

#==========================================================
command = "CREATE TABLE IF NOT EXISTS user_tbl (user_id INT, username TEXT, password TEXT)"
c.execute(command)    # run SQL statement

######################
command = "CREATE TABLE IF NOT EXISTS blog_tbl (blog_id INT, user_id INT, title TEXT, time_created TEXT, time_updated TEXT)"
c.execute(command)    # run SQL statement


######################
command = "CREATE TABLE IF NOT EXISTS entry_tbl (entry_id INT, blog_id INT, title TEXT, content TEXT, time_created TEXT, time_updated TEXT)"
c.execute(command)    # run SQL statement

db.commit() #save changes
db.close()  #close database

