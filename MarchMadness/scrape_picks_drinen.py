import requests
import re
import pandas as pd
import json

YEAR = str(2019)

team_translations = {}
with open('./March' + YEAR + '/Team_Translations.json') as f:
    team_translations = json.load(f)

teams_df = pd.read_csv('./March' + YEAR + '/Starting_Bracket.csv', index_col='ID')
starting_player_dict = {}
for key, value in teams_df.iterrows():
    starting_player_dict[value['TEAM']] = ''

r = requests.get('http://ddrinen.com/mm/')
body_text = r.text

pick_dict = {}
regex = r"^(?P<TEAM>[A-Za-z\s]*)\s\s(?P<NUM_PICKS>[0-9]{1,2})\s*(?P<PLAYER_LIST>[A-Za-z\s]*)$"
matches = re.finditer(regex, body_text, re.MULTILINE)
for match_num, match in enumerate(matches, start=1):
    team = match.group('TEAM').strip()
    num_picks = int(match.group('NUM_PICKS'))
    player_list_str = match.group('PLAYER_LIST')
    player_list = player_list_str.split()
    player_list_len = len(player_list)

    if num_picks != player_list_len:
        print(team)

    pick_dict[team] = {
            'num_picks': num_picks,
            'player_list': player_list
        }


players_picks = {}
for key, value in pick_dict.items():
    team_name = ''
    needs_translation = starting_player_dict.get(key)
    if needs_translation is None:
        team_name = team_translations.get(key)
        if team_name is None:
            print(key)
            continue
    if team_name == '':
        team_name = key

    player_dict = {}
    for player in value['player_list']:
        player_dict = players_picks.get(player)
        if player_dict is None:
            player_dict = starting_player_dict.copy()

        player_dict[team_name] = 'x'
        players_picks[player] = player_dict


player_list_dict = {
    'players': []
    }

for key, value in players_picks.items():
    player_list_dict['players'].append(key)


player_list_dict_df = pd.DataFrame(player_list_dict)
player_list_dict_df.to_csv('./March' + YEAR + '/players.csv')

players_df = pd.DataFrame(players_picks)
players_df.to_csv('./March' + YEAR + '/player_picks.csv')