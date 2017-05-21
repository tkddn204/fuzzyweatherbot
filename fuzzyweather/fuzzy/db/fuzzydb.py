import csv
from peewee import *

from fuzzyweather.fuzzy.db import database as db
from fuzzyweather.fuzzy.db.model import BeforeMembership, AfterMembership, Rules, ResultText

PATH = 'db/'+'data_csv/'


class FuzzyDB:
    def __init__(self):
        db.get_conn()
        db.create_tables([BeforeMembership, AfterMembership,
                          Rules, ResultText], safe=True)
        self.__init_db()

    @staticmethod
    def __init_db():
        if BeforeMembership.select().count() is 0:
            with open(PATH + 'before_fuzzyset.csv', 'r', encoding='utf-8') as fb:
                dr = csv.DictReader(fb)
                for row in dr:
                    BeforeMembership.create(season=row['\ufeff계절'],
                                            variable=row['언어변수'],
                                            value=row['언어값'],
                                            left=float(row['최저']),
                                            middle=float(row['중간']),
                                            right=float(row['최고']))

        if AfterMembership.select().count() is 0:
            with open(PATH + 'after_fuzzyset.csv', 'r', encoding='utf-8') as fa:
                dr = csv.DictReader(fa)
                for row in dr:
                    AfterMembership.create(variable=row['\ufeff언어변수'],
                                           value=row['언어값'],
                                           left=float(row['최저']),
                                           middle=float(row['중간']),
                                           right=float(row['최고']))

        if Rules.select().count() is 0:
            with open(PATH + 'rule.csv', 'r', encoding='utf-8') as fr:
                dr = csv.DictReader(fr)
                for row in dr:
                    Rules.create(rule_num=row['\ufeff규칙번호'],
                                 before_variable=row['전언어변수'],
                                 before_not=int(row['전_NOT']),
                                 before_value=row['전언어값'],
                                 and_field=int(row['AND']),
                                 or_field=int(row['OR']),
                                 after_variable=row['후언어변수'],
                                 after_not=int(row['후_NOT']),
                                 after_value=row['후언어값'])

    def get_before_membership(self, season='', *args):
        data = {}
        for var in args:
            data[var] = {}
            ms = BeforeMembership.select().where(
                BeforeMembership.season == season, BeforeMembership.variable == var)
            for m in ms:
                data[var][m.value] = [m.left, m.middle, m.right]
        return data

    def get_after_membership(self, *args):
        data = {}
        for var in args:
            data[var] = {}
            ms = AfterMembership.select().where(
                AfterMembership.variable == var)
            for m in ms:
                data[var][m.value] = [m.left, m.middle, m.right]
        return data


    def get_rule_nums(self):
        return Rules.select(fn.MAX(Rules.rule_num)).scalar()

    def get_rules(self, rule_num=1):
        return Rules.select().where(Rules.rule_num == rule_num)

    # def get_before_rule(self, rule_num=1):
    #     return Rules.select(Rules.before_variable,
    #                         Rules.before_not, Rules.before_value)\
    #                 .where(Rules.rule_num == rule_num)
    #
    # def get_rule_operater(self, rule_num=1):
    #     return Rules.select(Rules.and_field, Rules.or_field)\
    #                 .where(Rules.rule_num == rule_num)
    #
    # def get_after_rule(self, rule_num=1):
    #     return Rules.select(Rules.after_variable,
    #                         Rules.after_not, Rules.after_value)\
    #                 .where(Rules.rule_num == rule_num)

# fuzzydb = FuzzyDB()
# d = fuzzydb.get_before_membership('봄', '기온', '습도')
# print(d)
# d = fuzzydb.get_after_membership('결과')
# print(d)
# for r in fuzzydb.get_rules():
#     print(r.before_variable)
