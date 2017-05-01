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


# Fun plugin
def onInit(plugin_in):
    lenny_command = command.command(plugin_in, 'lenny', shortdesc='Give some Lenny')
    shrug_command = command.command(plugin_in, 'shrug', shortdesc='Shrug it off')
    tableflip_command = command.command(plugin_in, 'tableflip', shortdesc='Flip a table')
    fart_command = command.command(plugin_in, 'fart', shortdesc='PrincessZoey :P')
    beta_command = command.command(plugin_in, 'beta', shortdesc='Something went wrong™')
    return plugin.plugin(plugin_in, 'fun', [lenny_command, shrug_command, tableflip_command, fart_command, beta_command])

def onCommand(message_in):
    # Lenny.
    if message_in.command == 'lenny':
        # Create message.
        msg = "( ͡° ͜ʖ ͡°)"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Shrug.
    if message_in.command == 'shrug':
        # Create message.
        msg = "¯\_(ツ)_/¯"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Tableflip.
    if message_in.command == 'tableflip':
        # Create message.
        msg = "(╯°□°）╯︵ ┻━┻"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Fart.
    if message_in.command == 'fart':
        # Make farts.
        fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
        randnum = random.randint(0, len(fartList)-1)
        msg = '{}'.format(fartList[randnum])

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return fart message.
        return message.message(msg, delete=True)

    if message_in.command == 'beta':
        return message.message(body='It looks like something went wrong', file="beta.jpg")
