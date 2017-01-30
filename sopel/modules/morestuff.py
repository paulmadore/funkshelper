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
import time

@commands('moviequote')
@rule('$nickname moviequote')
def movieQuote(bot, trigger):
    quote = requests.post("https://andruxnet-random-famous-quotes.p.mashape.com/?cat=movies",
      headers={
        "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      }
    )
    quoteBody = quote.text
    quoteFinal = json.loads(quoteBody)
    quoteText = quoteFinal['quote']
    quoteAuthor = quoteFinal['author']
    bot.say(quoteText + '   (from "' + quoteAuthor + '")')
    
@commands('quote')
@rule('$nickname quote')
def famousQuote(bot, trigger):
    quote = requests.post("https://andruxnet-random-famous-quotes.p.mashape.com/?cat=famous",
      headers={
        "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      }
    )
    quoteBody = quote.text
    quoteFinal = json.loads(quoteBody)
    quoteText = quoteFinal['quote']
    quoteAuthor = quoteFinal['author']
    bot.say(quoteText + ' -- ' + quoteAuthor)
    
@commands('mathfact')
@rule('nickname mathfact')
def mathFact(bot, trigger):
    fact = requests.get("https://numbersapi.p.mashape.com/random/trivia?fragment=true&json=true&max=100000000&min=1",
  headers={
    "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
    "Accept": "text/plain"
  }
)
    factBody = fact.text
    factFinal = json.loads(factBody)
    factText = factFinal['text']
    number = factFinal['number']
    bot.say(str(number) + ' is ' + factText)
    
@commands('factabt')
@rule('nickname factabt')
def mathSpecificFact(bot, trigger):
    fact = requests.get("https://numbersapi.p.mashape.com/" + trigger.group(2) + "/math?fragment=true&json=true",
  headers={
    "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
    "Accept": "text/plain"
  }
)
    factBody = fact.text
    factFinal = json.loads(factBody)
    factText = factFinal['text']
    number = factFinal['number']
    bot.say(str(number) + ' is ' + factText)
    
@commands('gibberish')
@rule('$nickname gibberish')
def sayGibberish(bot, trigger):
    gibberishInit = open(str(time.time()) + '.txt', 'w').close()
    gibberishFile = gibberishInit
    gibberishInput = int(trigger.group(2))
    for _ in range(gibberishInput):
        gibberish = requests.get("https://wordsapiv1.p.mashape.com/words/?random=true",
        headers={
          "X-Mashape-Key": "7RNWkrbr2ymshIHSDARCfgVApFD7p1zhK8Kjsn4gzaFXaXCIhM",
          "Accept": "application/json"
        }
    )
        gibberishWord = gibberish.text
        gibberishOutput = json.loads(gibberishWord)
        gibText = gibberishOutput["word"]
        with open(gibberishFile, 'a') as outputFile:
            outputFile.write(gibText)
            outputFile.close()
        with open(gibberishFile, 'r') as gibberishOutputFinal:
            actualFinal = gibberishOutputFinal.read().replace('\n', ' ')
    bot.say(actualFinal)
    


