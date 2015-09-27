# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:03:42 2015

@author: Gal Bien
"""
import pymongo as pm
import requests
DATABASE_NAME = 'IsraelLeagueDB' 
Q_LEN = 10*60
OT_LEN = 5*60

# Initializing the DB
#---------------------
connection_string ='mongodb://localhost'
connection = pm.MongoClient(connection_string)
db = connection.get_database(DATABASE_NAME)

def get_collection_json(t):
    return {
        'teams': requests.get('http://basket.co.il/pbp/json/teams.json'),
        'players': requests.get('http://basket.co.il/pbp/json/players.json'),
        'games': requests.get('http://basket.co.il/pbp/json/games.json'),
    }[t]


def get_live_game(ex_id):
    link = 'http://basket.co.il/pbp/json_live/{0}_sbs.json'.format(ex_id)
    response = requests.get(link)
    return response.json()


def insert_collection(collection_name):
    db.create_collection(collection_name)


def insert_document(dic, collection_name):
    print db.get_collection(collection_name).insert(dic)
    

def update_collection(collection_name):
    response = get_collection_json(collection_name)
    dict_list = response.json()[0][collection_name]
    for d in dict_list:
        if db.get_collection(collection_name).find(d).count() == 0:
            insert_document(d, collection_name)

        
def update_live_games():
    g_ex_ids = db.get_collection('games').find({},{'ExternalID':1})
    for g_ex_id in g_ex_ids:
        ex_id = g_ex_id['ExternalID']
        game = get_live_game(ex_id)
        if db.get_collection('live_games').find(game).count() == 0:
            insert_document(game, 'live_games')


# Technical Functions
#---------------------

def quarter_time(q=1):
    ''' Returns the time when the quarter ends'''
    if q <= 4:
        return (q-1)*Q_LEN
    else :
        return 4*Q_LEN+(q-4)*OT_LEN


def cursor2list(cursor):
    lst = []
    for i in cursor:
        lst.append(i)
    return lst
    
    
def get_actions(live_game):
    return live_game['result']['actions']


def strtime2number(s):
    ''' The Given format is MM:SS '''
    c = s.find(':')
    return int(s[:c])*60+int(s[c+1:])


def action_time(action):
    ''' 
    Return the time of the action in seconds since the beginning of the game
    '''
    if not action['type'] == 'quarter':
        return quarter_time(action['quarter']) + strtime2number(action['quarterTime'])
    else:
        if action['parameters']['type'] == 'end-of-quarter':
            return quarter_time(action['quarter']+1)
        else:
            return quarter_time(action['quarter'])

            
def adding_real_time(live_game):
    actions = get_actions(live_game)
    for a in actions:
        a['time'] = action_time(a)
    
    
    
    