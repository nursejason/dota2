#!/usr/bin python2.7

""" Script to dump hero DB and re-load all heroes. """

import logging
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from interactors.api_interactors import GetHeroesRequest

# TODO should run once daily
def main():
    heroes_context = GetHeroesRequest(logging)
    result = heroes_context.query_api()
    heroes = parse_heroes(result)
    # TODO save to DB

def parse_heroes(json):
    heroes = []
    for hero in json['result']['heroes']:
        parsed_hero = hero['name'].split('npc_dota_hero_')[1].replace('_', " ")
        heroes.append({hero['id'], parsed_hero})
    return heroes

if __name__ == "__main__":
    main()
