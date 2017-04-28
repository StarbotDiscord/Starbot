import sqlite3

def open(db_in):
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")