from models import *

movie_data = open("data/movies.csv", "r")
ratings_data = open("data/ratings.csv", "r")

# parse genres list and add to DB
def genres_to_db():
    genres_list = []
    for row in movie_data:
        genres = row.split(',')[-1].rstrip()
        if genres != 'genres' and genres != '(no genres listed)':
            for genre in genres.split('|'):
                if genre not in genres_list:
                    genres_list.append(genre)
                    g = Genres(name=genre)
                    g.save()

# parse movies list and add to DB. Used many to many relation for movies and genres
def movies_to_db():
    for row in movie_data:
        title = row.split(',')
        genres = title.pop().rstrip()
        title.pop(0)
        title = ''.join(title)
        if title != 'title':
            movie = Movies(title=title)
            movie.save()
            if genres != 'genres' and genres != '(no genres listed)':
                for g in genres.split('|'):
                    genre = Genres.get(Genres.name == g)
                    movie_to_genre = MoviesToGenres(movie_id=movie.id, genre_id=genre.id)
                    movie_to_genre.save(force_insert=True)

# # parse ratings list and add to DB
def ratings_to_db():
    for row in ratings_data:
        if row.split(',')[0] != 'userId':
            user_id = int(row.split(',')[0])
            movie_id = int(row.split(',')[1])
            rating = float(row.split(',')[2])
            timestamp = int(row.split(',')[3])
            rating = Ratings(user_id=user_id, movie_id=movie_id, rating=rating, timestamp=timestamp)
            rating.save()

# add users
def add_users():
    last_user_id = Ratings.get(id=Ratings.select().count()).user_id
    for i in range(1, last_user_id + 1):
        user = Users()
        user.save()


if __name__ == '__main__':
    movies_to_db()