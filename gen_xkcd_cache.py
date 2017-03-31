from tqdm import tqdm
import urllib.error
import urllib.request
import json
import caching

for i in tqdm(range(1806)):
    try:
        jsonD = caching.getJson("https://xkcd.com/{}/info.0.json".format(i), caller='xkcd', customName='{}.json'.format(i))
    except urllib.error.HTTPError as e:
        print("404")
        continue
    except urllib.error.URLError as e:
        print("error")
        continue

    f = json.loads(jsonD)
    imageUrl = f['img']

    try:
        urllib.request.urlretrieve(imageUrl, 'cache/xkcd_{}.png'.format(i))
    except urllib.error.HTTPError as e:
        print("404")
    except urllib.error.URLError as e:
        print("error")