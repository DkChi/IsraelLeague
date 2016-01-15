# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 11:16:19 2015

@author: Gal Bien
"""
import utils
from collections import Counter
import sys
if r'D:\Gal\IsraelLeague\IsraelLeague' not in sys.path:
    sys.path.append(r'D:\Gal\IsraelLeague\IsraelLeague')


def made_shot(shot):
    return shot['parameters']['made'] == 'made'


def intersting_points(live_game, kind='fastBreak'):
    '''
    Kinds availabe: fastBreak, secondChancePoints, pointsFromTurnover
    '''
    actions = utils.get_actions(live_game)
    points = Counter()
    for a in actions:
        if a['type'] == 'shot':
            print a['parameters']
            if a['parameters'][kind]:
                print 'relevant ', 'made:', made_shot(a)
                points[a['teamId']] += a['parameters']['points']*made_shot(a)
    return points
