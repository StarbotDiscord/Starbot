import urllib.request
import json
import plugin
import command
import message
import os

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
        if message_in.body != '':
            try:
                int(message_in.body)
            except:
                err_message = message.message
                err_message.body = 'Input of `{}` is not a valid number'.format(message_in.body)
                return err_message

            json_filename = 'cache/xkcd_{}.json'.format(message_in.body.strip())

            if os.path.isfile(json_filename):
                pass
            else:
                print("Grabbing XKCD JSON! Not in cache.")
                urllib.request.urlretrieve("https://xkcd.com/{}/info.0.json".format(message_in.body.strip()), json_filename)

            f = ''
            with open(json_filename) as m:
                f = m.read()
            data = json.loads(f)
        else:
            f = urllib.request.urlopen("https://xkcd.com/info.0.json")
            data = json.load(f)

        comic_filename = 'cache/xkcd_{}.png'.format(data['num'])
        if os.path.isfile(comic_filename):
            pass
        else:
            print("Grabbing latest XKCD! Not in cache.")
            urllib.request.urlretrieve(data['img'], 'cache/xkcd_{}.png'.format(data['num']))

        message_send = message.message
        message_send.body = '**{}/{}/{} - {}**\n_{}_'.format(data['month'], data['day'], data['year'], data['safe_title'], data['alt'])
        message_send.file = 'cache/xkcd_{}.png'.format(data['num'])

        return message_send