import sqlite3

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

def logUserMessage(message):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_messages (userid INTEGER, username TEXT, message TEXT, serverid INTEGER, servername TEXT)')
    c.execute('INSERT INTO user_messages VALUES (?,?,?,?,?)',
              (message.author.id, message.author.name, message.content, message.server.id, message.server.name))
    conn.commit()
    conn.close()