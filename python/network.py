from time import sleep
from typing import Callable
from pyngrok import ngrok
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

def string_to_bytes(string : str) -> bytes:
	return bytes(string, "utf-8")

class LocalHost:
	HOSTED_RAW_DATA = "null"

	@staticmethod
	def SET_HOSTED_RAW_DATA( data : str ) -> None:
		LocalHost.HOSTED_RAW_DATA = data

	@staticmethod
	def GET_HOSTED_RAW_DATA() -> str:
		return LocalHost.HOSTED_RAW_DATA

	class ThreadedServerResponder(BaseHTTPRequestHandler):
		def _write_wfile(self, message : str) -> None:
			self.wfile.write( string_to_bytes(message) )
		def do_GET(self):
			# send response status code
			self.send_response(200)
			# send header information
			self.send_header("Content-Type", "html/text")
			# end headers and close response
			self.end_headers()
			self._write_wfile(LocalHost.HOSTED_RAW_DATA)
		# prevent console logs
		def log_message(self, format, *args):
			return

	class ServerThreadWrapper:
		webserver : HTTPServer = None

		server_thread : Thread = None
		shutdown_callback_thread : Thread = None

		def shutdown(self) -> None:
			self.webserver.shutdown()

		def join_thread_callback(self, thread : Thread, callback : Callable):
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

	def start_local_host(port=500) -> ServerThreadWrapper:
		customThreadedResponder = LocalHost.ThreadedServerResponder
		customThreadedResponder.webserver = None
		LocalHost.webServer = HTTPServer(('localhost', port), customThreadedResponder)
		def ThreadExitCallback(self):
			print("Server Closed")
			LocalHost.webServer.server_close()
		return LocalHost.ServerThreadWrapper(webserver=LocalHost.webServer, server_closed_callback=ThreadExitCallback)

class Ngrok:
	'''
	Ngrok singleton class - manages the ngrok tunnel.
	'''
	port = 8080
	tunnel = None
	_thread = None

	@staticmethod
	def _internal_start_tunnel( port : int ) -> None:
		'''
		Connect to the ngrok servers with the given port.
		'''
		Ngrok.tunnel = ngrok.connect(port)

	@staticmethod
	def set_port( port : int ) -> None:
		'''
		Set the port.
		'''
		Ngrok.port = port

	@staticmethod
	def open_tunnel( ) -> None:
		'''
		Open the ngrok tunnel if it is not open already.
		'''
		assert Ngrok.tunnel == None, "Tunnel is already open (tunnel reference)."
		assert Ngrok._thread == None, "Tunnel is already open (thread exists)."
		Ngrok._thread = Thread(target=Ngrok._internal_start_tunnel, args=(Ngrok.port,), daemon=True)
		Ngrok._thread.start()
		if Ngrok.tunnel == None:
			print("Awaiting ngrok tunnel to start.")
			while Ngrok.tunnel == None:
				sleep(1)
		print("ngrok tunnel has started.")

	@staticmethod
	def close_tunnel( ) -> None:
		'''
		Close the ngrok tunnel if it is open.
		'''
		assert Ngrok.tunnel != None, "Tunnel is non-existent."
		Ngrok._thread = None
		ngrok.disconnect( Ngrok.get_ngrok_addr() )
		Ngrok.tunnel = None

	@staticmethod
	def get_ngrok_addr( ) -> str:
		'''
		Get the ngrok address for web requests.
		'''
		assert Ngrok.tunnel != None, "You must open the tunnel before you can get the address."
		return Ngrok.tunnel.public_url

	@staticmethod
	def await_ngrok_addr( ) -> str:
		while Ngrok.tunnel == None:
			sleep( 0.25 )
		return Ngrok.tunnel.public_url
