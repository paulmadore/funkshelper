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
import woodcoin
from datetime import datetime
import json
from sopel.module import commands, rule
from sopel.bot import Sopel
import requests
import os
from urllib.request import urlopen
from requests_testadapter import Resp

woodcoin.SelectParams(mainnet)

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)

requests_session = requests.session()
requests_session.mount('file://', LocalFileAdapter())

loginjson = requests_session.get('file:///var/www/py/sopel/modules/woodcoin-details.json')
loginjson_text = loginjson.text
loginjsonoutput = json.loads(loginjson_text)
login = loginjsonoutput[0]['login']
loginpw = str(login)

pwjson = requests_session.get('file:///var/www/py/sopel/modules/woodcoin-details.json')
pwjson_text = pwjson.text
pwjsonoutput = json.loads(pwjson_text)
pw = pwjsonoutput[0]['passwd']
passwd = str(pw)

@commands('diffic', 'getdifficulty')
@rule('$nickname diffic')
def difficultyD(bot, trigger):
    user = 'woodcoinrpc'
    password = '9Bicycle**-->'
    rpconn = AuthServiceProxy("http://%s:%s@woodcoin.xyz:9338"%(user, password))
    diff = rpconn.info()
    getdiff = diff.difficulty
    
    return bot.reply('Network chopping difficulty is ' + getdiff)