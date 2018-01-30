import time

def gen_generic(opcode, data):
	return """{"op":""" + str(opcode) + ""","d":""" + data + "}"

def gen_indentify(token):
	data = """{
    "token": "TOKEN_DATA",
    "properties": {
        "$os": "darwin",
        "$browser": "SydDiscord",
        "$device": "SydDiscord"
    },
    "compress": false,
    "large_threshold": 50,
    "presence": {
        "game": {
            "name": "with APIs",
            "type": 0
        },
        "status": "online",
        "since": TIME,
        "afk": false
    }
}""".replace("TOKEN_DATA", token).replace("TIME", str(int(time.time())))
	return data

def gen_send_message(content):
    return "{\"content\": \"" + content.replace("\n", "\\n") + "\"}"