import urllib.request
import urllib.error
import json
import plugin
import command
import message
import os

def onInit(plugin):
    star_command = command.command(plugin, 'star', shortdesc='Post a random picture of Star Butterfly to the channel')
    return plugin.plugin.plugin(plugin, 'star', [star_command])

def onCommand(message_in):
    if message_in.command == 'star':
        try:
            f = urllib.request.urlopen("https://sydneyerickson.me/starapi/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to XKCD'.format(message_in.body))

        imageName = f.split('/')
        if os.path.isfile('cache/star_' + imageName[-1]):
            pass
        else:
            urllib.request.urlretrieve(f, 'cache/star_' + imageName[-1])

        return message.message(file='cache/star_' + imageName[-1])