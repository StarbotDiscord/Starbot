import urllib.request
import urllib.error
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
                if int(message_in.body) < 0:
                    err_message = message.message
                    err_message.body = 'ID `{}` is not a valid ID'.format(message_in.body)
                    err_message.file = None
                    return err_message
            except:
                err_message = message.message
                err_message.body = 'Input of `{}` is not a valid number'.format(message_in.body)
                err_message.file = None
                return err_message

            json_filename = 'cache/xkcd_{}.json'.format(message_in.body.strip())

            if os.path.isfile(json_filename):
                pass
            else:
                print("Grabbing XKCD JSON! Not in cache.")
                try:
                    urllib.request.urlretrieve("https://xkcd.com/{}/info.0.json".format(message_in.body.strip()), json_filename)
                except urllib.error.HTTPError as e:
                    err_message = message.message
                    err_message.body = 'Could not find comic with ID `{}`'.format(message_in.body)
                    err_message.file = None
                    return err_message
                except urllib.error.URLError as e:
                    err_message = message.message
                    err_message.body = 'There was an issue connecting to XKCD'.format(message_in.body)
                    return err_message
            f = ''
            with open(json_filename) as m:
                f = m.read()
            data = json.loads(f)
        else:
            try:
                f = urllib.request.urlopen("https://xkcd.com/info.0.json")
            except urllib.error.URLError as e:
                err_message = message.message
                err_message.body = 'There was an issue connecting to XKCD'.format(message_in.body)
                return err_message
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