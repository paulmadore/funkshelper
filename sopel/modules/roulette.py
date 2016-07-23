# coding=utf-8
"""
Block-Roulette.com Module 
copyright 2015 phm.link
Licensed under Mozilla Public License Version 2.


Synopsis: monitor all site addresses as well as output winning bet for each block
and recent win information.
"""
from __future__ import unicode_literals
from __future__ import division
import json
import jsonrpc
import sopel.module
from sopel.module import commands, rule
from sopel.formatting import color, colors, bold
from sopel.bot import Sopel
import requests
import storage

@sopel.module.interval(180)
@commands('trigger')
@rule('$nick blockwatch')
def blockwatchfornew(bot, trigger):
    if "#woodcoin" in bot.channels:
        evenred = [12, 14, 16, 18, 30, 32, 34, 36]
        evenblack = [2, 4, 6, 8, 10, 20, 22, 24, 26, 28]
        oddred = [1, 3, 5, 7, 9, 19, 21, 23, 25, 27]
        oddblack = [11, 13, 15, 17, 29, 31, 33, 35]

        check1 = requests.get('https://blockchain.info/latestblock')
        boodlydoo = check1.text
        rawboodly = json.loads(boodlydoo)
        sayit = rawboodly['hash']
        almostwin = sayit[-5:]
        almostwinning = '0x' + almostwin
        nearlywin = int(almostwinning, 16)
        victory = nearlywin % 38        
        
        if victory in evenred:
            victorycolor = 'red'
            victorycolor = color(victorycolor, colors.RED)
            victoryevodd = 'even'
            victoryevodd = color(victoryevodd, colors.GREEN)
            victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
        elif victory in evenblack:
            victorycolor = 'black'
            victoryevodd = 'even'
            victoryevodd = color(victoryevodd, colors.GREEN)
            victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
        elif victory in oddred:
            victorycolor = 'red'
            victorycolor = color(victorycolor, colors.RED)
            victoryevodd = 'odd'
            victoryevodd = color(victoryevodd, colors.GREEN)
            victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
        elif victory in oddblack:
            victorycolor = 'black'
            victoryevodd = 'odd'
            victoryevodd = color(victoryevodd, colors.GREEN)
            victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
        else:
            victorycolor = ' '
            victoryoutput = ' OTHER'
            victoryoutput = color(victoryoutput, colors.BLUE)
        check2 = {}
        storage.data['check2'] = sayit
        check3 = storage.data['check2']
        latest = str(victory) + victoryoutput
        if check2 == check1:
            return bot.say('no new blocks')
        else: 
            return bot.say('Latest winning spin ' + latest)
  
@commands('lastwin')
def lastwinblockraw(bot, trigger):
    evenred = [12, 14, 16, 18, 30, 32, 34, 36]
    evenblack = [2, 4, 6, 8, 10, 20, 22, 24, 26, 28]
    oddred = [1, 3, 5, 7, 9, 19, 21, 23, 25, 27]
    oddblack = [11, 13, 15, 17, 29, 31, 33, 35]
    
    raw = requests.get('https://blockchain.info/latestblock')
    boodlydoo = raw.text
    rawboodly = json.loads(boodlydoo)
    sayit = rawboodly['hash']
    almostwin = sayit[-5:]
    almostwinning = '0x' + almostwin
    nearlywin = int(almostwinning, 16)
    victory = nearlywin % 38
    if victory in evenred:
        victorycolor = 'red'
        victorycolor = color(victorycolor, colors.RED)
        victoryevodd = 'even'
        victoryevodd = color(victoryevodd, colors.GREEN)
        victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
    elif victory in evenblack:
        victorycolor = 'black'
        victoryevodd = 'even'
        victoryevodd = color(victoryevodd, colors.GREEN)
        victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
    elif victory in oddred:
        victorycolor = 'red'
        victorycolor = color(victorycolor, colors.RED)
        victoryevodd = 'odd'
        victoryevodd = color(victoryevodd, colors.GREEN)
        victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
    elif victory in oddblack:
        victorycolor = 'black'
        victoryevodd = 'odd'
        victoryevodd = color(victoryevodd, colors.GREEN)
        victoryoutput = ', ' + victorycolor + ', ' + victoryevodd
    else:
        victorycolor = ' '
        victoryoutput = ' OTHER'
        victoryoutput = color(victoryoutput, colors.BLUE)
    return bot.reply(str(victory) + victoryoutput)

@commands('lastfive')
def lastfivewins(bot, trigger):
    evenred = [12, 14, 16, 18, 30, 32, 34, 36]
    evenblack = [2, 4, 6, 8, 10, 20, 22, 24, 26, 28]
    oddred = [1, 3, 5, 7, 9, 19, 21, 23, 25, 27]
    oddblack = [11, 13, 15, 17, 29, 31, 33, 35]
    
    raw = requests.get('https://blockchain.info/latestblock')
    boodlydoo = raw.text
    rawboodly = json.loads(boodlydoo)
    sayit = rawboodly['hash']
    almostwin = sayit[-5]
    almostwinning = '0x' + almostwin
    nearlywin = int(almostwinning, 16)
    mostrecent = nearlywin % 38
    
    height = rawboodly['height']
    heightmin = int(height)
    fourthblk = heightmin - 1
    thirdblk = fourthblk - 1
    secondblk = thirdblk - 1
    firstblk = secondblk - 1
    
    fourth = requests.get('https://chain.so/api/v2/get_blockhash/BTC/' + str(fourthblk))
    fourthdoo = fourth.text
    fourthoodly = json.loads(fourthdoo)
    say4it = fourthoodly['data']['blockhash']
    almost4win = say4it[-5:]
    almost4winning = '0x' + almost4win
    nearly4win = int(almost4winning, 16)
    fourthmostrecent = nearly4win % 38
    
    third = requests.get('https://chain.so/api/v2/get_blockhash/BTC/' + str(thirdblk))
    thirdoo = third.text
    thirdoodly = json.loads(thirdoo)
    say3it = thirdoodly['data']['blockhash']
    almost3win = say3it[-5:]
    almost3winning = '0x' + almost3win
    nearly3win = int(almost3winning, 16)
    thirdmostrecent = nearly3win % 38
    
    second = requests.get('https://chain.so/api/v2/get_blockhash/BTC/' + str(secondblk))
    secondoo = second.text
    secondoodly = json.loads(secondoo)
    say2it = secondoodly['data']['blockhash']
    almost2win = say2it[-5:]
    almost2winning = '0x' + almost2win
    nearly2win = int(almost2winning, 16)
    secondmostrecent = nearly2win % 38
    
    first = requests.get('https://chain.so/api/v2/get_blockhash/BTC/' + str(firstblk))
    firstdoo = first.text
    firsthoodly = json.loads(firstdoo)
    say1it = firsthoodly['data']['blockhash']
    almost1win = say1it[-5:]
    almost1winning = '0x' + almost1win
    nearly1win = int(almost1winning, 16)
    firstmostrecent = nearly1win % 38
    
    if mostrecent in evenred:
        mostrecentcolor = 'red'
        mostrecentcolor = color(mostrecentcolor, colors.RED)
        mostrecentevodd = 'even'
        mostrecentevodd = color(mostrecentevodd, colors.GREEN)
        mostrecentoutput = ', ' + mostrecentcolor + ', ' + mostrecentevodd
    elif mostrecent in evenblack:
        mostrecentcolor = 'black'
        mostrecentevodd = 'even'
        mostrecentevodd = color(mostrecentevodd, colors.GREEN)
        mostrecentoutput = ', ' + mostrecentcolor + ', ' + mostrecentevodd
    elif mostrecent in oddred:
        mostrecentcolor = 'red'
        mostrecentcolor = color(mostrecentcolor, colors.RED)
        mostrecentevodd = 'odd'
        mostrecentevodd = color(mostrecentevodd, colors.GREEN)
        mostrecentoutput = ', ' + mostrecentcolor + ', ' + mostrecentevodd
    elif mostrecent in oddblack:
        mostrecentcolor = 'black'
        mostrecentevodd = 'odd'
        mostrecentevodd = color(mostrecentevodd, colors.GREEN)
        mostrecentoutput = ', ' + mostrecentcolor + ', ' + mostrecentevodd
    else:
        mostrecentcolor = ' '
        mostrecentoutput = ' OTHER'
        mostrecentoutput = color(mostrecentoutput, colors.BLUE)
        
    if fourthmostrecent in evenred:
        fourthmostrecentcolor = 'red'
        fourthmostrecentcolor = color(fourthmostrecentcolor, colors.RED)
        fourthmostrecentevodd = 'even'
        fourthmostrecentevodd = color(fourthmostrecentevodd, colors.GREEN)
        fourthmostrecentoutput = ', ' + fourthmostrecentcolor + ', ' + fourthmostrecentevodd
    elif fourthmostrecent in evenblack:
        fourthmostrecentcolor = 'black'
        fourthmostrecentevodd = 'even'
        fourthmostrecentevodd = color(fourthmostrecentevodd, colors.GREEN)
        fourthmostrecentoutput = ', ' + fourthmostrecentcolor + ', ' + fourthmostrecentevodd
    elif fourthmostrecent in oddred:
        fourthmostrecentcolor = 'red'
        fourthmostrecentcolor = color(fourthmostrecentcolor, colors.RED)
        fourthmostrecentevodd = 'odd'
        fourthmostrecentevodd = color(fourthmostrecentevodd, colors.GREEN)
        fourthmostrecentoutput = ', ' + fourthmostrecentcolor + ', ' + fourthmostrecentevodd
    elif fourthmostrecent in oddblack:
        fourthmostrecentcolor = 'black'
        fourthmostrecentevodd = 'odd'
        fourthmostrecentevodd = color(fourthmostrecentevodd, colors.GREEN)
        fourthmostrecentoutput = ', ' + fourthmostrecentcolor + ', ' + fourthmostrecentevodd
    else:
        fourthmostrecentcolor = ' '
        fourthmostrecentoutput = ' OTHER'
        fourthmostrecentoutput = color(fourthmostrecentoutput, colors.BLUE)
        
    if thirdmostrecent in evenred:
        thirdmostrecentcolor = 'red'
        thirdmostrecentcolor = color(thirdmostrecentcolor, colors.RED)
        thirdmostrecentevodd = 'even'
        thirdmostrecentevodd = color(thirdmostrecentevodd, colors.GREEN)
        thirdmostrecentoutput = ', ' + thirdmostrecentcolor + ', ' + thirdmostrecentevodd
    elif thirdmostrecent in evenblack:
        thirdmostrecentcolor = 'black'
        thirdmostrecentevodd = 'even'
        thirdmostrecentevodd = color(thirdmostrecentevodd, colors.GREEN)
        thirdmostrecentoutput = ', ' + thirdmostrecentcolor + ', ' + thirdmostrecentevodd
    elif thirdmostrecent in oddred:
        thirdmostrecentcolor = 'red'
        thirdmostrecentcolor = color(thirdmostrecentcolor, colors.RED)
        thirdmostrecentevodd = 'odd'
        thirdmostrecentevodd = color(thirdmostrecentevodd, colors.GREEN)
        thirdmostrecentoutput = ', ' + thirdmostrecentcolor + ', ' + thirdmostrecentevodd
    elif thirdmostrecent in oddblack:
        thirdmostrecentcolor = 'black'
        thirdmostrecentevodd = 'odd'
        thirdmostrecentevodd = color(thirdmostrecentevodd, colors.GREEN)
        thirdmostrecentoutput = ', ' + thirdmostrecentcolor + ', ' + thirdmostrecentevodd
    else:
        thirdmostrecentcolor = ' '
        thirdmostrecentoutput = ' OTHER'
        thirdmostrecentoutput = color(thirdmostrecentoutput, colors.BLUE)
        
    if secondmostrecent in evenred:
        secondmostrecentcolor = 'red'
        secondmostrecentcolor = color(secondmostrecentcolor, colors.RED)
        secondmostrecentevodd = 'even'
        secondmostrecentevodd = color(secondmostrecentevodd, colors.GREEN)
        secondmostrecentoutput = ', ' + secondmostrecentcolor + ', ' + secondmostrecentevodd
    elif secondmostrecent in evenblack:
        secondmostrecentcolor = 'black'
        secondmostrecentevodd = 'even'
        secondmostrecentevodd = color(secondmostrecentevodd, colors.GREEN)
        secondmostrecentoutput = ', ' + secondmostrecentcolor + ', ' + secondmostrecentevodd
    elif secondmostrecent in oddred:
        secondmostrecentcolor = 'red'
        secondmostrecentcolor = color(secondmostrecentcolor, colors.RED)
        secondmostrecentevodd = 'odd'
        secondmostrecentevodd = color(secondmostrecentevodd, colors.GREEN)
        secondmostrecentoutput = ', ' + secondmostrecentcolor + ', ' + secondmostrecentevodd
    elif secondmostrecent in oddblack:
        secondmostrecentcolor = 'black'
        secondmostrecentevodd = 'odd'
        secondmostrecentevodd = color(secondmostrecentevodd, colors.GREEN)
        secondmostrecentoutput = ', ' + secondmostrecentcolor + ', ' + secondmostrecentevodd
    else:
        secondmostrecentcolor = ' '
        secondmostrecentoutput = ' OTHER'
        secondmostrecentoutput = color(secondmostrecentoutput, colors.BLUE)
        

    if firstmostrecent in evenred:
        firstmostrecentcolor = 'red'
        firstmostrecentcolor = color(firstmostrecentcolor, colors.RED)
        firstmostrecentevodd = 'even'
        firstmostrecentevodd = color(firstmostrecentevodd, colors.GREEN)
        firstmostrecentoutput = ', ' + firstmostrecentcolor + ', ' + firstmostrecentevodd
    elif firstmostrecent in evenblack:
        firstmostrecentcolor = 'black'
        firstmostrecentevodd = 'even'
        firstmostrecentevodd = color(firstmostrecentevodd, colors.GREEN)
        firstmostrecentoutput = ', ' + firstmostrecentcolor + ', ' + firstmostrecentevodd
    elif firstmostrecent in oddred:
        firstmostrecentcolor = 'red'
        firstmostrecentcolor = color(firstmostrecentcolor, colors.RED)
        firstmostrecentevodd = 'odd'
        firstmostrecentevodd = color(firstmostrecentevodd, colors.GREEN)
        firstmostrecentoutput = ', ' + firstmostrecentcolor + ', ' + firstmostrecentevodd
    elif firstmostrecent in oddblack:
        firstmostrecentcolor = 'black'
        firstmostrecentevodd = ' odd'
        firstmostrecentevodd = color(firstmostrecentevodd, colors.GREEN)
        firstmostrecentoutput = ', ' + firstmostrecentcolor + ', ' + firstmostrecentevodd
    else:
        firstmostrecentcolor = ' '
        firstmostrecentoutput = ' OTHER'
        firstmostrecentoutput = color(firstmostrecentoutput, colors.BLUE)
    
    brcom = 'BLOCK-ROULETTE.com'
    brcom = color(brcom, colors.GREEN)
    
    bot.say('Last five winning bets at ' + brcom + ' are as follows:')
    bot.say(bold(str(mostrecent)) + str(mostrecentoutput) + ' at block ' + str(height) + '. ')
    bot.say(bold(str(fourthmostrecent)) + str(fourthmostrecentoutput) + ' at block ' + str(fourthblk) + '. ')
    bot.say(bold(str(thirdmostrecent)) + str(thirdmostrecentoutput) + ' at block ' + str(thirdblk) + '. ')
    bot.say(bold(str(secondmostrecent)) + str(secondmostrecentoutput) + ' at block ' + str(secondblk) + '. ')
    bot.say(bold(str(firstmostrecent)) + str(firstmostrecentoutput) + ' at block ' + str(firstblk) + '.')
    bot.say(bold('Information may be delayed. Do not rely on me for betting, as I am only a bot.'))
   





    
    

