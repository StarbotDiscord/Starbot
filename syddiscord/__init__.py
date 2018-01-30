import urllib.request
import json
import websocket
try:
	import thread
except ImportError:
	import _thread as thread
import time

GATEWAY_VERSION = "6"
LIBRARY_VERSION = "1.0"

socket = None
token = None
s = None

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
	websocket.enableTrace(True)
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

def __heartbeat(interval):
	print(interval)
	while True:
		if s == None:
			data = "{\"op\": 1, \"d\": null}"
		else:
			data = "{\"op\": 1, \"d\": " + s + "}"
		socket.send(data)
		time.sleep(interval/1000.0)
		print(data)
		print("HEARTBEAT")

def on_message(ws, message):
	global s
	print(message)
	parsed_json = json.loads(message)
	s = parsed_json["s"]
	if(parsed_json["op"] == 10):
		thread.start_new_thread(__heartbeat, (parsed_json["d"]["heartbeat_interval"],))
	if(parsed_json["op"] == 11):
		print("HEARTBEAT ACK")

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
	print("### opened ###")