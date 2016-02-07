#!/usr/bin python2.7

""" Script to load initial rows into heroes_win_loss table """
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from interactors.api_interactors import GetHeroesRequest
from interactors.sqlite_interactors import HeroesSqlInteractor

def main():
    heroes_sql_context = HeroesSqlInteractor()
    heroes_sql_context.insert_initial_win_loss()

if __name__ == "__main__":
    main()
