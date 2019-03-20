
import json
import math
import random
import pandas as pd

REGIONS = ['East', 'South', 'West', 'Midwest']

def main():

    teams_df = pd.read_csv('.\March2019\Starting_Bracket.csv', index_col='ID')

    bracket = initialize_bracket(teams_df)
    bracket = next_round(bracket, 64)
    bracket = next_round(bracket, 32)
    bracket = next_round(bracket, 16)
    bracket = next_round(bracket, 8)
    bracket = next_round(bracket, 4)
    bracket = next_round(bracket, 2)
    json_bracket = json.dumps(bracket)
    print(json_bracket)

def initialize_bracket(teams):
    region_index = 0
    return_bracket = {
        'teams_64': {}
        }

    for x in range(32):
        game_key = 'game_' + str(x)
        seed = (x % 8) + 1
        opponent_seed = 17 - seed
        region = REGIONS[region_index]

        query_start = 'ID == "' + region
        query_end = '"'
        team_1 = teams.query(query_start + str(seed) + query_end).to_dict('records')[0]
        team_2 = teams.query(query_start + str(opponent_seed) + query_end).to_dict('records')[0]

        next_game_index = ((seed-1) % 4) + (region_index*4)
        if seed > 4:
            next_game_index = (8-seed) + (region_index*4)

        game = {
                'team_1': {
                        'name': team_1['TEAM'],
                        'BPI': team_1['BPI']
                    },
                
                'team_2': {
                        'name': team_2['TEAM'],
                        'BPI': team_2['BPI']
                    },
                'next_game_key': 'game_' + str(next_game_index),
                'region': region
            }

        return_bracket['teams_64']['game_' + str(x)] = game

        if seed == 8:
            region_index += 1

    return_bracket['teams_32'] = {
            'game_0': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_1': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            },
            'game_2': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            },
            'game_3': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_4': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_2'
            },
            'game_5': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_3'
            },
            'game_6': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_3'
            },
            'game_7': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_2'
            },
            'game_8': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_4'
            },
            'game_9': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_5'
            },
            'game_10': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_5'
            },
            'game_11': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_4'
            },
            'game_12': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_6'
            },
            'game_13': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_7'
            },
            'game_14': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_7'
            },
            'game_15': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_6'
            }
        }
    return_bracket['teams_16'] = {
            'game_0': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_1': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_2': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            },
            'game_3': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            },
            'game_4': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_2'
            },
            'game_5': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_2'
            },
            'game_6': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_3'
            },
            'game_7': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_3'
            }
        }
    return_bracket['teams_8'] = {
            'game_0': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_1': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_2': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            },
            'game_3': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_1'
            }
        }
    return_bracket['teams_4'] = {
            'game_0': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            },
            'game_1': {
                'team_1': {},
                'team_2': {},
                'next_game_key': 'game_0'
            }
        }
    return_bracket['teams_2'] = {
            'game_0': {
                'team_1': {},
                'team_2': {},
                'winner': ''
            }
        }
    return return_bracket


def next_round(bracket, teams_left):
    next_round_key = 'teams_' + str(int(teams_left/2))
    current_round = bracket['teams_' + str(teams_left)]

    for key, value in current_round.items():
        team_1 = value['team_1']
        team_2 = value['team_2']

        team_1_odds = 1/(1+math.exp(-(team_1['BPI']-team_2['BPI'])/5))
        winner = team_2
        if random.random() < team_1_odds:
            winner = team_1
            
        if teams_left == 2:
            bracket['teams_2']['game_0']['winner'] = winner['name']
            return bracket

        next_game = bracket[next_round_key].get(value['next_game_key'])
        
        if next_game['team_1'].get('name') is None:
            next_game['team_1'] = {
                    'name': winner['name'],
                    'BPI': winner['BPI']
                }
        else:
            next_game['team_2'] = {
                    'name': winner['name'],
                    'BPI': winner['BPI']
                }

        bracket[next_round_key][value['next_game_key']] = next_game

    return bracket

if __name__ == '__main__':
    main()