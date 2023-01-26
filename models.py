import peewee
from peewee import Model


def db_name():
    return peewee.SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db_name()

class Genres(BaseModel):
    class Meta:
        table_name = "Genres"
    name = peewee.CharField(unique=True, max_length=50)


class Movies(BaseModel):
    class Meta:
        table_name = "Movies"
    title = peewee.CharField(max_length=30)
    genres = peewee.ManyToManyField(Genres, backref='movies')

class MoviesToGenres(BaseModel):
    movie = peewee.ForeignKeyField(Movies)
    genre = peewee.ForeignKeyField(Genres)

    class Meta:
        primary_key = peewee.CompositeKey('movie', 'genre')
        table_name = "MoviesToGenres"


class Users(BaseModel):
    class Meta:
        table_name = "Users"


class Ratings(BaseModel):
    class Meta:
        table_name = 'Ratings'
    user = peewee.ForeignKeyField(Users, field='id')
    movie = peewee.ForeignKeyField(Movies, field='id')
    rating = peewee.FloatField()
    timestamp = peewee.TimestampField()


def init_db():
    db = db_name()
    db.drop_tables([Genres, Movies, MoviesToGenres, Users, Ratings], safe=True)
    db.create_tables([Genres, Movies, MoviesToGenres, Users, Ratings], safe=True)

if __name__ == "__main__":
    init_db()

