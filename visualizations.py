import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from analysis_queries import MovieAnalytics

class MovieVisualizations:
    def __init__(self):
        self.analytics = MovieAnalytics()
        # Set style for better-looking plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_genre_popularity_chart(self):
        """Create genre popularity visualization"""
        data = self.analytics.genre_popularity_analysis()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Genre count by year
        genre_pivot = data.pivot_table(values='movie_count', index='release_year', 
                                     columns='genre', fill_value=0)
        genre_pivot.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Movie Count by Genre Over Time')
        ax1.set_xlabel('Release Year')
        ax1.set_ylabel('Number of Movies')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Average rating by genre
        genre_ratings = data.groupby('genre')['avg_genre_rating'].mean().sort_values(ascending=True)
        genre_ratings.plot(kind='barh', ax=ax2, color='skyblue')
        ax2.set_title('Average Rating by Genre')
        ax2.set_xlabel('Average Rating')
        
        plt.tight_layout()
        plt.savefig('genre_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_director_performance_chart(self):
        """Create director performance visualization"""
        data = self.analytics.director_performance_metrics()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Director ratings vs box office
        ax1.scatter(data['avg_director_rating'], data['avg_box_office'], 
                   s=data['total_movies']*50, alpha=0.6)
        ax1.set_xlabel('Average Rating')
        ax1.set_ylabel('Average Box Office ($)')
        ax1.set_title('Director Rating vs Box Office Performance')
        
        # Add director names to points
        for i, row in data.iterrows():
            ax1.annotate(row['director_name'], 
                        (row['avg_director_rating'], row['avg_box_office']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # Top directors by rating
        top_directors = data.nlargest(8, 'avg_director_rating')
        ax2.barh(top_directors['director_name'], top_directors['avg_director_rating'])
        ax2.set_title('Top Directors by Average Rating')
        ax2.set_xlabel('Average Rating')
        
        # Profit analysis
        ax3.bar(top_directors['director_name'], top_directors['avg_profit'])
        ax3.set_title('Average Profit by Top Directors')
        ax3.set_ylabel('Average Profit ($)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Movie count vs rating
        ax4.scatter(data['total_movies'], data['avg_director_rating'], alpha=0.7)
        ax4.set_xlabel('Total Movies Directed')
        ax4.set_ylabel('Average Rating')
        ax4.set_title('Productivity vs Quality')
        
        plt.tight_layout()
        plt.savefig('director_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_rating_distribution_chart(self):
        """Create rating distribution visualization"""
        data = self.analytics.rating_distribution_analysis()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Rating distribution histogram
        ax1.hist(data['avg_rating'], bins=20, alpha=0.7, color='lightblue', edgecolor='black')
        ax1.set_xlabel('Average Rating')
        ax1.set_ylabel('Number of Movies')
        ax1.set_title('Distribution of Movie Ratings')
        ax1.axvline(data['avg_rating'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {data["avg_rating"].mean():.2f}')
        ax1.legend()
        
        # Rating by genre boxplot
        sns.boxplot(data=data, x='genre', y='avg_rating', ax=ax2)
        ax2.set_title('Rating Distribution by Genre')
        ax2.tick_params(axis='x', rotation=45)
        
        # Rating vs profit scatter
        ax3.scatter(data['avg_rating'], data['profit'], alpha=0.6)
        ax3.set_xlabel('Average Rating')
        ax3.set_ylabel('Profit ($)')
        ax3.set_title('Rating vs Profit Correlation')
        
        # Add trend line
        z = np.polyfit(data['avg_rating'], data['profit'], 1)
        p = np.poly1d(z)
        ax3.plot(data['avg_rating'], p(data['avg_rating']), "r--", alpha=0.8)
        
        # Rating categories pie chart
        rating_counts = data['rating_category'].value_counts()
        ax4.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
        ax4.set_title('Movies by Rating Category')
        
        plt.tight_layout()
        plt.savefig('rating_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_seasonal_analysis_chart(self):
        """Create seasonal release pattern visualization"""
        data = self.analytics.seasonal_release_patterns()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Movies by season
        season_counts = data.groupby('season')['movie_count'].sum()
        ax1.pie(season_counts.values, labels=season_counts.index, autopct='%1.1f%%')
        ax1.set_title('Movie Releases by Season')
        
        # Average rating by season
        season_ratings = data.groupby('season')['avg_rating'].mean()
        ax2.bar(season_ratings.index, season_ratings.values, color='lightgreen')
        ax2.set_title('Average Rating by Season')
        ax2.set_ylabel('Average Rating')
        
        # Genre distribution by season
        season_genre = data.pivot_table(values='movie_count', index='season', 
                                      columns='genre', fill_value=0)
        season_genre.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Genre Distribution by Season')
        ax3.set_ylabel('Number of Movies')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Box office by season
        season_boxoffice = data.groupby('season')['avg_box_office'].mean()
        ax4.bar(season_boxoffice.index, season_boxoffice.values, color='orange')
        ax4.set_title('Average Box Office by Season')
        ax4.set_ylabel('Average Box Office ($)')
        
        plt.tight_layout()
        plt.savefig('seasonal_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_budget_analysis_chart(self):
        """Create budget vs performance visualization"""
        data = self.analytics.budget_vs_rating_correlation()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Budget vs Rating scatter
        colors = {'Low Budget': 'green', 'Medium Budget': 'orange', 'High Budget': 'red'}
        for category in data['budget_category'].unique():
            subset = data[data['budget_category'] == category]
            ax1.scatter(subset['budget'], subset['avg_rating'], 
                       label=category, color=colors[category], alpha=0.7)
        
        ax1.set_xlabel('Budget ($)')
        ax1.set_ylabel('Average Rating')
        ax1.set_title('Budget vs Rating')
        ax1.legend()
        ax1.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        
        # Budget categories distribution
        budget_counts = data['budget_category'].value_counts()
        ax2.bar(budget_counts.index, budget_counts.values, color=['green', 'orange', 'red'])
        ax2.set_title('Movies by Budget Category')
        ax2.set_ylabel('Number of Movies')
        
        # ROI analysis
        data['roi'] = (data['box_office'] / data['budget']) * 100
        budget_roi = data.groupby('budget_category')['roi'].mean()
        ax3.bar(budget_roi.index, budget_roi.values, color=['green', 'orange', 'red'])
        ax3.set_title('Average ROI by Budget Category')
        ax3.set_ylabel('ROI (%)')
        
        # Profit vs Rating
        ax4.scatter(data['avg_rating'], data['profit'], alpha=0.6, color='purple')
        ax4.set_xlabel('Average Rating')
        ax4.set_ylabel('Profit ($)')
        ax4.set_title('Rating vs Profit')
        ax4.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        plt.tight_layout()
        plt.savefig('budget_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    viz = MovieVisualizations()
    
    print("Generating visualizations...")
    print("1. Creating genre analysis charts...")
    viz.create_genre_popularity_chart()
    
    print("2. Creating director performance charts...")
    viz.create_director_performance_chart()
    
    print("3. Creating rating distribution charts...")
    viz.create_rating_distribution_chart()
    
    print("4. Creating seasonal analysis charts...")
    viz.create_seasonal_analysis_chart()
    
    print("5. Creating budget analysis charts...")
    viz.create_budget_analysis_chart()
    
    print("All visualizations saved as PNG files!")