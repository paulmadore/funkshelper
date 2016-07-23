@commands('votetweet')
@rule('$nickname votetweet')
def vote_on_tweet(bot, trigger):
    tweetVoteCount = 0
    text = open('/var/www/py/votingUserList.txt', 'w')
    text.write(str(bot.users))
    text.close()
    textFile = open('/var/www/py/votingUserList.txt', 'r')
    userPlain = re.findall(r'\'(.+?)\'', textFile.read())
    textFile.close()
    textLast = open('/var/www/py/votingUserListCurrent.txt', 'w')
    textLast.write(" ".join(userPlain))
    userCount = len(textLast) - len(textLast.lstrip(' '))
    textLast.close()
    majorityVote = userCount / 100 * 75
    tweetRoll = open('/var/www/py/roomTweets.txt', 'r')
    for line in tweetRoll:
        if trigger.group(2) in line[:3]:
            tweetVoteCount += 1
            with open('/var/www/py/roomTweets.txt', 'r') as addVoteTweetRoll:
                voteTweetRoll = addVoteTweetRoll.readlines()
                voteTweetRoll[trigger.group(2)] = line + tweetVoteCount + '\n'
                addVoteTweetRoll.close()
            with open('/var/www/py/roomTweets.txt', 'w') as newAddVoteTweetRoll:
                newAddVoteTweetRoll.write(voteTweetRoll)
                newAddVoteTweetRoll.close()
            bot.say('Tweet \n' + line + '\n has received a vote.')
            bot.say(majorityVote + 'votes required, ' + tweetVoteCount + 'received.')
