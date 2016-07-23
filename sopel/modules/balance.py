# drunk module
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import os
from os import path
import random
import datetime
from datetime import datetime
import json
from sopel.module import commands, rule
from sopel.bot import Sopel
import urllib.request
import requests

@commands('bal', 'checkbal')
@rule('$nickname checkbal')
def getBalance(bot, trigger):

    if not trigger.group(2):
        return bot.reply('check what balance?')
    address = trigger.group(2)
    
    addressBalance = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/addressbalance/' + address)
    balPlain = addressBalance.read().decode("utf8")
    height = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    text = height.read().decode("utf8")
    return bot.reply('Balance of ' + address + ' is ' + balPlain + ' at block ' + text)


@commands('richlist', 'richest')
@rule('$nickname richlist')
def richList(bot, trigger):
    outputTime = modification_date('/var/www/py/richlist.txt')   
    f = open('/var/www/py/richlist.txt')
    for line in iter(f):
        bot.say(line)
    f.close()
    return bot.say('Accurate as of ' + str(outputTime) + '. For a more updated list, visit http://bit.do/logRichList or http://bit.do/CryptoGuruLogRichList.')

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)
    