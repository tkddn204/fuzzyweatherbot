import csv

from fuzzyweather.fuzzy.db import database as db
from fuzzyweather.fuzzy.db.model import BeforeMembership, AfterMembership, Rules


class FuzzyDB:
    def __init__(self):
        db.get_conn()
        db.create_tables([BeforeMembership, AfterMembership, Rules], safe=True)
        if BeforeMembership.select().count() is 0\
                or AfterMembership.select().count() is 0\
                or Rules.select().count() is 0:
            self.__init_db()

    @staticmethod
    def __init_db():
        with open('db/data_csv/before_fuzzyset.csv', 'r', encoding='utf-8') as fb:
            dr = csv.DictReader(fb)
            for row in dr:
                BeforeMembership.create(season=row['\ufeff계절'],
                                        variable=row['언어변수'],
                                        value=row['언어값'],
                                        left=float(row['최저']),
                                        middle=float(row['중간']),
                                        right=float(row['최고']))
        with open('db/data_csv/after_fuzzyset.csv', 'r', encoding='utf-8') as fa:
            dr = csv.DictReader(fa)
            for row in dr:
                AfterMembership.create(variable=row['\ufeff언어변수'],
                                       value=row['언어값'],
                                       left=float(row['최저']),
                                       middle=float(row['중간']),
                                       right=float(row['최고']))
        with open('db/data_csv/rules.csv', 'r', encoding='utf-8') as fr:
            dr = csv.DictReader(fr)
            for row in dr:
                Rules.create(rule_num=row['\ufeff규칙번호'],
                             before_variable=row['전언어변수'],
                             before_not=bool(row['NOT']),
                             before_value=row['전언어값'],
                             and_field=bool(row['AND']),
                             or_field=bool(row['OR']),
                             after_variable=row['후언어변수'],
                             after_not=bool(row['NOT']),
                             after_value=row['후언어값'])

    def get_membership(self, season='', *args):
        data = {}
        for var in args:
            data[var] = {}
            ms = BeforeMembership.select().where(
                BeforeMembership.season == season, BeforeMembership.variable == var)
            for m in ms:
                data[var][m.value] = [m.left, m.middle, m.right]
        return data

# fuzzydb = FuzzyDB()
# d = fuzzydb.get_membership('봄', '기온', '습도')
