# coding=utf-8
#pylint: disable-msg=C0103
"""
Twitter module for Funkshelper/Sopel -- allows users to vote on tweets and ops
to post them.

Licensed under Mozilla Public License Version 2.

"""

import re
import readline
import datetime
import os
from os import path
from os.path import isfile, exists
import shutil
import glob
import string
from sopel import bot, coretasks
from sopel.module import commands, rule
from sopel.bot import Sopel, Trigger
from sopel import web, tools
from sopel import irc
from sopel.module import commands, rule, example, interval
from sopel.config.types import ValidatedAttribute, StaticSection
from sopel.module import commands, priority, OP, HALFOP, require_privilege, require_chanmsg
from sopel.tools import Identifier, target
import twitter

api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

@commands('twitter')
@rule('$nickname twitter')
def twitter_info(bot, trigger):
    """Provides information about the twitter feed as well as the latest tweet."""
    with open('/var/www/py/tweets.txt', 'w') as pretwits:
        pretwits.close()
    user = 'realWoodcoin'
    statuses = api.GetUserTimeline(screen_name=user)
    for tweet in reversed(statuses):
        with open('/var/www/py/tweets.txt', 'w') as twits:
            twits.write(tweet.text)
            twits.close()
    twitsy = open('/var/www/py/tweets.txt', 'r').readlines()[0]
    

    bot.say('Official Woodcoin Twitter page is http://twitter.com/realWoodcoin and our most recent tweet is:')
    bot.say('        ' + twitsy)
    bot.say('Say .tweetpropose to propose our next tweet and allow other members of the room to vote on it.')
    
    
@commands('tweethelp', 'twitterhelp')
@rule('$nickname tweethelp')
def twitter_help(bot, trigger):
    """"Private messages twattage.py help information to user"""
    bot.say('Sending you a list of Twitter-related commands, ' + trigger.nick)
    bot.say('Official Woodcoin Twitter page is http://twitter.com/realWoodcoin', trigger.nick)
    bot.say('Funkshelper Twitter commands are:', trigger.nick)
    bot.say('.twitter - provides feed info / latest tweet', trigger.nick)
    bot.say('.toptweet - provides latest tweet', trigger.nick)
    bot.say('.tweetpropose, .proposetweet - logs a user proposal of a tweet for voting', trigger.nick)
    bot.say('.tweetvote <#> - casts vote on chosen tweet to support', trigger.nick)

@require_privilege(OP, 'You are not a channel operator.')
@commands('call_tweet_vote')
def call_tweet_vote_manual(bot, trigger):
    """Manually lists proposed tweets. Only available to a channel operator."""
    bot.say('The following tweets are currently being considered for inclusion in our Twitter timeline. Each Tweet must have a majority of the room\'s approval before being posted.')
    tweetpath = '/var/www/py/tweets/'
    text = glob.glob(os.path.join(tweetpath, '*.txt'))
    for file in text:
        with open(file) as f:
            rawTweetCnts = [line.rstrip('\n') for line in f]
            for line in rawTweetCnts[:2]:
                tweetCnts = line
        tmp_filename = file.replace("/var/www/py/tweets/", "")
        filenameish = tmp_filename.replace(".txt", "")
        bot.say(filenameish + ' : ' + tweetCnts)
    bot.say('To vote for a tweet, say .voteTweet <#>. To vote against it, do nothing.')

@commands('post_tweet')
@rule('$nickname post_tweet')
@require_privilege(OP, 'You are not a channel operator.')
def write_tweet_ops(bot, trigger):
    """Allows a channel operator to post a tweet manually."""
    if len(trigger.group(2)) > 140:
        bot.reply('Your tweet is too fucking long! 140 characters or less!')
    else:
        api.PostUpdate(trigger.group(2))
        bot.reply('Your tweet has been posted. Say .toptweet to verify.')

@commands('toptweet')
@rule('$nickname toptweet')
def latest_tweet_display(bot, trigger):
    """Displays latest tweet."""
    with open('/var/www/py/tweets.txt', 'w') as pretwits:
        pretwits.close()
    user = 'realWoodcoin'
    statuses = api.GetUserTimeline(screen_name=user)
    for tweet in reversed(statuses):
        with open('/var/www/py/tweets.txt', 'w') as twits:
            twits.write(tweet.text)
            twits.close()
    twitsy = open('/var/www/py/tweets.txt', 'r').readlines()[0]
    bot.say('Latest tweet:' + twitsy)

@commands('tweetpropose', 'proposetweet')
@rule('$nickname twitter')
def propose_tweet(bot, trigger):
    """Stores a proposed tweet and associated files in /var/www/py/tweets."""
    if not trigger.group(2):
        return bot.reply('To use this properly you gotta say ".tweetpropose <tweet>"')
    if len(trigger.group(2)) > 140:
        bot.reply('Your tweet is too fucking long! 140 characters or less!')
    sequence = ""
    userList = bot.users
    userListPreOut = len(userList)
    userListOut = int(userListPreOut) - 2
    userName = trigger.nick
    tweet_file = "/var/www/py/tweets/tweet%s.txt"
    tweetPop = "/var/www/py/tweets/tweet%s.pop"
    tweetVoteCount = "/var/www/py/tweets/tweet%s.cnt"
    tweetLog = "/var/www/py/tweets/tweet%s.log"
    while isfile(tweetVoteCount % sequence):
        sequence = int(sequence or "1") + 1
    tweetVoteCount = tweetVoteCount % sequence
    initWriteTweetVoteCount = open(tweetVoteCount, 'w')
    initWriteTweetVoteCount.close()
    writeTweetVoteCount = open(tweetVoteCount, 'r+')
    writeTweetVoteCount.write('0')
    while isfile(tweet_file % sequence):
        sequence = int(sequence or "1") + 1
    tweet_file = tweet_file % sequence
    initialize_tweet = open(tweet_file, 'w')
    initialize_tweet.close()
    new_tweet = open(tweet_file, 'r+')
    new_tweet.write(str(trigger.group(2)))
    while isfile(tweetPop % sequence):
        sequence = int(sequence or "1") + 1
    tweetPop = tweetPop % sequence
    initWriteTweetPop = open(tweetPop, 'w')
    initWriteTweetPop.close()
    writeTweetPop = open(tweetPop, 'r+')
    writeTweetPop.write(str(userListOut))
    while isfile(tweetLog % sequence):
        sequence = int(sequence or "1") + 1
    tweetLog = tweetLog % sequence
    initWriteTweetLog = open(tweetLog, 'w')
    initWriteTweetLog.close()
    writeTweetLog = open(tweetLog, 'r+')
    writeTweetLog.write('Tweet proposed by ' + userName)
    bot.reply('Your tweet has been logged. Every 45 minutes I will ask for a vote from the room.')

@commands('votetweet', 'tweetvote')
@rule('$nickname votetweet')
def vote_on_tweet(bot, trigger):
    """Allows users to vote on a selected tweet."""
    if not trigger.group(2):
        bot.reply('Vote for WHICH tweet?')
    tweetNumber = trigger.group(2)
    userName = trigger.nick
     #opens tweet#
    selectedTweet = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.txt'
    voteLog = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.log'
    votePopFile = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.pop'
    voteCount = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.cnt'
    # the following section needs repair
        #  it is supposed to check whether the nick already appears
        # if it is already appears, it is supposed to prevent the vote
    with open(voteLog, 'a+') as logVote:
        voterLog = logVote.read()
        if voterLog.find(userName) != -1:
            bot.reply('You have already voted or you proposed this fucking tweet, you cheat!')
        else:
            logVote.write('\n' + userName)
            with open(voteCount, 'r+') as voting:
                rawVoteCnt = [line.rstrip('\n') for line in voting]
                for line in rawVoteCnt:
                    currentCount = int(line)
                    currentCount += 1
                    voting.write(str(currentCount))
    with open(selectedTweet, 'r+') as f:
        rawTweetCnts = [line.rstrip('\n') for line in f]
        for line in rawTweetCnts:
            tweetText = line
    newVoteCount = str(currentCount)
    #checks vote count against userCount
    with open(votePopFile) as f3:
        votePop = f3.readline()
        neededVotes = float(votePop) * 0.8
        if neededVotes < int(currentCount):
            approved_tweet = True
        else:
            approved_tweet = False
    if approved_tweet != True:
        bot.reply('Your vote has been cast for tweet #' + str(tweetNumber) + '. Tweet currently has ' + str(newVoteCount) + ' votes.')
    elif approved_tweet is True:
        bot.reply('Your vote has allowed ' + str(tweetNumber) + '-- "' + str(tweetText) + '" --' + 'to be posted at http://twitter.com/realWoodcoin')
        api.PostUpdate(tweetText)
        bot.say('To check latest tweet, use .toptweet')
        logdate = str(datetime.date.today().strftime("%j"))
        lognow = str(datetime.datetime.now().strftime("%H%M"))
        if not os.path.exists('/var/www/py/tweets/archived/' + logdate):
            os.mkdir('/var/www/py/tweets/archived/' + logdate)
        shutil.move(selectedTweet, '/var/www/py/tweets/archived/' + logdate + '/' + tweetNumber + '-' + lognow + '.txt')
        shutil.move(voteLog, '/var/www/py/tweets/archived/' + logdate + '/' + tweetNumber + '-' + lognow + '.log')
        shutil.move(votePopFile, '/var/www/py/tweets/archived/' + logdate + '/' + tweetNumber + '-' + lognow + '.pop')
        shutil.move(voteCount, '/var/www/py/tweets/archived/' + logdate + '/' + tweetNumber + '-' + lognow + '.cnt')


