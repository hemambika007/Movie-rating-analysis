import sqlite3
import pandas as pd

class MovieAnalytics:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def genre_popularity_analysis(self):
        """Analyze genre popularity over time"""
        query = """
        SELECT 
            genre,
            strftime('%Y', release_date) as release_year,
            COUNT(*) as movie_count,
            AVG(mr.avg_rating) as avg_genre_rating,
            SUM(box_office) as total_box_office
        FROM movies m
        JOIN (
            SELECT 
                movie_id, 
                AVG(rating) as avg_rating
            FROM movie_ratings 
            GROUP BY movie_id
        ) mr ON m.movie_id = mr.movie_id
        GROUP BY genre, release_year
        ORDER BY release_year, movie_count DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def director_performance_metrics(self):
        """Analyze director performance metrics"""
        query = """
        SELECT 
            d.name as director_name,
            COUNT(m.movie_id) as total_movies,
            AVG(mr.avg_rating) as avg_director_rating,
            AVG(m.box_office) as avg_box_office,
            SUM(m.box_office) as total_box_office,
            AVG(m.box_office - m.budget) as avg_profit,
            MIN(m.release_date) as first_movie,
            MAX(m.release_date) as latest_movie
        FROM directors d
        JOIN movies m ON d.director_id = m.director_id
        JOIN (
            SELECT 
                movie_id, 
                AVG(rating) as avg_rating,
                COUNT(rating) as rating_count
            FROM movie_ratings 
            GROUP BY movie_id
        ) mr ON m.movie_id = mr.movie_id
        GROUP BY d.director_id, d.name
        HAVING COUNT(m.movie_id) >= 2
        ORDER BY avg_director_rating DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def rating_distribution_analysis(self):
        """Analyze rating distributions by various factors"""
        query = """
        SELECT 
            m.title,
            m.genre,
            strftime('%Y', m.release_date) as release_year,
            d.name as director,
            AVG(mr.rating) as avg_rating,
            COUNT(mr.rating) as total_ratings,
            MIN(mr.rating) as min_rating,
            MAX(mr.rating) as max_rating,
            (m.box_office - m.budget) as profit,
            CASE 
                WHEN AVG(mr.rating) >= 8.0 THEN 'Excellent'
                WHEN AVG(mr.rating) >= 7.0 THEN 'Good'
                WHEN AVG(mr.rating) >= 6.0 THEN 'Average'
                ELSE 'Poor'
            END as rating_category
        FROM movies m
        JOIN directors d ON m.director_id = d.director_id
        JOIN movie_ratings mr ON m.movie_id = mr.movie_id
        GROUP BY m.movie_id, m.title, m.genre, release_year, d.name, profit
        ORDER BY avg_rating DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def actor_collaboration_network(self):
        """Analyze actor collaboration patterns"""
        query = """
        SELECT 
            a1.name as actor1,
            a2.name as actor2,
            COUNT(*) as collaborations,
            AVG(mr.avg_rating) as avg_collab_rating,
            GROUP_CONCAT(m.title, ', ') as movies_together
        FROM movie_actors ma1
        JOIN movie_actors ma2 ON ma1.movie_id = ma2.movie_id AND ma1.actor_id < ma2.actor_id
        JOIN actors a1 ON ma1.actor_id = a1.actor_id
        JOIN actors a2 ON ma2.actor_id = a2.actor_id
        JOIN movies m ON ma1.movie_id = m.movie_id
        JOIN (
            SELECT 
                movie_id, 
                AVG(rating) as avg_rating
            FROM movie_ratings 
            GROUP BY movie_id
        ) mr ON m.movie_id = mr.movie_id
        GROUP BY a1.actor_id, a2.actor_id, a1.name, a2.name
        HAVING COUNT(*) >= 2
        ORDER BY collaborations DESC, avg_collab_rating DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def seasonal_release_patterns(self):
        """Analyze seasonal movie release patterns"""
        query = """
        SELECT 
            CASE 
                WHEN CAST(strftime('%m', release_date) AS INTEGER) IN (12, 1, 2) THEN 'Winter'
                WHEN CAST(strftime('%m', release_date) AS INTEGER) IN (3, 4, 5) THEN 'Spring'
                WHEN CAST(strftime('%m', release_date) AS INTEGER) IN (6, 7, 8) THEN 'Summer'
                ELSE 'Fall'
            END as season,
            genre,
            COUNT(*) as movie_count,
            AVG(mr.avg_rating) as avg_rating,
            AVG(box_office) as avg_box_office,
            AVG(box_office - budget) as avg_profit
        FROM movies m
        JOIN (
            SELECT 
                movie_id, 
                AVG(rating) as avg_rating
            FROM movie_ratings 
            GROUP BY movie_id
        ) mr ON m.movie_id = mr.movie_id
        GROUP BY season, genre
        ORDER BY season, avg_rating DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def budget_vs_rating_correlation(self):
        """Analyze correlation between budget and ratings"""
        query = """
        SELECT 
            m.title,
            m.budget,
            m.box_office,
            (m.box_office - m.budget) as profit,
            AVG(mr.rating) as avg_rating,
            COUNT(mr.rating) as rating_count,
            CASE 
                WHEN m.budget < 20000000 THEN 'Low Budget'
                WHEN m.budget < 100000000 THEN 'Medium Budget'
                ELSE 'High Budget'
            END as budget_category
        FROM movies m
        JOIN movie_ratings mr ON m.movie_id = mr.movie_id
        GROUP BY m.movie_id, m.title, m.budget, m.box_office
        ORDER BY m.budget DESC
        """
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

if __name__ == "__main__":
    analytics = MovieAnalytics()
    
    print("Running sample queries...")
    
    # Test each analysis
    print("\n1. Genre Popularity Analysis:")
    genre_data = analytics.genre_popularity_analysis()
    print(genre_data.head())
    
    print("\n2. Director Performance:")
    director_data = analytics.director_performance_metrics()
    print(director_data.head())
    
    print("\n3. Rating Distribution:")
    rating_data = analytics.rating_distribution_analysis()
    print(rating_data.head())