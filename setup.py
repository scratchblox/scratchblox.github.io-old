import sqlite3

con = sqlite3.connect("primary.db")
cursor = con.cursor()

cursor.execute('''
	CREATE TABLE user(
	id INT PRIMARY KEY,
	username TEXT,
	password TEXT,
	token TEXT,
	rank INT
	)
	''')

con.commit()