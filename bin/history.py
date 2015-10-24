#!/usr/bin/env python2.7
"""
A simple script to call the Steam API, given a sequence number, to retrieve
match history and save it to a database.
"""

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
import requests
from sqlalchemy import create_engine

API_KEY = 'E3973E62088C5C78E02E446D4A8491A8'
STEAM_URL = 'https://api.steampowered.com/IDOTA2Match_570/'
METHOD_URL = 'GetMatchHistoryBySequenceNum/v0001/'
VALID_LOBBY_TYPES = [0, 6, 7]

def main():
    """
    1. Grab the most recent sequence number in the table.
    2. Query Steam using the most recent sequence number
    3. Process match and hero relation data
    4. Save match and hero data to DB.
    5. Update sequence number.
    """
    while True:
        sequence_num = get_sequence_num()
        raw_data = query_steam(sequence_num)

        match_relations, hero_relations = process_data(raw_data)
        save_hero_data(hero_relations)
        save_match_data(match_relations)

        latest_sequence_num = retrieve_sequence_num(raw_data)
        save_sequence_number(latest_sequence_num)

def query_steam(sequence_num):
    logging.info('Begin Steam query')
    payload = {
        'key': API_KEY,
        'start_at_match_seq_num': sequence_num
    }
    url = STEAM_URL + METHOD_URL
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        logging.info('Successful query to Steam API')
        return response.json()
    else:
        logging.error('Error calling steam API. %s:%s', response.status_code,
                      response.text)
        raise Exception('Error retrieving data from Steam API. Status %s, %s'
                        % response.status_code, response.text)

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

    logging.info('Match relations: %s', match_relations)
    logging.info('Hero relations: %s', hero_relations)
    return match_relations, hero_relations

def process_match(match):
    """
    Args: match dict -> Dictionary that contains match information from steam.
    Returns:
        match_data ~> Dict containing match_num and sequence_num
        hero_data ~> Dict containing hero 1-5 win and hero 1-5 loss + match_num
    """
    match_data = {'match_num': match['match_id'],
                  'sequence_num': match['match_seq_num']}
    hero_data = get_hero_data(match)
    hero_data['match_num'] = match['match_id']

    logging.info('Match data: %s', match_data)
    logging.info('Hero data: %s', hero_data)
    return match_data, hero_data



def get_hero_data(match):
    """
    Args: match object
    Returns:
        hero_data ~> Dict containing hero 1-5 win and hero 1-5 loss + match_num
    """
    hero_data = {}
    win_key = 'winning_hero_%s'
    lose_key = 'losing_hero_%s'
    idx = 1
    for player in match['players']:
        # Reset index for other set of keys
        if idx > 5:
            idx = 1

        if is_winning_player(match['radiant_win'], player['player_slot']):
            hero_data[win_key % idx] = player['hero_id']
        else:
            hero_data[lose_key % idx] = player['hero_id']
        idx += 1

    return hero_data

def is_winning_player(radiant_win, player_slot):
    """ Could just return the top most condition, but I feel the need to
        validate the logic.
    """
    if (radiant_win and player_slot < 5) or \
       (not radiant_win and player_slot >= 5):
        return True

    elif radiant_win and player_slot >= 5 or \
       (not radiant_win and player_slot < 5):
        return False

    else:
        raise Exception('Conditions for is_winning_player are invalid')

def retrieve_sequence_num(row_data):
    return ''

def save_hero_data(hero_data):
    logging.info('Attempt to hero data to DB.')
    insert_query = """
        INSERT INTO hero_matches
            ('winning_hero_1', 'winning_hero_2', 'winning_hero_3',
             'winning_hero_4', 'winning_hero_5', 'losing_hero_1',
             'losing_hero_2', 'losing_hero_3', 'losing_hero_4',
             'losing_hero_5','match_num')
        VALUES
    """
    values = ("(%(winning_hero_1)s, %(winning_hero_2)s, %(winning_hero_3)s, "
              "%(winning_hero_4)s, %(winning_hero_5)s, %(losing_hero_1)s, "
              "%(losing_hero_2)s, %(losing_hero_1)s, %(losing_hero_4)s, "
              "%(losing_hero_5)s, '%(match_num)s')")

    for value in hero_data:
        insert_query += values % value + ', '
    _execute_sql(insert_query[:-2])

def save_match_data(match_data):
    logging.info('Attempt to save match data to DB.')
    insert_query = """
        INSERT INTO 'match_history'
            ('match_num', 'sequence_num')
        VALUES
    """
    values = "('%(match_num)s', '%(sequence_num)s')"
    for value in match_data:
        insert_query += values % value + ', '
    _execute_sql(insert_query[:-2])

def get_sequence_num():
    logging.info('Attempt to query for most recent sequence number.')
    select = 'SELECT * FROM most_recent_sequence_num'
    row = _execute_sql(select).fetchone()
    return row.sequence_num

def save_sequence_number(latest_sequence_num):
    logging.info('Attempt to save most recent sequence num to db')
    query = """
        INSERT INTO most_recent_sequence_num
            ('sequence_num')
        VALUES ('%s')
    """ % latest_sequence_num
    _execute_sql(query)

def _execute_sql(query):
    engine = create_engine('sqlite:///dota.db', echo=False)
    connection = engine.connect()
    result = connection.execute(query)
    logging.info('Successfully ran query.')
    return result

if __name__ == '__main__':
    logging.basicConfig(filename='history.log', level=logging.INFO)
    main()
