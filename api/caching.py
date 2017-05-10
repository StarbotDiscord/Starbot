#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import inspect
import os
import urllib.request
import urllib.error
import urllib
import ssl

from api import database
from api.database.table import table, tableTypes

def getCaller():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    temp = mod.__name__
    return temp.split('.')[-1]

#=============================

def writeString(string, plugin, filename):
    database.init()
    table_strcache = table('strcache', tableTypes.pGlobal)
    filename = '{}_{}'.format(plugin, filename)
    try:
        entry_strcache = table.search(table_strcache, 'filename', filename)
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_strcache = None
    if entry_strcache:
        entry_strcache.edit(dict(filename=filename, text=string))
    else:
        table.insert(table_strcache, dict(filename=filename, text=string))


def getJson(url, caller='', customName='', save=True):
    if caller == '':
        getCaller()
    if customName == '':
        customName = url.split('/')[-1]
    filename = '{}_{}'.format(caller, customName)
    # Get cached String
    database.init()
    table_strcache = table('strcache', tableTypes.pGlobal)
    try:
        entry_strcache = table.search(table_strcache, 'filename', filename)
        return entry_strcache.data[2]
    except:
        json_string = urllib.request.urlopen(urllib.request.Request(url)).read().decode("utf-8")
        if save:
            writeString(json_string, caller, customName)
        return json_string


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