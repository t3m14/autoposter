from peewee import SqliteDatabase, Model, _StringField, IntegerField, ForeignKeyField

db = SqliteDatabase("posts.db")


class Post(Model):
    username = _StringField(null=False)
    message_id = IntegerField(null=False, unique=True)

    class Meta:
        database = db


class Config(Model):
    user_id = IntegerField(unique=True)
    public_public = _StringField()
    private_public = _StringField()

    class Meta:
        database = db


class Source_public(Model):
    source_public = _StringField()
    config = ForeignKeyField(Config, backref="source_publics")

    class Meta:
        database = db
