import inspect
import os
import urllib.request
import urllib.error
import urllib
import ssl

from api import db

def getCaller():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    temp = mod.__name__
    return temp.split('.')[-1]

#=============================

def writeString(string, plugin, filename):
    db.cacheFileS('{}_{}'.format(plugin, filename), string)

def getJson(url, caller='', customName='', save=True):
    if caller == '':
        getCaller()
    if customName == '':
        customName = url.split('/')[-1]
    fullFilename = '{}_{}'.format(caller, customName)
    cacheTry = db.getCachedFileS(fullFilename)
    if cacheTry != '':
        return cacheTry
    else:
        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        if save == True:
            writeString(jsonString)
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