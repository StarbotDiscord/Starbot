from urllib.request import urlopen
import urllib

from api import command, message, plugin


def onInit(plugin_in):
    tinyurl_command = command.command(plugin, 'tinyurl', shortdesc='Convert a link to a TinyURL')
    return plugin.plugin(plugin, 'tinyurl', [tinyurl_command])

def onCommand(message_in):
    if message_in.body == '':
        return message.message(body='Usage:\ntinyurl [url]')
    else:
        try:
            urllib.request.urlopen(message_in.body.strip())
            return message.message(body=urlopen("http://tinyurl.com/api-create.php?url=" + message_in.body.strip()).read().decode("utf-8"))
        except Exception as e:
            return message.message(body='That website doesn\'t seem to exist')