"""
A simple script to call the Steam API, given a sequence number, to retrieve
match history and save it to a database.
"""
import requests

API_KEY = 'E3973E62088C5C78E02E446D4A8491A8'
STEAM_URL = 'https://api.steampowered.com/IDOTA2Match_570/'
METHOD_URL = 'GetMatchHistoryBySequenceNum/v0001/'
def main():
    data = query_steam('1626847481')
    # TODO Gather data
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
    for match in data.matches:
        # Do not process match if it has bots
        if match.human_players == 10:
            process_match(match)
        else:
            continue
        # TODO Lobby Type?
        # TODO Cluster?

def process_match(match):
    winning_heroes = {}
    losing_heroes = {}
    for player in match.players:
        if match.radiant_win:
            # winning heroes player slot 0 < X < 5
            # losing heroes player slot > 5
        # winning_heroes = radiant
        # losing_heroes = dire
            pass
    else:
        # winning heroes player slot > 5
        # losing heroes player slot 0 < X < 5
        # winning_heroes = dire
        # losing_heroes = radiant
        pass

def process_players():
    pass

def process_player():
    pass

if __name__ == '__main__':
    main()
