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
    xkcd_plugin.name = 'comics'

    #now to register commands
    xkcd_command = command.command()
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
                    return message.create(body="ID `{}` is not a valid ID".format(message_in.body))
            except:
                return message.create(body='Input of `{}` is not a valid number'.format(message_in.body))

            json_filename = 'cache/xkcd_{}.json'.format(message_in.body.strip())

            if os.path.isfile(json_filename):
                pass
            else:
                print("Grabbing XKCD JSON! Not in cache.")
                try:
                    urllib.request.urlretrieve("https://xkcd.com/{}/info.0.json".format(message_in.body.strip()), json_filename)
                except urllib.error.HTTPError as e:
                    return message.create(body='Could not find comic with ID `{}`'.format(message_in.body))
                except urllib.error.URLError as e:
                    return message.create(body='There was an issue connecting to XKCD'.format(message_in.body))

            f = ''
            with open(json_filename) as m:
                f = m.read()
            data = json.loads(f)
        else:
            try:
                f = urllib.request.urlopen("https://xkcd.com/info.0.json")
            except urllib.error.URLError as e:
                return message.create(body='There was an issue connecting to XKCD'.format(message_in.body))
            data = json.load(f)

        comic_filename = 'cache/xkcd_{}.png'.format(data['num'])
        if os.path.isfile(comic_filename):
            pass
        else:
            print("Grabbing latest XKCD! Not in cache.")
            urllib.request.urlretrieve(data['img'], 'cache/xkcd_{}.png'.format(data['num']))

        return message.create(body='**{}/{}/{} - {}**\n_{}_'.format(data['month'], data['day'], data['year'], data['safe_title'], data['alt']),
                              file='cache/xkcd_{}.png'.format(data['num']))