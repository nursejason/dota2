#!/usr/bin/python2.7
""" SQLAlchemy Relational DB Functions"""
import sqlalchemy

CREATE_MATCH_HISTORY_QUERY = """
CREATE TABLE
    match_history
    (
        match_num varchar(12) PRIMARY KEY NOT NULL,
        sequence_num varchar(12) NOT NULL
    )
"""

CREATE_HERO_MATCHES_QUERY = """
CREATE TABLE
    hero_matches
    (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        winning_hero_1 int NOT NULL,
        winning_hero_2 int NOT NULL,
        winning_hero_3 int NOT NULL,
        winning_hero_4 int NOT NULL,
        winning_hero_5 int NOT NULL,
        losing_hero_1 int NOT NULL,
        losing_hero_2 int NOT NULL,
        losing_hero_3 int NOT NULL,
        losing_hero_4 int NOT NULL,
        losing_hero_5 int NOT NULL,
        match_num varchar(12) NOT NULL
    )
"""

CREATE_WINNING_HERO_INDEX = """
CREATE INDEX winning_hero_%s
ON hero_matches (winning_hero_%s)
"""

CREATE_LOSING_HERO_INDEX = """
CREATE INDEX losing_hero_%s
ON hero_matches (losing_hero_%s)
"""

CREATE_SEQUENCE_NUM_TABLE = """
CREATE TABLE
    most_recent_sequence_num
    (
        sequence_num varchar(12) PRIMARY KEY
    )
"""

INSERT_START_SEQUENCE_NUM = """
INSERT INTO most_recent_sequence_num
    ('sequence_num')
VALUES ('1626847481')
"""

CREATE_HEROES_TABLE = """
CREATE TABLE
    heroes_table
    (
        id int PRIMARY KEY,
        name varchar(24)
    )
"""

def main():
    engine = sqlalchemy.create_engine('sqlite:///dota.db', echo=False)
    conn = engine.connect()
    queries = [
        CREATE_MATCH_HISTORY_QUERY,
        CREATE_HERO_MATCHES_QUERY,
        CREATE_SEQUENCE_NUM_TABLE,
        INSERT_START_SEQUENCE_NUM
    ]
    for i in range(1, 6):
        queries.append(CREATE_WINNING_HERO_INDEX % (i, i))
        queries.append(CREATE_LOSING_HERO_INDEX % (i, i))

    for query in queries:
        try:
            conn.execute(query)
        except sqlalchemy.exc.OperationalError, exception:
            print 'Exception executing sql query. %s' % exception

if __name__ == "__main__":
    main()
