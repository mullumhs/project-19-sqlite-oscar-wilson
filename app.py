import sqlite3

conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Create the movies table
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    director TEXT,
    year INTEGER,
    rating FLOAT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()