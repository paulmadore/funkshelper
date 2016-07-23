# coding=utf-8

# .twitter - displays twitter handle and last tweet sent, plus information on following commands
# .tweetpropose - allows any room member to propse the next tweet
# .tweetVote - member may call a vote on the tweet they have logged in .tweetpropose
# .tweetpost - if member gets majority of room to approve, tweet can be posted
import re
import readline
import os
from os import path
from os.path import isfile
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

@interval(3600)
def call_tweet_vote(bot, trigger):
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
    bot.say('To vote for a tweet, say .voteTweet <tweet#>. To vote against it, do nothing.')

@require_privilege(OP, 'You are not a channel operator.')
@commands('call_tweet_vote')
def call_tweet_vote_manual(bot, trigger):
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

@commands('testThing')
@rule('$nickname testThing')
def testThing(bot, trigger):
    pass

@commands('post_tweet')
@rule('$nickname post_tweet')
@require_privilege(OP, 'You are not a channel operator.')
def write_tweet_ops(bot, trigger):
    if len(trigger.group(2)) > 140:
        bot.reply('Your tweet is too fucking long! 140 characters or less!')
    else:
        api.PostUpdate(trigger.group(2))
        bot.reply('Your tweet has been posted. Say .toptweet to verify.')

@commands('toptweet')
@rule('$nickname toptweet')
def latest_tweet_display(bot, trigger):
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
    if not trigger.group(2):
        return bot.reply('To use this properly you gotta say ".tweetpropose <tweet>"')
    if len(trigger.group(2)) > 140:
        bot.reply('Your tweet is too fucking long! 140 characters or less!')
    sequence = ""
    userList = bot.users
    userListPreOut = len(userList)
    userListOut = int(userListPreOut) - 2
    tweet_file = "/var/www/py/tweets/tweet%s.txt"
    while isfile(tweet_file % sequence):
        sequence = int(sequence or "1") + 1
    tweet_file = tweet_file % sequence
    initialize_tweet = open(tweet_file, 'w')
    initialize_tweet.close()
    new_tweet = open(tweet_file, 'r+')
    new_tweet.write('0' + '\n' + str(trigger.group(2)) + '\n' + str(userListOut))
    bot.reply('Your tweet has been logged. Every hour I will ask for a vote from the room.')

@commands('votetweet')
@rule('$nickname votetweet')
def vote_on_tweet(bot, trigger):
    if not trigger.group(2):
        bot.reply('Vote for WHICH tweet?')
    tweetNumber = trigger.group(2)
    userName = trigger.nick
     #opens tweet#
    selectedTweet = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.txt'
    voteLog = '/var/www/py/tweets/tweet' + str(tweetNumber) + '.log'
    # breaks tweet file up into three variables
    with open(selectedTweet, 'r+') as f:
        rawTweetCnts = [line.rstrip('\n') for line in f]
        for line in rawTweetCnts[:1]:
            currentCount = int(line) + 1
            newVoteCount = str(currentCount)
            f.write(newVoteCount)
        for line in rawTweetCnts[:2]:
            tweetText = line
        for line in rawTweetCnts[:3]:
            votePop = line
    #adds 1 to line 0, which is the vote count
        
    #adds username to line 3, which is the voter registration line
    with open(voteLog, 'a') as f2:
            f2.write(userName)
    #checks vote count against userCount
    neededVotes = int(votePop) / 100 * 80
    if neededVotes < int(newVoteCount):
        approved_tweet = True
    else:
        approved_tweet = False
    if approved_tweet != True:
        bot.reply('Your vote has been cast for ' + str(tweetNumber) + '. Tweet currently needs ' + str(neededVotes) + ' votes and has ' + str(newVoteCount) + ' votes.')
    elif approved_tweet is True:
        bot.reply('Your vote has allowed ' + str(tweetNumber) + '-- "' + str(tweetText) + '" --' + 'to be posted at http://twitter.com/realWoodcoin')
        api.PostUpdate(tweetText)
        bot.say('To check latest tweet, use .toptweet')
        shutil.move(selectedTweet, '/var/www/py/tweets/archived' + selectedTweet)
        shutil.move(voteLog, '/var/www/py/tweets/archived' + voteLog)

