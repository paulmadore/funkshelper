from sopel import module
from sopel.module import NOLIMIT, commands, example, rule

@module.commands('echo', 'repeat')
def echo(bot, trigger):
    bot.reply(trigger.group(2))
    
@module.rule('hello!?')
def hi(bot, trigger):
    bot.say('Huglgla ' + trigger.nick + '! Thrag baoth nàmhaid caggey uz khuzd! Remmag .help ez.')


    
