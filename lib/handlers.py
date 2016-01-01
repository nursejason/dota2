""" App logic """
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from domain import generate_match_relations

#  TODO add logging
def process_matches_by_sequence_num(sequence_num, interactors):
    """ Retrieves match history from a sequence_num, generates hero relations,
        then stores the relations.
    """
    match_history = interactors.api_interactor.call_steam(sequence_num)
    relations = generate_match_relations(match_history['matches'])
    interactors.storage_interactor.save_relations(relations)
    return retrieve_last_sequence_number(match_history)

def retrieve_last_sequence_number(match_history):
    """ Finds the last match from a match_history dictionary, and returns the
        last sequence number seen.
    """
    matches = match_history['matches']
    return matches[len(matches) - 1]['match_seq_num']

def get_sequence_number(storage_interactor):
    return storage_interactor.get_sequence_number()

def set_sequence_number(storage_interactor, sequence_number):
    storage_interactor.set_sequence_number(sequence_number)
