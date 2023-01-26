from peewee import fn
from statistics import fmean
from models import *


# 1. For each user, find the total number of ratings provided.
def total_number_of_ratings():
    users = Users.select()
    for user in users:
        ratings = Ratings.select().where(Ratings.user_id == user)
        print(f"User {user} has {ratings.count()} ratings")


# 2. How many movies have an average user ranked?
def rating_by_average_user():
    ratings_count = Ratings.select().count()
    users_count = Users.select().count()
    average_ratings_by_user = round(ratings_count / users_count, 1)
    print(f"Average user have ranked {average_ratings_by_user} movies")


# 3. For each user, find the minimum, maximum, and average rating he provided
def rating_by_user():
    users = Users.select()
    for user in users:
        ratings = Ratings.select().where(Ratings.user_id == user)
        min_rating = ratings.order_by(Ratings.rating).first().rating
        max_rating = ratings.order_by(Ratings.rating.desc()).first().rating
        average_rating = ratings.select(fn.AVG(Ratings.rating)).scalar()
        print(f"User's {user} minimum rating {min_rating}, maximum rating {max_rating}, average rating {average_rating}")


# 4. Find the top 10 movies by average rating
def top_movies_by_rating():
    movies = Movies.select()
    top_movies = []
    for movie in movies:
        # add counter log
        if movie.id % 10 == 0:
            print(f"{movie.id} has been checked")

        # get average reting for movie
        ratings = Ratings.select().where(Ratings.movie_id == movie)
        if ratings.count() != 0:
            average_rating = ratings.select(fn.AVG(Ratings.rating)).scalar()

            # if rating of movie higher than rating of any movie in list program replace movie with lower rate to
            # movie with higher rate
            if len(top_movies) < 10:
                top_movies.append({
                    'title': movie.title,
                    'average_rating': average_rating
                })
            else:
                lowest_rating = 5
                lowest_rating_index = 0
                for i, m in enumerate(top_movies):
                    if m['average_rating'] < lowest_rating:
                        lowest_rating = m['average_rating']
                        lowest_rating_index = i
                if average_rating > lowest_rating:
                    top_movies.pop(lowest_rating_index)
                    top_movies.append({
                        'title': movie.title,
                        'average_rating': average_rating
                    })
                    print(f"{movie.title} with rating {average_rating} added to top list")
    return top_movies

# 5. Provide a list of genre preferences for each user.
# It should be a dataset with the following structure:
# ● userId
# ● genre name
# ● number of ratings
# ● average rating

def preferences_for_each_user():
    users = Users.select()
    for user in users:
        genre_preferences_list = []

        # create empty list for ratings for genres data
        genres_count = Genres.select().count()
        ratings_data = {}
        for i in range(1, genres_count + 1):
            ratings_data[i] = []

        # select all user's ratings by genres
        ratings = Ratings.select().where(Ratings.user_id == user)
        for rating in ratings:
            movie_id = rating.movie_id
            genres = MoviesToGenres.select().where(MoviesToGenres.movie_id == movie_id)
            for g in genres:
                ratings_data[g.genre_id].append(rating.rating)

        # create list of genre preferences for each user
        for genre_id, ratings_list in ratings_data.items():
            if len(ratings_list) != 0:
                genre_preferences = {
                    'user_id': user.id,
                    'genre_name': Genres.get(Genres.id == genre_id).name,
                    'number of ratings': len(ratings_list),
                    'average_rating': round(fmean(ratings_list), 1)
                }
                genre_preferences_list.append(genre_preferences)
        print(genre_preferences_list)


if __name__ == '__main__':
    # total_number_of_ratings()
    # rating_by_average_user()
    # rating_by_user()
    # top_movies_by_rating()
    preferences_for_each_user()

