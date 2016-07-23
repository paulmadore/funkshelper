# coding=utf-8
"""
Experimental functions for funkshelper
"""

from __future__ import unicode_literals
import random
import re
from sopel import bot, coretasks
from sopel.module import commands, rule
from sopel.bot import Sopel
from sopel import web, tools
from sopel.module import commands, rule, example
from sopel.config.types import ValidatedAttribute, StaticSection

'''
future: 

requires: https://github.com/bear/python-twitter/blob/master/examples/tweet.py

'''

'''
.raffles - lists currently running raffles
.newraffle <name> - create a new raffle, with description of prizes
.raffleticket <name_of_raffle_to_be_entered> - other users can join in the raffle
'''

'''
flow of .newraffle:
    <user>: .newraffle <raffle_name>
    funkshelper via capture()): what is the prize of <raffle_name>?
    <user>: <prize_name>
    funkshelper: will there be a cost for international shipping? (options: yes, no, n/a)
    <user>: <yes/no/n\a>
    funkshelper: how much is each raffle ticket (in woodcoins or USD, which will be converted to logs -- if using USD, please preface with $)?
    <user>: <raffle_cost>
    funkshelper: finally, when is the drawing date for the raffle? (valid formats: 01/01/2020, 1 Jan 2020, Jan 1, 2020)
    <user>: <drawing_date>
    funkshelper: excellent. 
'''

'''
capture()
captures information about raffle, to include:
    prize
        requests image of prize
        requests caveats such as international shipping
    ticket cost
    drawing date
'''

def capture():
    pass


'''
flow of .raffleticket:
    <user>: .raffleticket <raffle_name>
    <
'''

