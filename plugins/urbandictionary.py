import command
import json
import message
import plugin
import string
import urllib.request
import urllib.error

from libs import bigmessage

# UD plugin
def onInit(plugin):
    define_command = command.command(plugin, 'define', shortdesc='Define X')
    randefine_command = command.command(plugin, 'randefine', shortdesc='Define a random thing')
    return plugin.plugin.plugin(plugin, 'urbandictionary', [define_command, randefine_command])

def onCommand(message_in):
    # Define.
    if message_in.command == 'define':
        # Get the word to define.
        word = message_in.body.strip()

        # Check to see if word is empty.
        if not word:
            return message.message('Usage: `{}define [word]`'.format('!')) # TODO: prefix variable

        # Get definition.
        rword = word.replace(" ", "+")
        msg = 'I couldn\'t find a definition for "{}"...'.format(word) 
        try:
            f = urllib.request.urlopen("http://api.urbandictionary.com/v0/define?term={}".format(rword)).read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to UD'.format(message_in.body))

        # Decode JSON and format definition.
        theJSON = json.loads(f)["list"]
        if len(theJSON):
            # Build the response.
            ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__Example(s):__\n\n*{}*'.format(msg, ourWord["example"])

        # Return message.
        return bigmessage.create(msg)

    # Random define.
    if message_in.command == 'randefine':
        # Get random definition.
        try:
            f = urllib.request.urlopen("http://api.urbandictionary.com/v0/random").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to UD'.format(message_in.body))

        # Decode JSON and format definition.
        theJSON = json.loads(f)["list"]
        if len(theJSON):
            # Build the response.
            ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
            if ourWord["example"]:
                msg = '{}\n\n__Example(s):__\n\n*{}*'.format(msg, ourWord["example"])

        # Return message.
        return bigmessage.create(msg)
