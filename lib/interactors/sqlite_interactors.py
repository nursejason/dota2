""" Interactor to SQLite DB """

import os
import sys
from sqlalchemy import create_engine

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../../lib')
from db.sqlite_queries import INSERT_HEROES, INSERT_INITIAL_WIN_LOSS

class SqlInteractor(object):
    """ Base SQL Interactor Object """
    def __init__(self):
        self.engine_connect()

    def engine_connect(self):
        engine = create_engine('sqlite:///../db/dota.db', echo=False)
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

    def insert_initial_win_loss(self):
        insert_query = INSERT_INITIAL_WIN_LOSS
        values = []
        patch = "1" # TODO: Need to grab version numba
        rows = 100 # Only insert 100 rows at a time

        for hero_1 in xrange(1,125):
            if len(values) > rows:
                query = insert_query + ",".join(values)
                self.execute_query(query)
                values = []

            for hero_2 in xrange(1,125):
                if hero_2 > hero_1:
                    values.append("(%i, %i, 0, 0, 0, '%s')" %
                                  (hero_1,hero_2,patch))
        query = insert_query + ",".join(values)
        self.execute_query(query)


class MatchSqlInteractor(SqlInteractor):
    """ Interacts with Match history SQL table """
    def __init__(self):
        super(MatchSqlInteractor, self).__init__()

    def insert_hero_match_data(self, hero_data):
        """ Format query and values for match history
            Input: hero_data -> ...
        """
        insert_query = """
            INSERT INTO hero_matches
                ('winning_hero_1', 'winning_hero_2', 'winning_hero_3',
                 'winning_hero_4', 'winning_hero_5', 'losing_hero_1',
                 'losing_hero_2', 'losing_hero_3', 'losing_hero_4',
                 'losing_hero_5','match_num')
            VALUES
        """
        values = ("(%(winning_hero_1)s, %(winning_hero_2)s, %(winning_hero_3)s, "
                  "%(winning_hero_4)s, %(winning_hero_5)s, %(losing_hero_1)s, "
                  "%(losing_hero_2)s, %(losing_hero_1)s, %(losing_hero_4)s, "
                  "%(losing_hero_5)s, '%(match_num)s')")

        for value in hero_data:
            insert_query += values % value + ', '
        self.execute_query(insert_query[:-2])

    def insert_match_history(self, match_data):
        """ Inserts match + sequence number into match_history table
            Input: match_data -> ...
        """
        insert_query = """
            INSERT INTO 'match_history'
                ('match_num', 'sequence_num')
            VALUES
        """
        values = "('%(match_num)s', '%(sequence_num)s')"
        for value in match_data:
            insert_query += values % value + ', '
        self.execute_query(insert_query[:-2])
