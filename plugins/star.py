import urllib.request
import urllib.error
import json
import plugin
import command
import message
import os

def onInit(plugin):
    #create the basics of our plugin
    xkcd_plugin = plugin.plugin.plugin()
    xkcd_plugin.plugin = plugin
    xkcd_plugin.name = 'star'

    #now to register commands
    xkcd_command = command.command()
    xkcd_command.plugin = plugin
    xkcd_command.name = 'star'

    #add our commands to the plugin
    xkcd_plugin.commands = [] #this line is for some reason needed or stuff will break
    xkcd_plugin.commands.append(xkcd_command)

    return xkcd_plugin

def onCommand(message_in):
    if message_in.command == 'star':
        try:
            f = urllib.request.urlopen("https://sydneyerickson.me/starapi/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.create(body='There was an issue connecting to XKCD'.format(message_in.body))

        imageName = f.split('/')
        if os.path.isfile('cache/star_' + imageName[-1]):
            pass
        else:
            urllib.request.urlretrieve(f, 'cache/star_' + imageName[-1])

        return message.create(file='cache/star_' + imageName[-1])