import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample User-Item Rating Matrix
ratings_dict = {
    'User': ['User1', 'User1', 'User2', 'User2', 'User3', 'User3', 'User4'],
    'Movie': ['Matrix', 'Inception', 'Matrix', 'Avatar', 'Inception', 'Avatar', 'Matrix'],
    'Rating': [5, 4, 4, 5, 3, 4, 5]
}
df = pd.DataFrame(ratings_dict)

# Create a pivot table
user_movie_matrix = df.pivot_table(index='User', columns='Movie', values='Rating').fillna(0)

# Calculate Cosine Similarity between users
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

print("User-User Similarity Matrix:")
print(user_similarity_df)

# Example: Suggest finding users similar to User1 to recommend unrated movies
print("\nUsers most similar to User1:")
print(user_similarity_df['User1'].sort_values(ascending=False)[1:])