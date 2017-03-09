import inspect
import os
import urllib.request
import urllib.error

def getCaller():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    temp = mod.__name__
    return temp.split('.')[-1]

#=============================

def writeString(string, plugin, filename):
    with open('cache\\{}_{}'.format(plugin, filename), 'w') as f:
        f.write(string)

def getJson(url, caller=''):
    if caller == '':
        getCaller()
    fullFilename = '{}_{}'.format(caller, url.split('/')[-1])
    if os.path.isfile(fullFilename):
        with open('cache/{}'.format(fullFilename)) as f:
            return f.read()
    else:
        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        with open('cache\\{}'.format(fullFilename), 'w') as f:
            f.write(jsonString)
        return jsonString


def downloadToCache(url, filename, caller=''):
    if caller == '':
        getCaller()
    fullFilename = 'cache/{}_{}'.format(caller, filename)
    if os.path.isfile(fullFilename):
        return 1
    else:
        try:
            urllib.request.urlretrieve(url, fullFilename)
            return 1
        except urllib.error.HTTPError as e:
            return -1
        except urllib.error.URLError as e:
            return -2