""" Queries for SQLite3 """


##############################################################################
######################### Heroes Win / Loss Queries ##########################
##############################################################################

CREATE_HEROES_WIN_LOSS = """
    CREATE TABLE
        heroes_win_loss
        (
            hero_1_id int,
            hero_2_id int,
            num_games int,
            hero_1_wins int,
            hero_1_losses int
        )
"""

CREATE_HERO_WIN_LOSS_INDEX_1 = """
    CREATE INDEX hero_1_id
    ON heroes_win_loss(hero_1_id)
"""

CREATE_HERO_WIN_LOSS_INDEX_2 = """
    CREATE INDEX hero_2_id
    ON heroes_win_loss(hero_2_id)
"""

INSERT_HEROES_WIN_LOSS = """
    INSERT INTO heroes_win_loss
        ('hero_1_id', 'hero_2_id', 'num_games', 'hero_1_wins', 'hero_1_losses')
    VALUES
        ('%s', '%s', 0, 0, 0)
"""

UPDATE_HEROES_WIN = """
    UPDATE heroes_win_loss
    SET num_games = num_games + 1,
        hero_1_wins = hero_1_wins + 1
    WHERE hero_1_id = %s
      AND hero_2_id = %s
"""

UPDATE_HEROES_LOSS = """
    UPDATE heroes_win_loss
    SET num_games = num_games + 1,
        hero_1_losses = hero_1_losses + 1
    WHERE hero_1_id = %s
      AND hero_2_id = %s
"""

##############################################################################
########################### Match History Queries ############################
##############################################################################

CREATE_MATCH_HISTORY_QUERY = """
    CREATE TABLE
        match_history
        (
            match_num varchar(24) PRIMARY KEY NOT NULL,
            sequence_num varchar(24) NOT NULL
        )
"""


##############################################################################
########################### Sequence Number Queries ##########################
##############################################################################

CREATE_SEQUENCE_NUM_TABLE = """
    CREATE TABLE
        most_recent_sequence_num
        (
            sequence_num varchar(12) PRIMARY KEY
        )
"""

INSERT_STARTING_SEQUENCE_NUMBER = """
    INSERT INTO most_recent_sequence_num
    (
        sequence_num varchar(24) PRIMARY KEY
    )
"""

##############################################################################
############################ Heroes Table Queries ############################
##############################################################################

CREATE_HEROES_TABLE = """
    heroes_table
    (
        id int PRIMARY KEY,
        name varchar(24)
    )
"""
