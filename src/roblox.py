
import os
import time

from .minify import minify_lua_source

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LUA_FOLDER = os.path.join(FILE_DIRECTORY, "lua")

print( LUA_FOLDER )

class CodePieces:
	HEX_FUNCTIONS = open( os.path.join(LUA_FOLDER, "hexF.lua"), "r" ).read()
	ZLIB_MODULE = open( os.path.join(LUA_FOLDER, "zlib.lua"), "r" ).read()
	# RENDERER_FUNCTION = open( os.path.join(LUA_FOLDER, "renderer.lua"), "r" ).read()

class CodeFactory:

	def __init__(self):
		self.source = []

	def append_server_relay_CLIENT_ONLY( self ) -> None:
		pass

	def append_server_relay_SERVER_SIDE( self ) -> None:
		pass

	def append_client_remote_control( self ) -> None:
		pass

	def append_client_displayer( self ) -> None:
		pass

	def append_synapseX_client_only( self ) -> None:
		pass

	def minify_source( self ) -> None:
		self.source = [ minify_lua_source( "\n".join( self.source ) ) ]

	def compile( self, filepath=os.path.join(FILE_DIRECTORY, str(time.time()))) -> str:
		with open( filepath, "w" ) as file:
			file.writelines( self.source )

class ServerSided:

	def generate_network_relay_CLIENT_ONLY( ngrok_addr : str, custom_filepath=None ) -> str:
		'''
		Use this with the 'generate_remote_controller' to allow clients to request data from the localhost and display it for themselves only (those that have run the remote script).
		'''
		pass

	def generate_network_relay_SERVER_SIDE( ngrok_addr : str, custom_filepath=None ) -> str:
		'''
		Use this with the 'generate_remote_controller' to allow clients to request data from the localhost and display it for all players via server-side rendering.
		'''
		pass

class ClientSide:

	def generate_remote_requester( custom_filepath=None ) -> str:
		'''
		Use this with the 'generate_network_relay_CLIENT_ONLY' or 'generate_network_relay_SERVER' to ask the server to check for an update.
		'''
		pass

	def generate_remote_displayer( custom_filepath=None ) -> str:
		'''
		Use this with the 'generate_network_relay_CLIENT_ONLY' to load images received by the server.
		'''
		pass

	def generate_synapseX_localhost( ngrok_addr : str, custom_filepath=None ) -> str:
		'''
		Use this for pure client-only image rendering.
		'''
		pass
