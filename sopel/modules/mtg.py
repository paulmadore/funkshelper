# magic cards module
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
import requests

@commands('draw')
@rule('$nickname draw')
def drawCard(bot, trigger):
    filename = '/var/www/py/sopel/modules/mtgcreatures.txt'
    line_num = 0
    selected_line = ''
    with open(filename) as f:
        while 1:
            line = f.readline()
            if not line: break
            line_num += 1
            if random.uniform(0, line_num) < 1:
                selected_line = line
        card = selected_line.strip()
    cardDrawRaw = requests.get('https://api.deckbrew.com/mtg/cards?&multiverseid=' + card)
    cardDrawRawText = cardDrawRaw.text
    cardDrawRawJson = json.loads(cardDrawRawText)
    cardID = cardDrawRawJson[0]['id']
    cardDrawRawWithID = requests.get('https://api.deckbrew.com/mtg/cards/' + cardID)
    cardDrawRawWithIDText = cardDrawRawWithID.text
    cardDrawRawWithIDJson = json.loads(cardDrawRawWithIDText)
    cardName = cardDrawRawWithIDJson['name']
    creaturePower = cardDrawRawWithIDJson['power'][0]
    creatureToughness = cardDrawRawWithIDJson['toughness'][0]
    creatureColor = cardDrawRawWithIDJson['colors'][0]
    cardURLRaw = cardDrawRawWithIDJson['editions'][0]['image_url']
    cardURLGet = requests.get('https://coinurl.com/api.php?uuid=53759db04170a030904396&url=' + cardURLRaw)
    cardURLGetText = cardURLGet.text
    cardURL = str(cardURLGetText)
    bot.say(str(trigger.nick) + ' has drawn ' + cardName + '. This ' + creatureColor + ' creature has ' + creaturePower + '/' + creatureToughness + '. Say .draw and then .fight to challenge him in a fight. To view ' + cardName + ', visit ' + cardURL)
    

            