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
from interactors.context import Context
from interactors.sqlite_interactors import WinLossInteractor, SequenceInteractor
from handlers import (
    process_matches_by_sequence_num, get_sequence_number, set_sequence_number)

def main():
    """
    1. Grab the most recent sequence number in the table.
    2. Query Steam using the most recent sequence number
    3. Process match and hero relation data
    4. Save match and hero data to DB.
    5. Update sequence number.
    """
    interactors = Context()
    interactors.api_interactor = GetMatchHistoryRequest(logging)
    interactors.storage_interactor = WinLossInteractor(logging)
    interactors.sequence_interactor = SequenceInteractor(logging)

    while True:
        sequence_number = get_sequence_number(interactors.sequence_interactor)
        process_matches_by_sequence_num(sequence_number, interactors)
        set_sequence_number(sequence_number, interactors.sequence_interactor)
        time.sleep(60)

if __name__ == '__main__':
    #logging.basicConfig(filename='history.log', level=logging.INFO)
    main()
