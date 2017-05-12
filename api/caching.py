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

def caller_get():
    '''Get the caller of the parent function.'''
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    temp = mod.__name__
    return temp.split('.')[-1]

#=============================

def json_store(string, plugin, filename):
    '''Store a json in the database.'''
    database.init()
    table_strcache = table('strcache', tableTypes.pGlobal)
    filename = '{}_{}'.format(plugin, filename)
    try:
        entry_strcache = table.search(table_strcache, 'filename', filename)
    except:
        # Table must be empty.
        entry_strcache = None
    if entry_strcache:
        entry_strcache.edit(dict(filename=filename, text=string))
    else:
        table.insert(table_strcache, dict(filename=filename, text=string))


def json_get(url, caller='', name_custom='', save=True):
    '''Retrieve and cache a JSON.'''
    if caller == '':
        caller_get()
    if name_custom == '':
        name_custom = url.split('/')[-1]
    filename = '{}_{}'.format(caller, name_custom)
    # Get cached String
    database.init()
    table_strcache = table('strcache', tableTypes.pGlobal)
    try:
        entry_strcache = table.search(table_strcache, 'filename', filename)
        json_string = entry_strcache.data[2]
    except AttributeError:
        json_string = urllib.request.urlopen(urllib.request.Request(url)).read().decode("utf-8")
        if save:
            json_store(json_string, caller, name_custom)
    return json_string


def cache_download(url, filename, caller='', ssl_enabled=True):
    '''Download a file to the cache'''
    if caller == '':
        caller_get()
    filename_full = 'cache/{}_{}'.format(caller, filename)
    if os.path.isfile(filename_full):
        return 1
    else:
        try:
            if ssl_enabled:
                urllib.request.urlretrieve(url, filename_full)
            else:
                ssl._create_default_https_context = ssl._create_unverified_context
                urllib.request.urlretrieve(url, filename_full)
            return 1
        except urllib.error.HTTPError:
            return -1
        except urllib.error.URLError:
            return -2
