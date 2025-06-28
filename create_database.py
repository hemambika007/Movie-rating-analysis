import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create SQLite database with movie rating data"""
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS movie_ratings')
    cursor.execute('DROP TABLE IF EXISTS movies')
    cursor.execute('DROP TABLE IF EXISTS directors')
    cursor.execute('DROP TABLE IF EXISTS actors')
    cursor.execute('DROP TABLE IF EXISTS movie_actors')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE directors (
            director_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            release_date DATE,
            director_id INTEGER,
            budget INTEGER,
            box_office INTEGER,
            FOREIGN KEY (director_id) REFERENCES directors (director_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE actors (
            actor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE movie_actors (
            movie_id INTEGER,
            actor_id INTEGER,
            role_type TEXT,
            PRIMARY KEY (movie_id, actor_id),
            FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
            FOREIGN KEY (actor_id) REFERENCES actors (actor_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE movie_ratings (
            rating_id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            user_id INTEGER,
            rating REAL CHECK (rating >= 1 AND rating <= 10),
            review_date DATE,
            FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
        )
    ''')
    
    # Insert sample directors
    directors = [
        ('Christopher Nolan', 1970),
        ('Quentin Tarantino', 1963),
        ('Martin Scorsese', 1942),
        ('Steven Spielberg', 1946),
        ('Denis Villeneuve', 1967),
        ('Greta Gerwig', 1983),
        ('Jordan Peele', 1979),
        ('Rian Johnson', 1973),
        ('Chloe Zhao', 1982),
        ('Bong Joon-ho', 1969)
    ]
    
    cursor.executemany('INSERT INTO directors (name, birth_year) VALUES (?, ?)', directors)
    
    # Insert sample actors
    actors = [
        ('Leonardo DiCaprio', 1974),
        ('Margot Robbie', 1990),
        ('Ryan Gosling', 1980),
        ('Emma Stone', 1988),
        ('Christian Bale', 1974),
        ('Scarlett Johansson', 1984),
        ('Oscar Isaac', 1979),
        ('Saoirse Ronan', 1994),
        ('Timothee Chalamet', 1995),
        ('Zendaya', 1996),
        ('Daniel Kaluuya', 1989),
        ('Frances McDormand', 1957),
        ('Adam Driver', 1983),
        ('Florence Pugh', 1996),
        ('Michael Shannon', 1974)
    ]
    
    cursor.executemany('INSERT INTO actors (name, birth_year) VALUES (?, ?)', actors)
    
    # Insert sample movies
    genres = ['Drama', 'Action', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure']
    movies_data = []
    
    movie_titles = [
        'Inception Dreams', 'Pulp Fiction Redux', 'The Departed Soul', 'Saving Private Ryan',
        'Dune Awakening', 'Lady Bird Flies', 'Get Out Now', 'Knives Out Sharp',
        'Nomadland Journey', 'Parasite Rising', 'Interstellar Voyage', 'Django Unchained',
        'The Wolf of Wall Street', 'Schindlers List', 'Arrival Point', 'Little Women',
        'Us Together', 'Glass Onion', 'The Rider', 'Memories of Murder',
        'The Dark Knight', 'Kill Bill Vol. 3', 'Goodfellas', 'E.T. Returns',
        'Blade Runner 2049', 'Barbie World', 'Nope', 'Looper', 'Eternals',
        'Okja', 'Memento', 'Reservoir Dogs', 'Taxi Driver', 'Jaws',
        'Sicario', 'Frances Ha', 'Candyman', 'Star Wars: Last Jedi', 'Songs My Brothers',
        'The Host', 'Tenet', 'Once Upon a Time', 'Casino', 'Munich'
    ]
    
    for i, title in enumerate(movie_titles):
        release_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
        director_id = random.randint(1, 10)
        genre = random.choice(genres)
        budget = random.randint(5000000, 200000000)
        box_office = budget + random.randint(-budget//2, budget*3)
        
        movies_data.append((title, genre, release_date.strftime('%Y-%m-%d'), 
                          director_id, budget, box_office))
    
    cursor.executemany('''
        INSERT INTO movies (title, genre, release_date, director_id, budget, box_office) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', movies_data)
    
    # Insert movie-actor relationships
    movie_actors_data = []
    for movie_id in range(1, len(movie_titles) + 1):
        # Each movie has 2-4 main actors
        num_actors = random.randint(2, 4)
        selected_actors = random.sample(range(1, 16), num_actors)
        
        for actor_id in selected_actors:
            role_type = random.choice(['Lead', 'Supporting', 'Cameo'])
            movie_actors_data.append((movie_id, actor_id, role_type))
    
    cursor.executemany('''
        INSERT INTO movie_actors (movie_id, actor_id, role_type) 
        VALUES (?, ?, ?)
    ''', movie_actors_data)
    
    # Insert movie ratings
    ratings_data = []
    for movie_id in range(1, len(movie_titles) + 1):
        # Each movie gets 50-200 ratings
        num_ratings = random.randint(50, 200)
        
        for _ in range(num_ratings):
            user_id = random.randint(1, 1000)
            # Generate realistic rating distribution (skewed towards higher ratings)
            rating = max(1, min(10, random.normalvariate(7.2, 1.5)))
            rating = round(rating, 1)
            
            review_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
            ratings_data.append((movie_id, user_id, rating, review_date.strftime('%Y-%m-%d')))
    
    cursor.executemany('''
        INSERT INTO movie_ratings (movie_id, user_id, rating, review_date) 
        VALUES (?, ?, ?, ?)
    ''', ratings_data)
    
    conn.commit()
    conn.close()
    print("Database created successfully with sample data!")
    print(f"Created {len(movie_titles)} movies with ratings and cast information")

if __name__ == "__main__":
    create_database()