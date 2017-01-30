# coding=utf-8
"""
Woodcoin Network Status Module copyright 2015 phm.link
Licensed under Mozilla Public License Version 2.

Help with lastsellprice() json calls was provided by pride@bitbucket.org

Synopsis: a module that will report various statistics from the Woodcoin network.
Specifically, current hash rate, difficulty, coin supply, rich list, etc. 
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from datetime import datetime
import json
from sopel.module import commands, rule
from sopel.bot import Sopel
import urllib
import urllib.request
import requests
import os
import random


@commands('genesis')
@rule('$nickname genesis')
def genesisBlock(bot, trigger):
    block0 = '010000000000000000000000000000000000000000000000000000000000000000000000d508b7916ec00595c1f8e1c767dc3b37392a5e68adf98118bca80a2ed58331d614138173241e0ffff015911890101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff3804ffff001d010430426172756b204b68617a61642e202042544320426c6f636b20333236313733206e6f6e63653a20383738303136363536ffffffff010000000000000000 '
    bot.say('Yes, this information can be a pain to compile in a sane way.')
    bot.say('After much research, I find a raw hex of')
    bot.say(block0)
    return bot.say('regarding Woodcoin block 00000000.')


@commands('abt', 'about')
@rule('$nickname about')
def botinfo(bot, trigger):
    maint = 'phm@woodcoin.org'
    addr =  'WiPHMipxoJWr2Mw1AvPHvaMpzQfzTBLNu4'
    originalbot = 'sopel//sopel.chat'
    return bot.say('This bot is modified and maintained by ' + maint + ' and is also based on ' + originalbot + '. You can contribute to my hosting by sending logs to ' + addr + '.')

@commands('price', 'lastprice')
@rule('$nickname price')
def lastsellprice(bot, trigger):
    raw = requests.get('https://c-cex.com/t/log-btc.json')
    raw_text = raw.text
    raw_json = json.loads(raw_text)
    output = raw_json['ticker']['lastprice']
    return bot.reply("{:.8f}".format(output) + 'BTC')

@commands('usd')
@rule('$nickname value')
def dollar(bot, trigger):
    raw = requests.get('https://c-cex.com/t/log-usd.json')
    raw_text = raw.text
    raw_json = json.loads(raw_text)
    output = raw_json['ticker']['lastprice']
    usd = "{:.8f}".format(output)
    return bot.reply('The current US dollar valaution of a LOG is $' + usd)

@commands('woodcoin')
@rule('$nickname woodcoin')
def woodcoinPrice(bot, trigger):
    raw = requests.get('https://api.woodcoinaverage.com/ticker/global/USD')
    raw_text = raw.text
    raw_json = json.loads(raw_text)
    output = raw_json['last']
    priceBitcoin = str(output)
    nickName = ['mothafuckah', 'you lazy bitch', 'love, fucking web search', 'you dirty cunt', 'but why does that matter?', 'tweedle-twat', 'traitor', 'anvil-dropping slut', 'you fucking tunnel-worm', 'worthless cave gherkin', 'm\'lady']
    return bot.reply('Current price of them woodcoins is $' + priceBitcoin + ' each, ' + random.choice(nickName) + '.')

@commands('fiat')
@rule('$nickname fiat')
def fiatvalue(bot, trigger):
    raw = requests.get('https://c-cex.com/t/log-usd.json')
    raw_text = raw.text
    raw_json = json.loads(raw_text)
    output = raw_json['ticker']['lastprice']
    usd = "{:.8f}".format(output)
    exch = requests.get('')
    exch_text = exch.text
    exch_json = json.loads(exch_text)
    gbp = exch_json['quotes']['USDGBP']
    cny = exch_json['quotes']['USDCNY']
    rup = exch_json['quotes']['USDINR']
    rub = exch_json['quotes']['USDRUB']
    eur = exch_json['quotes']['USDEUR']
    gbpconv = gbp * output
    cnyconv = cny * output
    rupconv = rup * output
    rubconv = rub * output
    eurconv = eur * output
    gbp80 = "{:.8f}".format(gbpconv)
    cny80 = "{:.8f}".format(cnyconv)
    rup80 = "{:.8f}".format(rupconv)
    rub80 = "{:.8f}".format(rubconv)
    eur80 = "{:.8f}".format(eurconv)
    fiatmsg = 'The current fiat valuations of our beloved LOGs are: '
    usdmsg = ' US Dollar: $'
    gbpmsg = ' Pounds Sterling: £'
    cnymsg = ' Chinese Yuan: ¥'
    rupmsg = ' Indian Rupee: ₹'
    rubmsg = ' Russian Ruble: ₽'
    eurmsg = ' Euro: €'
    blkht = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    blkht_text = blkht.text
    blockheight = blkht_text
    blockmsg = ' Accurate at block #'
    return bot.reply(fiatmsg + usdmsg + usd + ' -|-' + gbpmsg + gbp80 + ' -|-' + eurmsg + eur80 + ' -|-' + cnymsg + cny80 + ' -|-' + rubmsg + rub80 + ' -|-' + rupmsg + rup80 + ' ~~' + blockmsg + blockheight + '.')

@commands('coins', 'supply')
@rule('$nickname supply')
def coinsupply(bot, trigger):
    height = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    raw = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/totalbc/' + height)
    raw_text = raw.text
    amt = raw_text
    return bot.reply('The current number of LOGS (woodcoins) in existence is ' + amt)

@commands('diff', 'difficulty')
@rule('$nickname diff')
def difficulty(bot, trigger):
    raw = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/getdifficulty')
    raw_text = raw.text
    diff = raw_text
    return bot.reply('Woodcoin mining difficulty is currently ' + diff)

@commands('hash', 'nethash')
@rule('$nickname hash')
def networkhash(bot, trigger):
    height = urllib.request.urlopen('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    text = height.read().decode("utf8")
    height2 = int(float(text))
    last = height2 - 1
    raw = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/nethash/1/{}/{}?format=json'.format(last, height2))
    raw_text = raw.text
    raw_json = json.loads(raw_text)
    nethash = str(raw_json)
    nethash2 = nethash.split(",")
    nethash3 = nethash2[7]
    nethash4 = str(nethash3).replace(' ', '')[:-3].upper()
    nethash5 = nethash4[1:]
    nethash6 = int(float(nethash5))
    nethash7 = nethash6 / 1000000000
    nethash8 = str(nethash7)
    return bot.reply('The Woodcoin mining network presently has a hashrate of ' + nethash8 + ' GH/s ')

@commands('height', 'blockheight', 'blocks')
@rule('$nickname blockheight')
def blockheight(bot, trigger):
    raw = requests.get('http://explorer.woodcoin.org/chain/Woodcoin/q/getblockcount')
    raw_text = raw.text
    blocknum = raw_text
    return bot.reply('Number of blocks in the Woodcoin block chain: ' + blocknum)