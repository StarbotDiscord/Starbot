from tqdm import tqdm
import urllib.error
import urllib.request
import json

for i in tqdm(range(1806)):
    try:
        urllib.request.urlretrieve("https://xkcd.com/{}/info.0.json".format(i), 'cache/xkcd_{}.json'.format(i))
    except urllib.error.HTTPError as e:
        print("404")
        continue
    except urllib.error.URLError as e:
        print("error")
        continue

    imageUrl = ''
    with open('cache/xkcd_{}.json'.format(i)) as fl:
        f = json.loads(fl.read())
        imageUrl = f['img']

    try:
        urllib.request.urlretrieve(imageUrl, 'cache/xkcd_{}.png'.format(i))
    except urllib.error.HTTPError as e:
        print("404")
    except urllib.error.URLError as e:
        print("error")