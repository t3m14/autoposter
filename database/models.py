from peewee import SqliteDatabase, Model, _StringField, IntegerField, ForeignKeyField, BooleanField, ManyToManyField

db = SqliteDatabase("app.db")


class BaseModel(Model):
    class Meta:
        database = db


class Post(BaseModel):
    username = _StringField(null=False)
    message_id = IntegerField(null=False, unique=True)




class Config(BaseModel):
    user_id = IntegerField(unique=True)
    public_public_id = _StringField(null=True)
    private_public_id = _StringField(null=True)
    is_subscribed = BooleanField(default=False)


class Source_public(BaseModel):
    source_public_id = _StringField(null=False, unique=True)
    config_id = ForeignKeyField(Config)