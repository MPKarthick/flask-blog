import sqlite3

with sqlite3.connect("blog.db") as connection:
    c = connection.cursor()

    c.execute("""create table posts
    (title TEXT, post TEXT)""")

    c.execute('INSERT INTO posts VALUES("Good", "I\'m  good.")')
    c.execute('INSERT INTO posts VALUES("well", "I\'m  well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m  Excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m  Okay.")')