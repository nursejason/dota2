""" Interactor to SQLite DB """

from sqlalchemy import create_engine

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
    def insert_heroes_to_heroes(self, heroes):
        pass

class WinLossSqlInteractor(SqlInteractor):
    """ Interacts with Match history SQL table """
    def __init__(self):
        super(WinLossSqlInteractor, self).__init__()

    def save_relations(self, relations):
        """ Accepts a list of dictionaries containing:
            hero_1_id, hero_2_id, hero_1_win
            Converts each one to an appropriate SQL query and updates DB.
        """
        pass
