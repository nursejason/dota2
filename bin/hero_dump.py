#!/usr/bin python2.7

""" Script to dump hero DB and re-load all heroes. """

import logging
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from interactors.api_interactors import GetHeroesRequest
from interactors.sqlite_interactors import HeroesSqlInteractor
from handlers import parse_heroes

# TODO should run once daily
# TODO refactor into lib dirs
def main():
    heroes_context = GetHeroesRequest(logging)
    result = heroes_context.query_api()
    heroes = parse_heroes(result)

    heroes_sql_context = HeroesSqlInteractor()
    heroes_sql_context.insert_heroes_to_heroes(heroes)


if __name__ == "__main__":
    main()
