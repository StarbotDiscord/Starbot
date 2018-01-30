import syddiscord

def onmessage(message):
	if message["content"] == "!ping":
		syddiscord.send_message("PONG", message["channel_id"])

token = ""
with open("token.txt") as m:
	token = m.read().strip()

syddiscord.new_message_func = onmessage
syddiscord.connect(token)