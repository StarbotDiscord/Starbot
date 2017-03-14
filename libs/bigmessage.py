import message
import textwrap

# Breaks giant message into chunks.
def create(msg, characters : int = 2000):
    if not msg:
        return None

    # Create message list.
    textList = textwrap.wrap(msg, characters, break_long_words=True, replace_whitespace=False)
    if not len(textList):
        return None
    
    # Create message list objects.
    messageList = []
    for msg in textList:
        messageList.append(message.message(msg))
    
    # Return the list.
    return messageList
