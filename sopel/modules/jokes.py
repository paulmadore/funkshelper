#!/usr/bin/python3
# coding=utf-8
"""
Chuck Norris and Other Jokes Module copyright 2015 phm.link
Licensed under Mozilla Public License Version 2.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import json
import jsonrpc
from sopel.module import commands, rule
from sopel.bot import Sopel
import requests
import os
from urllib.request import urlopen
import twitter

api = twitter.Api(consumer_key='CaFQsqiGusZvwCtoOpcfPA2bD',
                  consumer_secret='KMlNirFyJPj2Iq19DXe8Rq6P4njuO6WXt6Me9PgIBWzOvbcEkO',
                  access_token_key='720043744611840000-5DzeqNUwQrVFqM8yPd6E6QjDQ3xT2ic',
                  access_token_secret='PQBxas8CAEa9fiS8wYkyoTnwQ2qGg7ePmLB6bQi9sDvRt')


@commands('jokehelp', 'funny')
@rule('$nickname jokehelp')
def jokeModuleHelp(bot, trigger):
    return bot.reply('To get a general random joke, do .telljoke. To get a random Chuck Norris joke, say .joke. To get a random joke about yourself, say .jokeme. To get a random joke about someone else, say .chuckuser <username>. To get the latest tweet from Hulk Trump, do .trumptweet. To convert a sentence to Pirate, do .piratize. To convert a sentence to Yoda, do .yodize.')

@commands('joke')
@rule('$nickname joke')
def chuckNorrisJoke(bot, trigger):
    randomChuckJoke = 'http://api.icndb.com/jokes/random'
    jokeChuckRandom = requests.get(randomChuckJoke)
    jokeChuck = jokeChuckRandom.text
    jokeFinal = json.loads(jokeChuck)
    jokeFinalOutput = jokeFinal['value']['joke']
    bot.say(jokeFinalOutput)

@commands('jokeme')
@rule('$nickname jokeme')
def userJoke(bot, trigger):
    randomJoke = 'http://api.icndb.com/jokes/random?firstName=' + trigger.nick + '&lastName='
    jokeUserRandom = requests.get(randomJoke)
    jokeUser = jokeUserRandom.text
    jokeFinal = json.loads(jokeUser)
    jokeFinalOutput = jokeFinal['value']['joke']
    bot.say(jokeFinalOutput)
    
@commands('chuckuser')
@rule('$nickname chuckuser')
def userChuckJoke(bot, trigger):
    randomJoke = 'http://api.icndb.com/jokes/random?firstName=' + trigger.group(2) + '&lastName='
    jokeUserRandom = requests.get(randomJoke)
    jokeUser = jokeUserRandom.text
    jokeFinal = json.loads(jokeUser)
    jokeFinalOutput = jokeFinal['value']['joke']
    bot.say(jokeFinalOutput)
    
@commands('piratize')
@rule('$nickname piratize')
def convertToPirate(bot, trigger):
    pirateMain = 'http://isithackday.com/arrpi.php?text=' + trigger.group(2)
    pirateLocal = requests.get(pirateMain)
    pirateOutput = pirateLocal.text
    bot.reply(pirateOutput)
    
@commands('yodize')
@rule('$nickname yodize')
def convertToYoda(bot, trigger):
    yodized = requests.get('https://yoda.p.mashape.com/yoda?sentence=' + trigger.group(2),
            headers={
            "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
            "Accept": "text/plain"
  }
)
    output = yodized.text
    bot.say(output)

@commands('telljoke')
@rule('$nickname telljoke')
def tellRandomJoke(bot, trigger):
    randomJoke = 'http://tambal.azurewebsites.net/joke/random'
    jokeUserRandom = requests.get(randomJoke)
    jokeUser = jokeUserRandom.text
    jokeFinal = json.loads(jokeUser)
    jokeFinalOutput = jokeFinal['joke']
    bot.say(jokeFinalOutput)
    
@commands('trumptweet')
@rule('$nickname trumptweet')
def latest_tweet_display(bot, trigger):
    """Displays latest @HulkDonaldTrump tweet."""
    with open('/var/www/py/trumptweets.txt', 'w') as pretwits:
        pretwits.close()
    user = 'HulkDonaldTrump'
    statuses = api.GetUserTimeline(screen_name=user)
    for tweet in reversed(statuses):
        with open('/var/www/py/trumptweets.txt', 'w') as twits:
            twits.write(tweet.text)
            twits.close()
    twitsy = open('/var/www/py/trumptweets.txt', 'r').readlines()[0]
    bot.say('Latest tweet from Aspiring President Trump: ' + twitsy)
        