""" App logic """
import os
import sys
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')


def process_data():
    pass

def parse_heroes(data):
    heroes = []
    for hero in data['result']['heroes']:
        parsed_hero = hero['name'].split('npc_dota_hero_')[1].replace('_', " ")
        heroes.append({'id':hero['id'], 'name':parsed_hero})
    return heroes
