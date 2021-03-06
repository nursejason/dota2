### DotA2 Pick Hax

This API driven application is intended to use public information to assist in the DotA draft screen.

##### v1. Basic counterpicking
- Enter in any number of heroes and retrieve counterpick information.
  - Match data needs to be stored with all ten heroes and winning team.
  - Hero data needs to be stored with all heroes, names, and id's
  - To generate win-loss-relations, use match data stored from above, iterating through each hero, and querying for all matches with that hero. Iterate through results, and write to DB. Ignore processing for heroes with ID < current ID, as that ID would have already been processed.
  - A simple API will need to be created in order for the front end to get win-loss-relational data.
  - Finally a UI needs to be created in order for users to consume the service.

- Includes:
  - 1. Script to store hero win/loss relation data. Runs every 30-45s
    - history.py # TODO should rename
  - 2. Script to store hero data. Runs every day # Done
    - hero_dump.py
  - ~~3. Script to generate win-loss-relations. Runs every day~~ # Swapped to 1.
  - 4. Generate back-end for UI component
  - 5. Create UI Component

##### Step v1.1 Sorting and filtering on UI
- Be able to filter and sort by ranged, carry, etc based on role required.
- Be able to search for hero name to find counter rating

- Includes:
  - Adding role to Hero DB
  - Add search functionality to UI when picking and also when looking at counters
  - Add filters and sorting drop downs to UI

##### Step ??. Search Engine Optimization

##### Step ??. Monetize

##### Step 2. Team composition
- Pull hero information from DotA website. Balance a team based on that information.

##### Step 3. Exploiting enemy team composition
- Lack stuns? Pick mobile heroes. Etc.

##### Step 4. Player picks
- Add user account creation
- Account creation allows user to input dota2 username in order to look at win rate statistics with heroes.
  - > 50% win rate causes hero to go up in picks
  - < 50% win rate causes hero to go down in picks

##### Step 5. Advanced player specific picks
- Allows user to input player names of people on current / opposing teams in order to give advice for picking, banning, and hate drafting based on player statistics.
- Look for and display usernames of players that user plays with frequently for quick add.

##### Step 6. Counterpicking improved
- Use game statistics in order to counterpick
  - Will require some advanced formulas

##### Step 8. Item Guides
- Recommended item use against enemy heroes.
- Recommended item use that goes well with your team.

##### Step ??. Mobile platform

##### Step ??. Input your team

##### Step ??. Advanced team composition
- Ex. User desires a pushing team, and therefore the team comp allows for additional pushing in order to become balanced.
