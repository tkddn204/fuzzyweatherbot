from peewee import *

from fuzzyweather.fuzzy.db import database as db


class BaseModel(Model):
    class Meta:
        database = db


class MembershipTable(BaseModel):
    season = CharField()
    variable = CharField()
    value = CharField()
    left = FloatField()
    middle = FloatField()
    right = FloatField()
