from __future__ import unicode_literals
import random
import re
from sopel import bot, coretasks
from sopel.module import commands, rule
from sopel.bot import Sopel
from sopel import web, tools
from sopel.module import commands, rule, example
from sopel.config.types import ValidatedAttribute, StaticSection
'''
.randomLink - pulls a random link from a database of stored links shared in the channel
.tweetVote - allows the room to vote on the next tweet to be sent out
'''
url_finder = None
class UrlSection(StaticSection):
    # TODO some validation rules maybe?
    exclude = ValidatedAttribute('exclude')
    exclusion_char = ValidatedAttribute('exclusion_char', default='!')

def configure(config):
    config.define_section('url')
    config.url.configure_setting(
        'exclude',
        'Enter regular expressions for each URL you would like to exclude.'
    )
    config.url.configure_setting(
        'exclusion_char',
        'Enter a character which can be prefixed to suppress URL titling'
    )


def setup(bot=None):
    global url_finder

    # TODO figure out why this is needed, and get rid of it, because really?
    if not bot:
        return
    bot.config.define_section('new', UrlSection)

    if bot.config.url.exclude:
        regexes = [re.compile(s) for s in bot.config.url.exclude]
    else:
        regexes = []

    # We're keeping these in their own list, rather than putting then in the
    # callbacks list because 1, it's easier to deal with modules that are still
    # using this list, and not the newer callbacks list and 2, having a lambda
    # just to pass is kinda ugly.
    if not bot.memory.contains('url_exclude'):
        bot.memory['url_exclude'] = regexes
    else:
        exclude = bot.memory['url_exclude']
        if regexes:
            exclude.extend(regexes)
        bot.memory['url_exclude'] = exclude

    # Ensure that url_callbacks and last_seen_url are in memory
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    if not bot.memory.contains('last_seen_url'):
        bot.memory['last_seen_url'] = tools.SopelMemory()

    url_finder = re.compile(r'(?u)(%s?(?:http|https|ftp)(?:://\S+))' %
                            (bot.config.url.exclusion_char))
    
@rule('(?u).*(https?://\S+).*')
def log_urls(bot, trigger):
    bad_chars = '[]\''
    URL = re.findall(url_finder, trigger)
    URL = re.compile('[%s]' % bad_chars)
    with open('urls.txt', 'a+') as f:
        f.write(str(URL) + '\n')
        f.close()
        
@commands('randomlink')
@rule('$nickname lineURL')
def random_line(bot, afile):
    with open('urls.txt') as afile: 
        lineURL = next(afile)
        for num, aline in enumerate(afile):
          if random.randrange(num + 2): continue
          lineURL = aline
        return bot.say(lineURL)
        afile.close()
