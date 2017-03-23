import inspect
import os
import urllib.request
import urllib.error
import urllib
import ssl

def getCaller():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    temp = mod.__name__
    return temp.split('.')[-1]

#=============================

def writeString(string, plugin, filename):
    with open('cache\\{}_{}'.format(plugin, filename), 'w') as f:
        f.write(string)

def getJson(url, caller='', customName='', save=True):
    if caller == '':
        getCaller()
    if customName == '':
        customName = url.split('/')[-1]
    fullFilename = '{}_{}'.format(caller, customName)
    if os.path.isfile(fullFilename):
        with open('cache/{}'.format(fullFilename)) as f:
            return f.read()
    else:
        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        if save == True:
            with open('cache/{}'.format(fullFilename), 'w') as f:
                f.write(jsonString)
        return jsonString


def downloadToCache(url, filename, caller='', sslEnabled=True):
    if caller == '':
        getCaller()
    fullFilename = 'cache/{}_{}'.format(caller, filename)
    if os.path.isfile(fullFilename):
        return 1
    else:
        try:
            if sslEnabled == True:
                urllib.request.urlretrieve(url, fullFilename)
            else:
                ssl._create_default_https_context = ssl._create_unverified_context
                urllib.request.urlretrieve(url, fullFilename)
            return 1
        except urllib.error.HTTPError as e:
            return -1
        except urllib.error.URLError as e:
            return -2