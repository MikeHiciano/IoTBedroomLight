import sqlite3

conn = sqlite3.connect('registry.db')
c = conn.cursor()

c.execute("SELECT * FROM registro")
for row in c.fetchall():
    print(row)