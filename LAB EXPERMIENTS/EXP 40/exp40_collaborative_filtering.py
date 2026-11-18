import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample User-Item Rating Matrix
ratings_dict = {
    "User": ["User1", "User1", "User2", "User2", "User3", "User3", "User4"],
    "Movie": ["Matrix", "Inception", "Matrix", "Avatar", "Inception", "Avatar", "Matrix"],
    "Rating": [5, 4, 4, 5, 3, 4, 5]
}
ratings = pd.DataFrame(ratings_dict)

# Create a complete pivot table; ratings are 0 for unrated movies
user_movie_matrix = ratings.pivot_table(
    index="User", columns="Movie", values="Rating", aggfunc="mean"
).fillna(0)

# Calculate user-user cosine similarity
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)

print("User-User Similarity Matrix:")
print(user_similarity_df)

# Recommend unrated movies for User1 using weighted scores from similar users
selected_user = "User1"
if selected_user not in user_movie_matrix.index:
    raise ValueError(f"Unknown user: {selected_user}")

similarities = user_similarity_df[selected_user].drop(index=selected_user)
unrated_mask = user_movie_matrix.loc[selected_user] == 0

weighted_scores = {}
for movie in user_movie_matrix.columns[unrated_mask]:
    weighted_sum = 0.0
    similarity_sum = 0.0

    for similar_user, similarity in similarities.items():
        rating = user_movie_matrix.loc[similar_user, movie]
        if rating > 0:
            weighted_sum += similarity * rating
            similarity_sum += similarity

    if similarity_sum > 0:
        weighted_scores[movie] = weighted_sum / similarity_sum

print(f"\nTop recommended movies for {selected_user}:")
if not weighted_scores:
    print("No unrated movies have enough similar-user ratings.")
else:
    recommendations = sorted(weighted_scores.items(), key=lambda item: item[1], reverse=True)
    for rank, (movie, score) in enumerate(recommendations, start=1):
        print(f"{rank}. {movie} - predicted rating: {score:.2f}")

print(f"\nUsers most similar to {selected_user}:")
print(user_similarity_df[selected_user].sort_values(ascending=False).iloc[1:])
