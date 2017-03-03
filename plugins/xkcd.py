import urllib.request
import json
import plugin
import command
import message

def onInit(plugin):
    #create the basics of our plugin
    xkcd_plugin = plugin.plugin
    xkcd_plugin.plugin = plugin
    xkcd_plugin.name = 'XKCD'

    #now to register commands
    xkcd_command = command.command
    xkcd_command.plugin = plugin
    xkcd_command.name = 'xkcd'

    #add our commands to the plugin
    xkcd_plugin.commands = [] #this line is for some reason needed or stuff will break
    xkcd_plugin.commands.append(xkcd_command)

    return xkcd_plugin

def onCommand(message_in):
    if message_in.command == 'xkcd':
        f = urllib.request.urlopen("https://xkcd.com/info.0.json")
        data = json.load(f)

        message_send = message.message
        message_send.body = data['img']

        return message_send