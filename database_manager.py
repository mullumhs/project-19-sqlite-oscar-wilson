import sqlite3

def menu_int(message, choices):
    while True:
        try:    
            choice = int(input(message))
            if choice in choices:
                return choice
            else:
                raise Exception
        except:
            print("Error! Invalid Choice!")

def get_rating(message):
    while True:
        try:
            num = float(input(message).strip())
            if num >= 0 and num <= 10:
                return num
            else:
                raise Exception
        except:
            print("Error! Enter a rating between 0-10!")

def get_int(message):
    while True:
        try:
            num = int(input(message).strip())
            return num
        except:
            print("Error! Enter a whole number!")

def create_connection():
    # Create a connection to my_movies.db
    conn = sqlite3.connect("my_movies.db")
    return conn

def create_table(conn):
    # Create the movies table
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            rating FLOAT,
            genre TEXT
    )
    """)

    conn.commit()

def add_movie(conn, title, director, year, rating, genre):
    # Insert a new movie into the database
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO my_movies (title, director, year, rating, genre)
    VALUES (?, ?, ?, ?, ?)
    """, (title, director, year, rating, genre))

    conn.commit()

def display_all_movies(conn):
    # Select all movies
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM my_movies
    """)

    selected_movies = cursor.fetchall()

    # Display all movies
    print("My Movies:")
    for movie in selected_movies:
        print(f"ID: {movie[0]} - {movie[1]}\n\t-\tDirector(s): {movie[2]}\n\t-\tYear: {movie[3]}\n\t-\tRating: {movie[4]}/10\n\t-\tGenre: {movie[5]}".expandtabs(2))

def update_movie_rating(conn, title):
    # Select movie id by title
    cursor = conn.cursor()
    
    try:
        selected_id = select_id_by_title(conn, title)
    except:
        return

    # Get new rating
    new_rating = get_rating("Enter new rating (0-10): ")

    # Update based on selected movie id
    cursor.execute(f"""
    UPDATE my_movies SET rating = {new_rating} WHERE id = {selected_id}
    """)

    conn.commit()

def delete_movie(conn, title):
    # ------------- Delete a specified movie from the database
    # Select movies by title
    cursor = conn.cursor()
    
    try:
        selected_id = select_id_by_title(conn, title)
    except:
        return
    
    # Delete based on selected movie id
    cursor.execute(f"""
    DELETE FROM my_movies WHERE id = {id}
    """)

    conn.commit()

def find_movies_by_director(conn, director):
    # Select movies by director
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT * FROM my_movies WHERE director = "{director}"
    """)

    selected_movies = cursor.fetchall()

    # Display all movies by director
    print(f"Movies by {director}:")
    for movie in selected_movies:
        print(f"ID: {movie[0]} - {movie[1]}\n\t-\tDirector(s): {movie[2]}\n\t-\tYear: {movie[3]}\n\t-\tRating: {movie[4]}/10\n\t-\tGenre: {movie[5]}".expandtabs(2))

def select_id_by_title(conn, title):
    # Select movie id by title
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT * FROM my_movies WHERE title = "{title}"
    """)

    selected_movies = cursor.fetchall()

    # Check if only one movie is selected
    if len(selected_movies) == 1:
        selected_id = selected_movies[0][0]
        return selected_id

    elif len(selected_movies) > 1:
        # Get a list of all the ids that have been selected
        id_choices = [movie[0] for movie in selected_movies]

        # Display all of the selected movies
        print(f"Movies named {title}:")
        for movie in selected_movies:
            print(f"ID: {movie[0]} - {movie[1]}\n\t-\tDirector(s): {movie[2]}\n\t-\tYear: {movie[3]}\n\t-\tRating: {movie[4]}/10\n\t-\tGenre: {movie[5]}".expandtabs(2))
        print()

        selected_id = menu_int(message=f"Select the correct movie ID and enter your choice: ", choices=id_choices)
        return selected_id

    elif len(selected_movies) == 0:
        print(f"Error! No movies titled {title}")
        raise Exception
    
    else: # This should never happen?
        print(len(selected_movies))
        print(selected_movies)
        raise Exception

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        
        while True:
            print("\n--- Movie Database Manager ---")
            print("1. Add a new movie")
            print("2. Display all movies")
            print("3. Update a movie's rating")
            print("4. Delete a movie")
            print("5. Find movies by director")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            print()
            
            if choice == '1':
                title = input("Enter movie title: ").strip()
                director = input("Enter director name: ").strip()
                year = get_int("Enter release year: ")
                rating = get_rating("Enter rating (0-10): ")
                genre = input("Enter movie genre: ").title().strip()
                add_movie(conn, title, director, year, rating, genre)
                print("Movie added successfully!")
            
            elif choice == '2':
                display_all_movies(conn)
            
            elif choice == '3':
                title = input("Enter movie title to update: ")
                update_movie_rating(conn, title)
                print("Rating updated successfully!")
            
            elif choice == '4':
                title = input("Enter movie title to delete: ")
                delete_movie(conn, title)
                print("Movie deleted successfully!")
            
            elif choice == '5':
                director = input("Enter director name: ")
                find_movies_by_director(conn, director)
            
            elif choice == '6':
                print("Thank you for using Movie Database Manager. Goodbye!\n")
                break
            
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to Continue: ")

        conn.close()
        
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()