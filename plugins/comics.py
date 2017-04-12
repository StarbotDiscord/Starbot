import json

from api import command, caching, message, plugin


def onInit(plugin_in):
    xkcd_command = command.command(plugin, 'xkcd', shortdesc='Posts the latest XKCD, or by specific ID')
    return plugin.plugin(plugin, 'comics', [xkcd_command])

def onCommand(message_in):
    if message_in.command == 'xkcd':
        if message_in.body != '':
            try:
                if int(message_in.body) < 0:
                    return message.message(body="ID `{}` is not a valid ID".format(message_in.body))
            except:
                return message.message(body='Input of `{}` is not a valid number'.format(message_in.body))

            data = json.loads(caching.getJson("https://xkcd.com/{}/info.0.json".format(message_in.body.strip()),
                                              caller='xkcd',
                                              customName='{}.json'.format(message_in.body.strip())))
        else:
            data = json.loads(caching.getJson("https://xkcd.com/info.0.json", caller='xkcd', save=False))

        caching.downloadToCache(data['img'], '{}.png'.format(data['num']), caller='xkcd')

        return message.message(body='**{}/{}/{} - {}**\n_{}_'.format(data['month'], data['day'], data['year'], data['safe_title'], data['alt']),
                               file='cache/xkcd_{}.png'.format(data['num']))