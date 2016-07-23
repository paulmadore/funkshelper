#!/usr/bin/python3
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
from woodcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
import json
import jsonrpc
from sopel.module import commands, rule
from sopel.bot import Sopel
import requests
import os
from urllib.request import urlopen

loginjson = requests.get('woodcoin-details.json')
loginjson_text = loginjson.text
loginjsonoutput = json.loads(loginjson_text)
login = loginjsonoutput['login']

pwjson = requests.get('woodcoin-details.json')
pwjson_text = pwjson.text
pwjsonoutput = json.loads(pwjson_text)
pw = pwjsonoutput['passwd']

@commands('diffic', 'getdifficulty')
@rule('$nickname diffic')
def difficulty(bot, trigger):
    rpconn = (AuthServiceProxy("http://%s:%s@127.0.0.1:9338"%(login, pw)))
    diff = rpconn.getdifficulty
    getdiff = (rpcconn.getdifficulty(diff))
    return bot.reply('Network chopping difficulty is ' + getdiff)