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

# TODO: Move caching commands into caching.py and remove old DB API

import sqlite3

def cacheFile(filename, data):
    filename = filename.replace('.', '/.')
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data BLOB)')
    c.execute('SELECT filename FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    if len(list(c)) != 0:
        c.execute('UPDATE cachedfiles_string SET data=\'?\' WHERE filename=\'?\'', (data, filename))
    else:
        c.execute('INSERT INTO cachedfiles_string VALUES (?,?)', ("'" + filename + "'", "'" + data + "'"))
    conn.commit()
    conn.close()

def getCachedFile(filename):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data BLOB)')
    c.execute('SELECT data FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    try:
        row = list(c)[0]
    except:
        row = [""]
    conn.commit()
    conn.close()
    return row[0]

def cacheFileS(filename, data):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data TEXT)')
    c.execute('SELECT filename FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    if len(list(c)) != 0:
        c.execute('UPDATE cachedfiles_string SET data=? WHERE filename=?', (data, filename))
    else:
        c.execute('INSERT INTO cachedfiles_string VALUES (?,?)', (filename, data))
    conn.commit()
    conn.close()

def getCachedFileS(filename):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cachedfiles_string (filename TEXT, data TEXT)')
    c.execute('SELECT data FROM cachedfiles_string WHERE filename=\'' + filename + '\'')
    try:
        row = list(c)[0]
    except:
        print("[DB    ] Could not find file {} in string file cache.".format(filename))
        row = [""]
    conn.commit()
    conn.close()
    return row[0]

#====================================
# Prefix Stuff
#====================================

def setPrefix(serverid, prefix):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS prefixes (serverid INTEGER, prefix TEXT)')
    c.execute('SELECT prefix FROM prefixes WHERE serverid=' + serverid)
    if len(list(c)) != 0:
        c.execute('UPDATE prefixes SET prefix=? WHERE serverid=?', (prefix, serverid))
    else:
        c.execute('INSERT INTO prefixes VALUES (?,?)', (serverid, prefix))
    conn.commit()
    conn.close()

def getPrefix(serverid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS prefixes (serverid INTEGER, prefix TEXT)')
    c.execute('SELECT prefix FROM prefixes WHERE serverid=' + serverid)
    try:
        row = list(c)[0]
    except:
        row = ["!"]
    conn.commit()
    conn.close()
    return row[0]

#====================================
# Logging Stuff
#====================================

def logUserMessage(message):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_messages (userid INTEGER, username TEXT, message TEXT, serverid INTEGER, servername TEXT)')
    c.execute('INSERT INTO user_messages VALUES (?,?,?,?,?)',
              (message.author.id, message.author.name, message.content, message.server.id, message.server.name))
    conn.commit()
    conn.close()

#====================================
# Server Owner Stuffs
#====================================

def isOwner(uid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    cur = c.execute('SELECT userid FROM owners')
    for row in list(cur):
        if str(row[0]) == str(uid):
            conn.commit()
            conn.close()
            return True
    conn.commit()
    conn.close()
    return False

def getOwners():
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    cur = c.execute('SELECT userid FROM owners')
    owners = []
    for row in list(cur):
        owners.append(row[0])
    conn.commit()
    conn.close()
    return owners

def addOwner(uid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    c.execute('INSERT INTO owners VALUES (' + uid + ')')
    conn.commit()
    conn.close()

#====================================
# Server Owner Stuffs
#====================================

def setMessageCount(serverid, messageCount):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messagecounts (serverid INTEGER, count INTEGER)')
    c.execute('SELECT count FROM messagecounts WHERE serverid=' + serverid)
    if len(list(c)) != 0:
        c.execute('UPDATE messagecounts SET count=? WHERE serverid=?', (messageCount, serverid))
    else:
        c.execute('INSERT INTO messagecounts VALUES (?,?)', (serverid, messageCount))
    conn.commit()
    conn.close()

def getMessageCount(serverid):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messagecounts (serverid INTEGER, count INTEGER)')
    c.execute('SELECT count FROM messagecounts WHERE serverid=' + serverid)
    try:
        row = list(c)[0]
    except:
        row = [0]
    conn.commit()
    conn.close()
    return int(row[0])