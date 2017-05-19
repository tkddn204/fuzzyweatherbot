import csv
import os

from fuzzyweather.fuzzy.db import database as db
from fuzzyweather.fuzzy.db.model import MembershipTable


class FuzzyDB:
    def __init__(self):
        db.get_conn()
        db.create_tables([MembershipTable, ], safe=True)
        if MembershipTable.select().count() is 0:
            self.__init_db()

    @staticmethod
    def __init_db():
        with open(os.path.abspath('db/data_csv/fuzzyset.csv'), 'r', encoding='utf-8') as f:
            dr = csv.DictReader(f)
            for row in dr:
                MembershipTable.create(season=row['\ufeff계절'],
                                       variable=row['언어변수'],
                                       value=row['언어값'],
                                       left=float(row['최저']),
                                       middle=float(row['중간']),
                                       right=float(row['최고']))

    def get_Membership(self, season='', variable=''):
        ms = MembershipTable.select().where(
            MembershipTable.season == season,
            MembershipTable.variable == variable)
        for m in ms:
            print(m.value, m.left, m.middle, m.right)


fuzzydb = FuzzyDB()
fuzzydb.get_Membership('봄', '기온')
