import urllib.request
import json
import websocket
try:
	import thread
except ImportError:
	import _thread as thread
import time
import asyncio

from syddiscord import opcode_factory

GATEWAY_VERSION = "6"
LIBRARY_VERSION = "1.0"

socket = None
token = None
s = None
first_heartbeat = True

def __get_gateway():
	gateway_url = "https://discordapp.com/api/v{}/gateway?encoding=json".format(GATEWAY_VERSION)
	ua = 'SydDiscord {} (Sydney#0256)'.format(LIBRARY_VERSION)

	req = urllib.request.Request(url=gateway_url,headers={'User-Agent':ua})
	json_data = urllib.request.urlopen(req).read()

	parsed_json = json.loads(json_data)
	print(parsed_json["url"])
	return parsed_json["url"]

def __connect_socket(sock_url):
	global socket
	# websocket.enableTrace(True)
	socket = websocket.WebSocketApp("{}/?v={}&encoding=json".format(sock_url, GATEWAY_VERSION),
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	socket.on_open = on_open
	socket.run_forever()

def connect(token_in):
	global token
	token = token_in

	__connect_socket(__get_gateway())

#-------------------------------------------------------------------------------

new_message_func = None

def __heartbeat(interval):
	global first_heartbeat
	print(interval)
	while True:
		if s == None:
			data = "{\"op\": 1, \"d\": null}"
		else:
			data = "{\"op\": 1, \"d\": " + str(s) + "}"
		socket.send(data)

		print("HEARTBEAT")

		time.sleep(interval/1000.0)

def on_message(ws, message):
	global s
	print(message)
	parsed_json = json.loads(message)
	s = parsed_json["s"]
	if(parsed_json["op"] == 10):
		# Hello opcode, very first and only done once
		thread.start_new_thread(__heartbeat, (parsed_json["d"]["heartbeat_interval"],))
		socket.send(opcode_factory.__gen_generic(2, opcode_factory.__gen_indentify(token)))
	if(parsed_json["op"] == 11):
		# Heartbeat acknowledged opcode
		print("HEARTBEAT ACK")
	if(parsed_json["op"] == 0):
		# Post-login stuff
		if(parsed_json["t"] == "MESSAGE_CREATE"):
			# New message
			print("------------------------------")
			print(parsed_json["d"])
			print("------------------------------")
			if new_message_func != None:
				thread.start_new_thread(new_message_func, (parsed_json["d"],))

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
	print("### opened ###")

#-------------------------------------------------------------------------------

def send_message(content, channel):
	gateway_url = "https://discordapp.com/api/v{}/channels/{}/messages?encoding=json".format(GATEWAY_VERSION, channel)
	data = opcode_factory.__gen_send_message(content)
	ua = 'SydDiscord {} (Sydney#0256)'.format(LIBRARY_VERSION)

	req = urllib.request.Request(url=gateway_url,data=str.encode(data),headers={'User-Agent':ua,"Authorization":"Bot "+token})
	json_data = urllib.request.urlopen(req).read()
	print(json_data)