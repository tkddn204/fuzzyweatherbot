from peewee import Model, CharField, FloatField,\
                   SmallIntegerField, TextField

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
    text = TextField()
    emoticon = CharField()


class Rules(BaseModel):
    rule_num = SmallIntegerField()
    before_variable = CharField()
    before_not = SmallIntegerField(default=0)
    before_value = CharField()
    and_field = SmallIntegerField(default=0)
    or_field = SmallIntegerField(default=0)
    after_variable = CharField(null=True)
    after_not = SmallIntegerField(null=True)
    after_value = CharField(null=True)
