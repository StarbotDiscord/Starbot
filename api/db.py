import sqlite3

def logUserMessage(message):
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user_messages (userid INTEGER, username TEXT, message TEXT, serverid INTEGER, servername TEXT)')
    c.execute('INSERT INTO user_messages VALUES (?,?,?,?,?)',
              (message.author.id, message.author.name, message.content, message.server.id, message.server.name))
    conn.commit()
    conn.close()