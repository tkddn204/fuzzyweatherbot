import csv
from peewee import *

from fuzzyweather.fuzzy.db import PATH, database as db
from fuzzyweather.fuzzy.db.model import BeforeMembership, AfterMembership, Rules
from fuzzyweather.util.timer import get_season


class FuzzyDB:
    def __init__(self):
        db.get_conn()
        db.create_tables([BeforeMembership, AfterMembership, Rules], safe=True)
        self.__init_db()

    @staticmethod
    def __init_db():
        if BeforeMembership.select().count() is 0:
            with open(PATH + 'data_csv/before_fuzzyset.csv', 'r', encoding='utf-8') as fb:
                dr = csv.DictReader(fb)
                for row in dr:
                    if '' not in row:
                        BeforeMembership.create(season=row['\ufeff계절'],
                                                variable=row['언어변수'],
                                                value=row['언어값'],
                                                left=float(row['최저']),
                                                middle=float(row['중간']),
                                                right=float(row['최고']))

        if AfterMembership.select().count() is 0:
            with open(PATH + 'data_csv/after_fuzzyset.csv', 'r', encoding='utf-8') as fa:
                dr = csv.DictReader(fa)
                for row in dr:
                    if '' not in row:
                        AfterMembership.create(variable=row['\ufeff언어변수'],
                                               value=row['언어값'],
                                               left=float(row['최저']),
                                               middle=float(row['중간']),
                                               right=float(row['최고']),
                                               text=row['텍스트'],
                                               emoticon=row['이모티콘'])

        if Rules.select().count() is 0:
            with open(PATH + 'data_csv/rule.csv', 'r', encoding='utf-8') as fr:
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

    def get_before_membership(self):
        season = get_season()
        result_before_membership = {}
        variables = self.get_before_variables()
        for var in variables:
            result_before_membership[var.variable] = {}
            before_membership = BeforeMembership.select().where(
                BeforeMembership.season == season,
                BeforeMembership.variable == var.variable)
            for before in before_membership:
                result_before_membership[var.variable][before.value] =\
                    [before.left, before.middle, before.right]
        return result_before_membership

    def get_after_membership(self):
        result_after_membership = {}
        variables = self.get_after_variables()
        for var in variables:
            result_after_membership[var] = {}
            after_membership = AfterMembership.select().where(
                AfterMembership.variable == var)
            for after in after_membership:
                result_after_membership[var][after.value] =\
                    [after.left, after.middle, after.right]
        return result_after_membership

    @staticmethod
    def get_before_variables():
        return BeforeMembership.select(BeforeMembership.variable)\
            .distinct().order_by(BeforeMembership.variable.asc())

    @staticmethod
    def get_after_variables():
        return AfterMembership.select(AfterMembership.variable)\
            .distinct().order_by(AfterMembership.variable.asc()).scalar(as_tuple=True)

    def get_after_text_and_emoticon(self):
        return AfterMembership.select(AfterMembership.value, AfterMembership.text, AfterMembership.emoticon)\
            .where(AfterMembership.variable == self.get_after_variables()[0])

    @staticmethod
    def get_rule_nums():
        return Rules.select(fn.MAX(Rules.rule_num)).scalar()

    @staticmethod
    def get_rule(rule_num=1):
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
# d = fuzzydb.get_before_membership()
# print(d)
# d = fuzzydb.get_after_membership('결과')
# print(d)
# for r in fuzzydb.get_rules():
#     print(r.before_variable)
