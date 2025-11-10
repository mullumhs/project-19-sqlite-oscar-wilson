from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('my_movies.db')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    movies = conn.execute('SELECT * FROM my_movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    # On a form submission (POST)
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = int(request.form['year'])
        rating = float(request.form['rating'])
        genre = request.form['genre']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO my_movies (title, director, year, rating, genre) VALUES (?, ?, ?, ?, ?)',
                     (title, director, year, rating, genre))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # On visiting the page (GET)
    return render_template('add.html')

@app.route('/movie/<int:id_num>')
def movie(id_num):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    selected_movie = conn.execute(f'SELECT * FROM my_movies WHERE id = {id_num}').fetchone()
    conn.close()
    return render_template('movie.html', selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)