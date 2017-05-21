from peewee import *

from fuzzyweather.fuzzy.db import database as db


class BaseModel(Model):
    class Meta:
        database = db


class BeforeMembership(BaseModel):
    season = CharField()
    variable = CharField()
    value = CharField()
    left = FloatField()
    middle = FloatField()
    right = FloatField()


class AfterMembership(BaseModel):
    variable = CharField()
    value = CharField()
    left = FloatField()
    middle = FloatField()
    right = FloatField()


class Rules(BaseModel):
    rule_num = SmallIntegerField()
    before_variable = CharField()
    before_not = BooleanField()
    before_value = CharField()
    and_field = BooleanField()
    or_field = BooleanField()
    after_variable = CharField(null=True)
    after_not = BooleanField(null=True)
    after_value = CharField(null=True)
