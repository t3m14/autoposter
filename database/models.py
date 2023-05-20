from peewee import SqliteDatabase, Model, _StringField, IntegerField

db = SqliteDatabase("posts.db")

class Post(Model):
    username = _StringField(null=False)
    message_id = IntegerField(null=False, unique=True)
    class Meta:
        database = db