from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from base64 import decode as bs4decode
from typing import Union

HOST_IP = "localhost"
HOSTED_RAW_DATA = "there is no data setup"

def SET_HOSTED_RAW_DATA(data : str) -> None:
	global HOSTED_RAW_DATA
	HOSTED_RAW_DATA = data

def GET_HOSTED_RAW_DATA() -> str:
	global HOSTED_RAW_DATA
	return HOSTED_RAW_DATA

def _str_to_byte(str) -> bytes:
	return bytes(str, "utf-8")

class ThreadedServerResponder(BaseHTTPRequestHandler):
	def _write_wfile(self, message : str) -> None:
		self.wfile.write( _str_to_byte(message) )

	def do_GET(self):
		print("got request")

		# send response status code
		self.send_response(200)
		# send header information
		self.send_header("Content-Type", "application/json")
		# end headers and close response
		self.end_headers()

		self._write_wfile(HOSTED_RAW_DATA)
		
	# prevent console logs
	def log_message(self, format, *args):
		return

class ServerThreadWrapper:
	webserver : HTTPServer = None

	server_thread : Thread = None
	shutdown_callback_thread : Thread = None

	def shutdown(self) -> None:
		self.webserver.shutdown()

	def join_thread_callback(self, thread : Thread, callback):
		thread.join()
		callback(self)

	def thread_ended_callback(self, main_thread : Thread, callback) -> Thread:
		callback_thread = Thread(target=self.join_thread_callback, args=(main_thread, callback))
		callback_thread.start()
		return callback_thread

	def start(self, webserver=None, server_closed_callback=None):
		self.webserver = webserver
		if webserver == None:
			return
		server_thread : Thread = Thread(target=webserver.serve_forever)
		self.server_thread = server_thread
		print(f"Server Starting @ {self.webserver.server_address}")
		server_thread.start()
		if server_closed_callback != None:
			self.shutdown_callback_thread = self.thread_ended_callback(server_thread, server_closed_callback)

	def __init__(self, webserver=None, server_closed_callback=None):
		self.start(webserver=webserver, server_closed_callback=server_closed_callback)

def SetupLocalHost(port=500) -> ServerThreadWrapper:
	customThreadedResponder = ThreadedServerResponder
	customThreadedResponder.webserver = None
	webServer = HTTPServer((HOST_IP, port), customThreadedResponder)
	def ThreadExitCallback(self):
		print("Server Closed")
		nonlocal webServer
		webServer.server_close()
	return ServerThreadWrapper(webserver=webServer, server_closed_callback=ThreadExitCallback)
