import pandas as pd
from analysis_queries import MovieAnalytics
import sqlite3

class ReportGenerator:
    def __init__(self):
        self.analytics = MovieAnalytics()
        
    def generate_html_report(self):
        """Generate comprehensive HTML report with findings"""
        
        # Get all analysis data
        genre_data = self.analytics.genre_popularity_analysis()
        director_data = self.analytics.director_performance_metrics()
        rating_data = self.analytics.rating_distribution_analysis()
        collab_data = self.analytics.actor_collaboration_network()
        seasonal_data = self.analytics.seasonal_release_patterns()
        budget_data = self.analytics.budget_vs_rating_correlation()
        
        # Calculate key insights
        total_movies = len(rating_data)
        avg_rating = rating_data['avg_rating'].mean()
        top_genre = genre_data.groupby('genre')['movie_count'].sum().idxmax()
        best_director = director_data.loc[director_data['avg_director_rating'].idxmax(), 'director_name']
        most_profitable_movie = rating_data.loc[rating_data['profit'].idxmax(), 'title']
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Movie Rating Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                    margin-top: 30px;
                }}
                .summary-stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    display: block;
                }}
                .stat-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: white;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .insight-box {{
                    background-color: #e8f4fd;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 5px;
                }}
                .chart-placeholder {{
                    background-color: #ecf0f1;
                    height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 20px 0;
                    border-radius: 5px;
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 Movie Rating Analysis Report</h1>
                
                <div class="summary-stats">
                    <div class="stat-card">
                        <span class="stat-number">{total_movies}</span>
                        <span class="stat-label">Total Movies Analyzed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{avg_rating:.1f}</span>
                        <span class="stat-label">Average Rating</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{top_genre}</span>
                        <span class="stat-label">Most Popular Genre</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{len(director_data)}</span>
                        <span class="stat-label">Directors Analyzed</span>
                    </div>
                </div>

                <h2>📊 Key Insights</h2>
                <div class="insight-box">
                    <strong>🏆 Top Performer:</strong> {best_director} has the highest average rating among directors with multiple films.
                </div>
                <div class="insight-box">
                    <strong>💰 Most Profitable:</strong> "{most_profitable_movie}" generated the highest profit in our dataset.
                </div>
                <div class="insight-box">
                    <strong>🎭 Genre Leader:</strong> {top_genre} is the most frequently produced genre in our analysis.
                </div>

                <h2>🎯 Director Performance Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Director</th>
                            <th>Movies</th>
                            <th>Avg Rating</th>
                            <th>Avg Box Office</th>
                            <th>Total Box Office</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add top directors to table
        top_directors = director_data.nlargest(10, 'avg_director_rating')
        for _, director in top_directors.iterrows():
            html_content += f"""
                        <tr>
                            <td>{director['director_name']}</td>
                            <td>{director['total_movies']}</td>
                            <td>{director['avg_director_rating']:.1f}</td>
                            <td>${director['avg_box_office']:,.0f}</td>
                            <td>${director['total_box_office']:,.0f}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>

                <h2>🏅 Top Rated Movies</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Movie</th>
                            <th>Director</th>
                            <th>Genre</th>
                            <th>Year</th>
                            <th>Rating</th>
                            <th>Total Ratings</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add top movies to table
        top_movies = rating_data.nlargest(15, 'avg_rating')
        for _, movie in top_movies.iterrows():
            html_content += f"""
                        <tr>
                            <td>{movie['title']}</td>
                            <td>{movie['director']}</td>
                            <td>{movie['genre']}</td>
                            <td>{movie['release_year']}</td>
                            <td>{movie['avg_rating']:.1f}</td>
                            <td>{movie['total_ratings']}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>

                <h2>🤝 Actor Collaboration Network</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Actor 1</th>
                            <th>Actor 2</th>
                            <th>Collaborations</th>
                            <th>Avg Rating</th>
                            <th>Movies Together</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add collaborations to table
        for _, collab in collab_data.head(10).iterrows():
            html_content += f"""
                        <tr>
                            <td>{collab['actor1']}</td>
                            <td>{collab['actor2']}</td>
                            <td>{collab['collaborations']}</td>
                            <td>{collab['avg_collab_rating']:.1f}</td>
                            <td>{collab['movies_together'][:50]}...</td>
                        </tr>
            """
        
        # Calculate genre insights
        genre_stats = genre_data.groupby('genre').agg({
            'movie_count': 'sum',
            'avg_genre_rating': 'mean',
            'total_box_office': 'sum'
        }).round(2)
        
        html_content += f"""
                    </tbody>
                </table>

                <h2>🎭 Genre Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Genre</th>
                            <th>Total Movies</th>
                            <th>Avg Rating</th>
                            <th>Total Box Office</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for genre, stats in genre_stats.iterrows():
            html_content += f"""
                        <tr>
                            <td>{genre}</td>
                            <td>{stats['movie_count']}</td>
                            <td>{stats['avg_genre_rating']:.1f}</td>
                            <td>${stats['total_box_office']:,.0f}</td>
                        </tr>
            """
        
        # Calculate seasonal insights
        seasonal_stats = seasonal_data.groupby('season').agg({
            'movie_count': 'sum',
            'avg_rating': 'mean',
            'avg_box_office': 'mean'
        }).round(2)
        
        html_content += f"""
                    </tbody>
                </table>

                <h2>🌟 Seasonal Release Patterns</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Season</th>
                            <th>Movies Released</th>
                            <th>Avg Rating</th>
                            <th>Avg Box Office</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for season, stats in seasonal_stats.iterrows():
            html_content += f"""
                        <tr>
                            <td>{season}</td>
                            <td>{stats['movie_count']}</td>
                            <td>{stats['avg_rating']:.1f}</td>
                            <td>${stats['avg_box_office']:,.0f}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>

                <h2>💡 Analysis Methodology</h2>
                <div class="insight-box">
                    <p><strong>Data Source:</strong> SQLite database with synthetic movie data including ratings, box office, cast, and crew information.</p>
                    <p><strong>Analysis Techniques:</strong> SQL aggregations, joins, window functions, and statistical analysis using Python pandas.</p>
                    <p><strong>Key Metrics:</strong> Average ratings, box office performance, profit margins, collaboration patterns, and seasonal trends.</p>
                    <p><strong>Visualizations:</strong> Generated using matplotlib and seaborn for comprehensive data exploration.</p>
                </div>

                <h2>🔍 SQL Queries Used</h2>
                <div class="insight-box">
                    <p>This analysis demonstrates advanced SQL skills including:</p>
                    <ul>
                        <li>Complex JOINs across multiple tables</li>
                        <li>Aggregate functions (AVG, COUNT, SUM, MIN, MAX)</li>
                        <li>Subqueries and CTEs</li>
                        <li>Window functions and ranking</li>
                        <li>Date/time functions</li>
                        <li>CASE statements for categorization</li>
                        <li>GROUP BY with HAVING clauses</li>
                    </ul>
                </div>

                <div style="text-align: center; margin-top: 40px; color: #7f8c8d;">
                    <p>Report generated on """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
                    <p>Movie Rating Analysis Project | Data Analytics Portfolio</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save the report
        with open('movie_analysis_report.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("HTML report generated successfully: movie_analysis_report.html")
        return html_content

if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate_html_report()