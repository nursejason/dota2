#!/usr/bin python2.7
"""
A simple script to call the Steam API, given a sequence number, to retrieve
match history and save it to a database.
"""

# TODO Stop pulling data if date == today
# TODO incomplete game logic
# TODO Retry logic
""" TODO Board
-> Begin Grabbing Basic Hero Data
3. DB For all heroes: name, id, localized_name, win%
4. Script to save hero data to DB
<- Heroes should be done
-> Begin data relation script
5. DB For win_loss_relation:
    hero_id, compare_hero_id, win%
6. for hero in heroes:
    a. SELECT losing_hero_1-5 FROM hero_matches WHERE winning_hero_1-5 = hero
    b. for match in result:
        i. add to dict
    c. add to overall dict
save to db
<- data relation script complete
-> Begin writing UI component -- Main Logic -- API?
7. for each hero picked, grab win rates of all remaining heroes.
   average all win rates together
   return averaged win rates
    SELECT * from win_loss_relation
    WHERE hero_id or compare_hero_id IN [heroes_picked]
<- End main logic, make pretty GUI
----->
BASIC APPLICATION MILESTONE COMPLETE
At this point some minor clean arch refactoring should take place.
This should remain a 'behemoth' application for the time being.
Will need to consider where to go next from here. Should I begin adding ad
revenue and working on SEO? Or should I start working on the more advanced
pieces that will make this more accurate.
<----
# One thing worth noting... Should supports or various hero types carry
different weights? Or do all heroes have equal impact on the game? I think all
have equal impact.
"""

import logging
import os
import sys
import time

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../lib')

from interactors.api_interactors import GetMatchHistoryRequest
from interactors.sqlite_interactors import MatchSqlInteractor

VALID_LOBBY_TYPES = [0, 6, 7]

def main():
    """
    1. Grab the most recent sequence number in the table.
    2. Query Steam using the most recent sequence number
    3. Process match and hero relation data
    4. Save match and hero data to DB.
    5. Update sequence number.
    """
    history = GetMatchHistoryRequest(logging)
    while True:
        sequence_num = get_sequence_num()
        raw_data = query_steam(history, sequence_num)

        match_relations, hero_relations = process_data(raw_data)
        save_hero_data(hero_relations)
        save_match_data(match_relations)

        latest_sequence_num = retrieve_sequence_num(raw_data)
        save_sequence_number(latest_sequence_num)
        time.sleep(60)

def query_steam(request_adapter, sequence_num):
    logging.info('Querying Steam VIA Adapter.')
    return request_adapter.query_api(sequence_num)

def process_data(data):
    """
    Args: data object from Steam API.
    returns: list_winning_heroes, list_losing_heroes from all matches in call.
    """
    logging.info('Begin processing Steam data.')
    result = None
    if data['result']['status'] == 1:
        result = data['result']
    else:
        raise Exception('Invalid data status')

    hero_relations = []
    match_relations = []
    for match in result['matches']:
        # Only concerned with some lobby types. (This could be an issue)
        if match['lobby_type'] not in VALID_LOBBY_TYPES:
            print "Invalid Lobby Type: %s" % match['lobby_type']
            continue

        # Matches shorter than 15 minutes have some sort of monkey business.
        if match['duration'] < 900:
            print "Too short match duration"
            continue

        # Do not process match if it has bots
        if match['human_players'] == 10:
            match_data, hero_data = process_match(match)
            match_relations.append(match_data)
            hero_relations.append(hero_data)
        else:
            continue

    return match_relations, hero_relations

def process_match(match):
    """
    Args: match dict -> Dictionary that contains match information from steam.
    Returns:
        match_data ~> Dict containing match_num and sequence_num
        hero_data ~> Dict containing hero 1-5 win and hero 1-5 loss + match_num
    """
    # TODO May need reworking
    match_data = {'match_num': match['match_id'],
                  'sequence_num': match['match_seq_num']}
    hero_data = get_hero_data(match)
    hero_data['match_num'] = match['match_id']

    logging.debug('Match data: %s', match_data)
    logging.debug('Hero data: %s', hero_data)
    return match_data, hero_data

def get_hero_data(match):
    """
    Args: match object
    Returns:
        hero_data ~> Dict containing hero 1-5 win and hero 1-5 loss + match_num
    """
    hero_data = {}
    for player in match['players']:
        pass # TODO
        # TODO Create a list of dictionaries
        # hero_1 = x
        # hero_2 = y
        # win/loss bool

    return hero_data

def retrieve_sequence_num(row_data): # TODO
    return ''

# TODO Is match data still necessary?
#def save_match_data(match_data):
#    logging.info('Attempt to save match data to DB.')
#    insert_query = """
#        INSERT INTO 'match_history'
#            ('match_num', 'sequence_num')
#        VALUES
#    """
#    values = "('%(match_num)s', '%(sequence_num)s')"
#    for value in match_data:
#        insert_query += values % value + ', '
#    _execute_sql(insert_query[:-2])

# TODO Use handler
#def get_sequence_num():
#    logging.info('Attempt to query for most recent sequence number.')
#    select = 'SELECT * FROM most_recent_sequence_num'
#    row = _execute_sql(select).fetchone()
#    return row.sequence_num

# TODO Use handler
#def save_sequence_number(latest_sequence_num):
#    logging.info('Attempt to save most recent sequence num to db')
#    query = """
#        INSERT INTO most_recent_sequence_num
#            ('sequence_num')
#        VALUES ('%s')
#    """ % latest_sequence_num
#    _execute_sql(query)

# TODO Use handler
#def _execute_sql(query):
#    engine = create_engine('sqlite:///dota.db', echo=False)
#    connection = engine.connect()
#    result = connection.execute(query)
#    logging.info('Successfully ran query.')
#    return result

if __name__ == '__main__':
    logging.basicConfig(filename='history.log', level=logging.INFO)
    main()
