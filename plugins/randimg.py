import random
import urllib.error
import urllib.request

from api import command, caching, message, plugin


def onInit(plugin):
    star_command = command.command(plugin, 'star', shortdesc='Post a random picture of Star Butterfly to the channel')
    starco_command = command.command(plugin, 'starco', shortdesc='Nowhere is safe from the shipping wars. Nowhere.')
    marco_command = command.command(plugin, 'marco', shortdesc='Post a random picture of Marco Diaz to the channel')
    goldfish_command = command.command(plugin, 'goldfish', shortdesc='Post a random picture of a goldfish to the channel')
    return plugin.plugin.plugin(plugin, 'randimg', [star_command, goldfish_command, starco_command, marco_command])

def onCommand(message_in):
    # Star
    if message_in.command == 'star':
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            try:
                re = urllib.request.Request("https://starbooru.com/api/posts?offset=0&limit=100&query=safety:safe%20star_butterfly%20solo")
                re.add_header('Content-Type', 'application/json')
                re.add_header('Accept', 'application/json')
                r = urllib.request.urlopen(re).read()
            except Exception as e:
                return message.message(body='Issue connecting to Starbooru. Perhaps it\'s down?')
            try:
                jsonG = r.json()
                print(len(jsonG['results']))
                randIMG = random.choice(jsonG['results'])
                filename = str(randIMG['id']) + '.' + randIMG['contentUrl'].split(".")[-1]
                caching.downloadToCache(randIMG['contentUrl'], filename, caller='star', sslEnabled=False)
                return message.message(file='cache/star_' + filename)
            except Exception as e:
                return message.message(body='No images by these tags found. :(')
        except Exception as e:
            return message.message(body='Unknown issue')

    if message_in.command == 'starco':
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            try:
                re = urllib.request.Request(
                    "https://starbooru.com/api/posts?offset=0&limit=100&query=safety:safe%20starco")
                re.add_header('Content-Type', 'application/json')
                re.add_header('Accept', 'application/json')
                r = urllib.request.urlopen(re).read()
            except Exception as e:
                return message.message(body='Issue connecting to Starbooru. Perhaps it\'s down?')
            try:
                jsonG = r.json()
                print(len(jsonG['results']))
                randIMG = random.choice(jsonG['results'])
                filename = str(randIMG['id']) + '.' + randIMG['contentUrl'].split(".")[-1]
                caching.downloadToCache(randIMG['contentUrl'], filename, caller='starco', sslEnabled=False)
                return message.message(file='cache/starco_' + filename)
            except Exception as e:
                return message.message(body='No images by these tags found. :(')
        except Exception as e:
            return message.message(body='Unknown issue')

    if message_in.command == 'marco':
        try:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            try:
                re = urllib.request.Request(
                    "https://starbooru.com/api/posts?offset=0&limit=100&query=safety:safe%20marco_diaz%20solo")
                re.add_header('Content-Type', 'application/json')
                re.add_header('Accept', 'application/json')
                r = urllib.request.urlopen(re).read()
            except Exception as e:
                return message.message(body='Issue connecting to Starbooru. Perhaps it\'s down?')
            try:
                jsonG = r.json()
                print(len(jsonG['results']))
                randIMG = random.choice(jsonG['results'])
                filename = str(randIMG['id']) + '.' + randIMG['contentUrl'].split(".")[-1]
                caching.downloadToCache(randIMG['contentUrl'], filename, caller='marco', sslEnabled=False)
                return message.message(file='cache/marco_' + filename)
            except Exception as e:
                return message.message(body='No images by these tags found. :(')
        except Exception as e:
            return message.message(body='Unkown issue')

    # Goldfish
    if message_in.command == 'goldfish':
        try:
            f = urllib.request.urlopen("http://goldfishapi.azurewebsites.net/goldfish/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to goldfish API.'.format(message_in.body))

        imageName = f.split('/')
        caching.downloadToCache(f, imageName[-1], caller='goldfish')

        return message.message(file='cache/goldfish_' + imageName[-1])
