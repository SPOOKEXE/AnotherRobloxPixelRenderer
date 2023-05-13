
from os import path as os_path, popen
from tempfile import gettempdir
from roblox.minify import minify_lua_source

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

def GetScriptFileSource( filename : str ) -> str:
	filepath = os_path.join( FILE_DIRECTORY, "scripts", filename )
	if not os_path.exists( filepath ):
		return f"-- no script file available for compressor '{filename}'"
	data = None
	with open(filepath, "r") as file:
		data = file.read()
	return data

def GenerateRobloxScript( ngrok_url : str, compressor=1 ) -> str:
	raw_code = ""
	with open( os_path.join(FILE_DIRECTORY, "base.lua"), "r" ) as file:
		raw_code = file.read()

	ngrok_code = minify_lua_source( raw_code.replace("&&&&", ngrok_url) )
	compressor_source = minify_lua_source( GetScriptFileSource(f"v{compressor}_compressor.lua") )

	new_code = ngrok_code + ("\n"*3) + compressor_source

	filepath = os_path.join(gettempdir(), "pull_data.lua")
	with open( filepath, "w") as file:
		file.write(new_code)

	popen("notepad " + filepath)

	return raw_code