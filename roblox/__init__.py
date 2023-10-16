
import os

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

from .minify import minify_lua_file, minify_lua_source

def prepare_scripts( ngrok_url : str ) -> tuple:
	# print( ngrok_url )

	with open( os.path.join(FILE_DIRECTORY, "download.server.lua") ) as file:
		download_source = file.read()
		download_source = download_source.replace("&&&&", ngrok_url)

	with open( os.path.join(FILE_DIRECTORY, "zlib.lua") ) as file:
		zlib_source = file.read()

	with open( os.path.join(FILE_DIRECTORY, "display.server.lua") ) as file:
		display_source = file.read() #minify_lua_source()

	return download_source, zlib_source + "\n" + display_source
