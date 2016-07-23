# coding=utf-8
"""
Woodcoin IRC GPG Key Association Module copyright 2015 phm.link
Licensed under Mozilla Public License Version 2.

Synopsis: a module that will register a user with their designated GPG key.

Behavior: should import the public key it is told to import, then store that in a file it then associates with the
user in question once the user signs a message that the bot tells the user. This will be a relatively simple implementation, but if required it could be that once someone has registered, only after they've verified with the bot can their username be used to say things in the room. This could be ideal for a name registration, at the channel level, system. 
"""
from __future__ import unicode_literals
from __future__ import print_function
import gnupg
from sopel.module import commands, rule
from sopel.bot import Sopel
import requests
import random
import string
import os
from urllib.request import urlopen

@commands('register help')
@rule('$nickname register help')
def registerhelp(bot, trigger):
    return bot.say('You must have your GPG key at a reputable server to use it here. Then do .register key KEY-ID, where KEY-ID is the ID of your key. I will then go and fetch the key and associate it with your name. The only way to remove the association will be to sign a message with it.')
    return bot.say('Additionally, at various times no one with your user name will be able to talk without verifying their identity with your GPG key.')

@commands('register key' + providedKey)
@rule('$nickname register key' + providedKey)
def registerkey(bot, trigger):
    keyresult = gpg.recv_keys('aes.keys.peer.sh', providedKey)
    public_keys = gpg.export_keys(keyresult)
    public_keys = gpg.export_keys(keyresult, True)
    filename = providedKey + '.txt'
    def msgToSign(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    msgFilename = msgToSign + '.txt'
    with open(msgFilename, 'w') as msgFile:
        msgFile.write(msgToSign)
    with open(filename, 'w') as keyFile:
        keyFile.write(public_keys)
    return bot.say('Now sign the message ' + msgToSign + ' with your key, and return to say finishregistration signed_message key_id, where signed_message is the signed message and key_id is the proper key id you are trying to finish registration for.')

@commands('finishregistration' + signedMsg + keyId)
@rule('$nickname finishregistration' + signedMsg + keyId)
def finishReg(bot, trigger):
    if signedMsg = ' ' OR keyId = ' '
            ''' ^^invalid^^ '''
    return bot.say('Say finishregistration signed_message keyID and I will confirm your registration.')
    elif signedMsg != ' '
        holdMsg = signedMsg
        holdKey = keyId
            holdMsg = gpg.verify(signedMsg)
            holdKeyFile = holdMsg + '.txt'
            with open(keyId, 'w') as holdKeyFile:
                holdKeyFile.write(holdMsg)
            