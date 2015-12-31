""" App logic """
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from domain import generate_match_relations

def process_matches_by_sequence_num(sequence_num, interactors):
    result = interactors.api_interactor.call_steam(sequence_num)
    relations = generate_match_relations(result['matches'])
    interactors.storage_interactor.save_relations(relations)

def get_sequence_number(storage_interactor):
    return storage_interactor.get_sequence_number()

def set_sequence_number(storage_interactor, sequence_number):
    storage_interactor.set_sequence_number(sequence_number)
