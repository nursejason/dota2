#!/usr/bin/python2.7
""" SQLAlchemy Relational DB Functions"""
import os
import sqlalchemy
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from db.sqlite_queries import (
    CREATE_HEROES_WIN_LOSS_TABLE,
    CREATE_HERO_WIN_LOSS_INDEX_1,
    CREATE_HERO_WIN_LOSS_INDEX_2,
    CREATE_MATCH_HISTORY_TABLE,
    CREATE_SEQUENCE_NUM_TABLE,
    CREATE_HEROES_TABLE)

def main():
    """ Run create table and add index migrations """
    engine = sqlalchemy.create_engine('sqlite:///dota.db', echo=False)
    conn = engine.connect()
    queries = [
        CREATE_HEROES_WIN_LOSS_TABLE,
        CREATE_HERO_WIN_LOSS_INDEX_1,
        CREATE_HERO_WIN_LOSS_INDEX_2,
        CREATE_MATCH_HISTORY_TABLE,
        CREATE_SEQUENCE_NUM_TABLE,
        CREATE_HEROES_TABLE
    ]

    for query in queries:
        try:
            conn.execute(query)
        except sqlalchemy.exc.OperationalError, exception:
            print 'Exception executing sql query. %s' % exception

if __name__ == "__main__":
    main()
