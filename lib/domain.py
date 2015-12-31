""" Business logic layer """

def generate_match_relations(matches):
    hero_relations = []
    for match in matches:
        hero_relations.extend(generate_match_hero_relations(
            match['players'], match['radiant_win']))
    return hero_relations

def generate_match_hero_relations(players, radiant_win):
    """
        Accepts
        players - list
        radiant_win - bool

        Maps players, based on slot, to radiant or dire. These are then use to
        create a mapping of win/loss relations based on radiant_win value
    """
    radiant_heroes = []
    dire_heroes = []
    for player in players:
        if player['player_slot'] <= 4:
            radiant_heroes.append(player['hero_id'])
        else:
            dire_heroes.append(player['hero_id'])

    win_loss_relations = []
    for radiant in radiant_heroes:
        for dire in dire_heroes:
            win_loss_relations.append(_create_hero_relation(
                radiant, dire, radiant_win))
    return win_loss_relations

def _create_hero_relation(hero_1_id, hero_2_id, hero_1_win):
    """ Mapping is only stored one directionally.
        Ex. Hero 1-4, Hero 2-5, Hero 1-win True is a valid mapping.
        Hero 1-5, Hero 2-4, Hero 1-win True is an invalid mapping
        This would instead be represented as:
        Hero 1-4, Hero 2-5, Hero 1-win False
    """
    # Flip the values if hero_1 > hero_2
    if hero_1_id > hero_2_id:
        temp = hero_1_id
        hero_1_id = hero_2_id
        hero_2_id = temp
        hero_1_win = not hero_1_win

    relation = {'hero_1_id': hero_1_id, 'hero_2_id': hero_2_id,
                'hero_1_win': hero_1_win}
    return relation
