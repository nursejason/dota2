#!/usr/bin/python2.7
""" SQLAlchemy Relational DB Functions"""
from sqlalchemy import create_engine

CREATE_MATCH_HISTORY_QUERY = """
CREATE TABLE
    match_history
    (
        match_num varchar(12) PRIMARY KEY NOT NULL,
        sequence_num varchar(12) NOT NULL
    )
"""

# TODO Does this table need an index?
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

def main():
    engine = create_engine('sqlite:///dota.db', echo=False)
    conn = engine.connect()
    conn.execute(CREATE_MATCH_HISTORY_QUERY)
    conn.execute(CREATE_HERO_MATCHES_QUERY)

if __name__ == "__main__":
    main()
