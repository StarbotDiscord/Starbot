#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import random

from api import command, message, plugin
from libs import displayname


# Eating plugin
def onInit(plugin_in):
    eat_command = command.command(plugin_in, 'eat', shortdesc='Eat someone or something')
    return plugin.plugin(plugin_in, 'eat', [eat_command])

async def onCommand(message_in):
    if message_in.command == 'eat':
        author = displayname.name(message_in.author)
        member = message_in.body.strip()

        # Check if we're eating nothing
        if member == "":
            list_none = ['you sit quietly and eat *nothing*...',
                         'you\'re *sure* there was something to eat, so you just chew on nothingness...',
                         'there comes a time when you need to realize that you\'re just chewing nothing for the sake of chewing.  That time is now.']

            randnum = random.randint(0, len(list_none) - 1)
            return message.message('*{}*, {}'.format(author, list_none[randnum]))

        # Check if we're eating a member
        mem_check = displayname.memberForName(member, message_in.server)
        if mem_check:
            # We're eating a member - let's do a bot-check
            if mem_check.id == message_in.server.me.id:
                # It's me!
                msg_list = ['you try to eat *me* - but unfortunately, I saw it coming - your jaw hangs open as I deftly sidestep.',
                            'your mouth hangs open for a brief second before you realize that *I\'m* eating *you*.',
                            'I\'m a bot.  You can\'t eat me.',
                            'your jaw clamps down on... wait... on nothing, because I\'m *digital!*.',
                            'what kind of bot would I be if I let you eat me?']

            elif mem_check.id == message_in.author.id:
                # We're eating...  ourselves?
                msg_list = ['you clamp down on your own forearm - not surprisingly, it hurts.',
                            'you place a finger into your mouth, but *just can\'t* force yourself to bite down.',
                            'you happily munch away, but can now only wave with your left hand.',
                            'wait - you\'re not a sandwich!',
                            'you might not be the smartest...']

            else:
                mem_name = displayname.name(mem_check)
                msg_list = ['you unhinge your jaw and consume *{}* in one bite.'.format(mem_name),
                            'you try to eat *{}*, but you just can\'t quite do it - you spit them out, the taste of failure hanging in your mouth...'.format(mem_name),
                            'you take a quick bite out of *{}*.  They probably didn\'t even notice.'.format(mem_name),
                            'you sink your teeth into *{}\'s* shoulder - they turn to face you, eyes wide as you try your best to scurry away and hide.'.format(mem_name),
                            'your jaw clamps down on *{}* - a satisfying *crunch* emanates as you finish your newest meal.'.format(mem_name)]

            randnum = random.randint(0, len(msg_list) - 1)
            return message.message('*{}*, {}'.format(author, msg_list[randnum]))

        # Assume we're eating something else
        itemList = ['you take a big chunk out of *{}*. *Delicious.*'.format(member),
                    'your teeth sink into *{}* - it tastes satisfying.'.format(member),
                    'you rip hungrily into *{}*, tearing it to bits!'.format(member),
                    'you just can\'t bring yourself to eat *{}* - so you just hold it for awhile...'.format(member),
                    'you attempt to bite into *{}*, but you\'re clumsier than you remember - and fail...'.format(member),]

        randnum = random.randint(0, len(itemList) - 1)
        return message.message('*{}*, {}'.format(author, itemList[randnum]))
