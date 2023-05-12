
from time import sleep
from pyngrok import ngrok
from threading import Thread

def _run_tunnel_core(localhost, port : int):
	print(localhost, port)
	localhost.tunnel = ngrok.connect(port)

class LocalHostTunnel:
	tunnel = None

	def open_tunnel(self):
		if self.tunnel != None:
			return
		Thread(target=_run_tunnel_core, args=(self, self.PORT), daemon=True).start()
		while not self.tunnel:
			print("Awaiting ngrok tunnel to start.")
			sleep(1)
		print("Ngrok tunnel started.")

	def close_tunnel(self):
		if self.tunnel == None:
			return
		self.tunnel.exit()
		self.tunnel = None

	def get_ngrok_addr(self) -> str:
		return self.tunnel.public_url

	def __init__(self, port=500):
		self.PORT = port
