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
    rating FLOAT,
    genre TEXT
)
''')

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

# 
director = input("Enter director: ")

cursor.execute(f"""
SELECT * FROM movies WHERE director = "{director}"
""")

selected_movies = cursor.fetchall()

# Display all movies by director
print(f"Movies by {director}:")
for movie in selected_movies:
    print(f"ID: {movie[0]} - {movie[1]}\n\t-\tDirector(s): {movie[2]}\n\t-\tYear: {movie[3]}\n\t-\tRating: {movie[4]}/10\n\t-\tGenre: {movie[5]}".expandtabs(2))
print()

# -------------------------------------------------------- Finishing Stuff --------------------------------------------------------
# Commit the changes and close the connection
conn.close()