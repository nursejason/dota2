""" Interactor to SQLite DB """

import os
import sys

from sqlalchemy import create_engine

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) +
                '/../../lib')

from db.sqlite_queries import (
    INSERT_HEROES_WIN_LOSS, UPDATE_HEROES_WIN, UPDATE_HEROES_LOSS,
    GET_SEQUENCE_NUM, UPDATE_SEQUENCE_NUM, INSERT_HEROES)

class SqlInteractor(object):
    """ Base SQL Interactor Object """
    def __init__(self):
        self.engine_connect()

    def engine_connect(self):
        engine = create_engine('sqlite:///dota.db', echo=False)
        self.connection = engine.connect()

    def execute_query(self, query):
        result = self.connection.execute(query)
        return result

class HeroesSqlInteractor(SqlInteractor):
    """ Interacts with Heroes SQL table """
    def __init__(self):
        super(HeroesSqlInteractor, self).__init__()

    def insert_heroes_to_heroes(self, heroes):
        insert_query = INSERT_HEROES
        values = """(%(id)s, '%(name)s')"""
        for value in heroes:
            insert_query += values % value + ', '
        self.execute_query(insert_query[:-2])

class SequenceInteractor(SqlInteractor):
    def __init__(self):
        super(SequenceInteractor, self).__init__()

    def get_sequence_number(self):
        self.execute_query(GET_SEQUENCE_NUM)

    def set_sequence_number(self, sequence_number):
        self.execute_query(UPDATE_SEQUENCE_NUM % sequence_number)

class WinLossInteractor(SqlInteractor):
    """ Interacts with Match history SQL table """
    def __init__(self):
        super(WinLossInteractor, self).__init__()

    def insert_relation(self, hero_id_1, hero_id_2):
        self.execute_query(INSERT_HEROES_WIN_LOSS % (hero_id_1, hero_id_2))

    def update_relations(self, relations):
        """ Accepts a list of dictionaries containing:
            hero_1_id, hero_2_id, hero_1_win
            Converts each one to an appropriate SQL query and updates DB.
        """
        update_query = self._generate_relations_sql(relations)
        self.execute_query(update_query)

    def _generate_relations_sql(self, relations):
        """ Appends an update query string for each hero relation
            and returns the overall query.
        """
        query_string = ""
        for relation in relations:
            hero_1_win = relation['hero_1_win']
            del relation['hero_1_win']
            if hero_1_win:
                query_string += UPDATE_HEROES_WIN % relation
            else:
                query_string += UPDATE_HEROES_LOSS % relation
            query_string += " \n"

        return query_string
