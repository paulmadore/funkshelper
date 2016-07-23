# drunk module
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import os
import random
from datetime import datetime
import json
from sopel.module import commands, rule
from sopel.bot import Sopel
import urllib.request

@commands('ale', 'drink')
@rule('$nickname ale')
def serveDrink(bot, trigger):
    bal = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/addressbalance/WbeercMznP9v5gLgWZW8KqkPssAquBwErS')
    balPlain = bal.read().decode("utf8")
    height = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    text = height.read().decode("utf8")
    height2 = int(float(text))
    last = height2 + 1
    sendAt = str(last)
    block = str(height2)
    with open('bar.log', 'w+') as f:
        f.write(balPlain)
        f.close()
    return bot.reply('Please send 1 log or more to WbeercMznP9v5gLgWZW8KqkPssAquBwErS before block ' + sendAt + '. Current block is ' + text + ' . At block ' + sendAt + ' say .sent or .paid')

@commands('sent', 'paid', 'tab')
@rule('$nickname sent')
def sentFunds(bot, trigger):
    beerType = ['Busch Signature Copper Lager', 'Fosters', 'Steel Reserve', \
                'Olde English', 'Southern Blonde', 'Goosehead', 'Guinness', \
                'Stout', 'Cunt Spice Rum Brew', 'Amber Boch', 'Dos Equus',
                'Modelo', 'Corona', 'Flat Tire', 'Wild Stallion', 'Side Pocket']
    bal = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/addressbalance/WbeercMznP9v5gLgWZW8KqkPssAquBwErS')
    balPlain = bal.read().decode("utf8")
    balance = open('bar.log')
    for line in balance.readlines():
        if line not in balPlain:
            balance.close()
            newbalance = open('bar.log', 'w+')
            newbalance.write(str(balPlain))
            newbalance.close()
            return bot.reply('Thank you for your patronage. Enjoy a ' + random.choice(beerType) + '!!!')
        elif line in balPlain:
            return bot.reply('Funds not yet received.')
        else:
            return bot.reply('Funds not yet received. How about paying for your drink!?')
