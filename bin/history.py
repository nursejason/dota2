"""
A simple script to call the Steam API, given a sequence number, to retrieve
match history and save it to a database.
"""
import requests
# TODO Add logging

API_KEY = 'E3973E62088C5C78E02E446D4A8491A8'
STEAM_URL = 'https://api.steampowered.com/IDOTA2Match_570/'
METHOD_URL = 'GetMatchHistoryBySequenceNum/v0001/'
VALID_LOBBY_TYPES = [0, 6, 7]
def main():
    data = query_steam('1626847481')
    print process_data(data)
    # TODO Save to DB

def query_steam(sequence_num):
    payload = {
        'key': API_KEY,
        'start_at_match_seq_num': sequence_num,
        'matches_requested': 1
    }
    url = STEAM_URL + METHOD_URL
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Error retrieving data from Steam API. Status %s, %s'
                        % response.status_code, response.text)

def process_data(data):
    """
    Args: data object from Steam API.
    returns: list_winning_heroes, list_losing_heroes from all matches in call.
    """
    result = None
    if data['result']['status'] == 1:
        result = data['result']
    else:
        raise Exception('Invalid data status')

    all_winning_heroes = []
    all_losing_heroes = []
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
            winning_heroes, losing_heroes = process_match(match)
            all_winning_heroes.extend(winning_heroes)
            all_losing_heroes.extend(losing_heroes)
        else:
            continue

    return all_winning_heroes, all_losing_heroes

def process_match(match):
    """
    Args: match object
    Returns:
        winning_heroes, losing_heroes: lists that contain the hero_id's of
            the heroes respective to the particular list in refernece.
    """
    winning_heroes = []
    losing_heroes = []
    radiant_win = match['radiant_win']
    for player in match['players']:
        if (radiant_win and player['player_slot'] < 5) or \
           (not radiant_win and player['player_slot'] >= 5):
            winning_heroes.append(player['hero_id'])

        elif radiant_win and player['player_slot'] >= 5 or \
           (not radiant_win and player['player_slot'] < 5):
            losing_heroes.append(player['hero_id'])

    return winning_heroes, losing_heroes

if __name__ == '__main__':
    main()
