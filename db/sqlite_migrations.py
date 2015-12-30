#!/usr/bin/python2.7
""" SQLAlchemy Relational DB Functions"""
import sqlalchemy
# TODO Import Queries

def main():
    engine = sqlalchemy.create_engine('sqlite:///dota.db', echo=False)
    conn = engine.connect()
    queries = [
    ]

    for query in queries:
        try:
            conn.execute(query)
        except sqlalchemy.exc.OperationalError, exception:
            print 'Exception executing sql query. %s' % exception

if __name__ == "__main__":
    main()
