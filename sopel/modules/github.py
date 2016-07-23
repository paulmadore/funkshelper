# coding=utf-8
"""
Github module for funkshelper/sopel bot by phm.link.
Must first do pip install pygithub3.
Mozilla 2.0 license.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from datetime import datetime
from pygithub3 import Github
from sopel.module import commands, rule
from sopel.bot import Sopel

@commands('gitrepos', 'repos')
@rule('$nickname repos')
def botinfo(bot, trigger):
    ghname = input.trigger
    namegh = pygithub3('GET /users/:(ghname)/repos')