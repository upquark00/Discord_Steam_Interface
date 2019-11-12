'''
This module imports information from a Steam user's session.

Annotated on 11/10/2019 @ 14:20:00 PDT 
Author: Upquark00

'''

import requests

from credentials import API_key, steam_ID, BOT_TOKEN

class SteamUser():
    '''Create an object holding a player's account information and current status.'''
    
    def __init__(self, steam_ID, API_key):
        self.API_url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=' \
        + API_key +'&steamids=' + steam_ID
        self.info = self.get_user_info()
        self.active_game = self.get_active_game(self.info) 
        self.name = self.info['personaname']
        self.status = self.get_player_status(self.info)
        # profile_url = 'https://steamcommunity.com/profiles/' + steam_ID
        
    def get_user_info(self):
        '''Returns a dict containing Steam information for one player using the
        Steam API. Requires the desired player's user ID and a valid API key.'''
        response = requests.get(self.API_url)
        
        if response.status_code != 200:
            raise Exception('Request unsuccessful; returned code ' + str(response.status_code) \
            + ': ' + str(requests.status_codes._codes[response.status_code][0]))
        else:
            print('Success! API responded to call.')
            self.__player_info = response.json()['response']['players'][0]
        return self.__player_info
    
    def get_player_status(self, player_info_dict):
        
        '''Returns the player's Steam status as a Discord status type.
        
        STEAM STATUS        | STEAM STATE | DISCORD STATUS
        'Offline'           |      0      | 'Offline'
        'Online'            |      1      | 'Online'
        'Busy'              |      2      | 'dnd'
        'Away'              |      3      | 'Idle'
        'Snooze'            |      4      | 'Idle'
        'Looking to trade'  |      5      | 'Online'
        'Looking to play'   |      6      | 'Online'
        
        '''

        status_list = {0: 'offline', 1: 'online', 3: 'dnd', 4: 'idle', 5: 'idle', 6: 'online', 7: 'online'}
        steam_state = player_info_dict['personastate']
        return status_list[steam_state]
        
    def get_active_game(self, player_info_dict):
        '''Returns the name of the Steam game that the player is currently playing. 
        If not currently playing anything, return False.'''
        
        try:
            self.__game = player_info_dict['gameextrainfo']
            game_name = self.__game
        except KeyError:  
            game_name = False
        return game_name 
    
print(API_key, steam_ID, BOT_TOKEN)
player = SteamUser(steam_ID, API_key)
