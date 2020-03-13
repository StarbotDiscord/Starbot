import pluginloader
from api.bot import Bot
from api.message import Message

if __name__ == "__main__":
    pluginloader.init()

    tm = Message(body="test")
    m = Bot.commands[3].func(tm)

    sys.exit()