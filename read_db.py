# connect to sqlite database and read the data
import sqlite3

conn = sqlite3.connect('reddit.db')
c = conn.cursor()
# get count of posts
c.execute("SELECT COUNT(*) FROM posts")
print(c.fetchone())
# get the 10 oldest posts
c.execute("SELECT title FROM posts ORDER BY created_utc ASC LIMIT 10")
print(c.fetchall())
# get the 10 newest posts
c.execute("SELECT title FROM posts ORDER BY created_utc DESC LIMIT 10")
print(c.fetchall())