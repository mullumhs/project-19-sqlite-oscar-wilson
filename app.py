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

cursor.execute("""
ALTER TABLE movies ADD COLUMN genre TEXT               
""")
conn.commit()

# -------------------------------------------------------- Inserting Stuff --------------------------------------------------------
# Insert Mean Girls (2004)
cursor.execute("""
INSERT INTO movies (title, director, year, rating)
VALUES (?, ?, ?, ?)    
""", ('Mean Girls', 'Mark Waters', 2004, 7.1))

# Insert multiple musicals
musicals = [
    ('Mean Girls', 'Samantha Jayne, Arturo Perez Jr', 2024, 5.5),
    ('Wicked: Part 1', 'Jon M. Chu', 2024, 7.4),
    ('Frozen', 'Chris Buck, Jennifer Lee', 2013, 7.4),
    ('Little Shop of Horrors', 'Frank Oz', 1986, 7.1)
]

cursor.executemany("""
INSERT INTO movies (title, director, year, rating)
VALUES (?, ?, ?, ?)
""", musicals)

# -------------------------------------------------------- Selecting Stuff --------------------------------------------------------
conn.commit()

# View all of the movies (because the SQLite viewer extension doesn't work)
cursor.execute('''
SELECT * FROM movies;               
''')
all_movies = cursor.fetchall()
print("Selected Movies:")
for item in all_movies:
    print(f"\t{item}")

# View all of the musicals (can't do that until I add a genre!)

# -------------------------------------------------------- Finishing Stuff --------------------------------------------------------
# Commit the changes and close the connection
conn.close()