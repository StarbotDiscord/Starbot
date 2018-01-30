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

import json
import string
import urllib.error
import urllib.request

from api import command, message, plugin, caching

# UD plugin
def onInit(plugin_in):
    define_command = command.Command(plugin_in, 'define', shortdesc='Define X')
    randefine_command = command.Command(plugin_in, 'randefine', shortdesc='Define a random thing')
    return plugin.Plugin(plugin_in, 'urbandictionary', [define_command, randefine_command])

def onCommand(message_in):
    # Define.
    if message_in.command == 'define':
        # Get the word to define.
        word = message_in.body.strip()

        # Check to see if word is empty.
        if not word:
            return message.Message('Usage: `{}define [word]`'.format('!')) # TODO: prefix variable

        # Get definition.
        rword = word.replace(" ", "+")
        msg = 'I couldn\'t find a definition for "{}"...'.format(word)

        f = caching.json_get("http://api.urbandictionary.com/v0/define?term={}".format(rword), caller='define', name_custom=rword)

        #try:
        #    f = urllib.request.urlopen("http://api.urbandictionary.com/v0/define?term={}".format(rword)).read().decode("utf-8")
        #except urllib.error.URLError as e:
        #    return message.Message(body='There was an issue connecting to UD'.format(message_in.body))

        # Decode JSON and format definition.
        theJSON = json.loads(f)["list"]
        if len(theJSON):
            # Build the response.
            ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__Example(s):__\n\n*{}*'.format(msg, ourWord["example"])

        # Return message.
        return message.msg_split(msg)

    # Random define.
    if message_in.command == 'randefine':
        # Get random definition.
        try:
            f = urllib.request.urlopen("http://api.urbandictionary.com/v0/random").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.Message(body='There was an issue connecting to UD'.format(message_in.body))

        # Decode JSON and format definition.
        theJSON = json.loads(f)["list"]
        if len(theJSON):
            # Build the response.
            ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__Example(s):__\n\n*{}*'.format(msg, ourWord["example"])

        # Return message.
        return message.msg_split(msg)
