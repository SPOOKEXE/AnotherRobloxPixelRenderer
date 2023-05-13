
from os import path as os_path, remove
from subprocess import run as subprocess_run
from tempfile import gettempdir

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

LUA_EXE_FILE = os_path.join( "lua", "lua54.exe" )
COMMAND_LUA_MINIFY = os_path.join( "LuaMinify", "CommandLineMinify.lua" )

def minify_lua_source( source : str ) -> str:
	# filepaths for the in and out files
	temp_filepath = os_path.join( gettempdir(), "temp.lua" )
	out_filepath = os_path.join( gettempdir(), "temp_out.lua" )
	# write the source to the temporary file
	with open(temp_filepath, "w") as file:
		file.write(source)
	# clear the output file
	with open(out_filepath, "w") as file:
		file.write("")
	# TODO: MINIFY THE TEMPLATE FILE AND WRITE THE FILE TO THE OUT PATH
	with open(out_filepath, "w") as file:
		file.write(source)
	# read the minified file
	with open(out_filepath, "r") as file:
		source = file.read()
	# remove the temporary files
	remove(temp_filepath)
	remove(out_filepath)
	# return the minifyed source
	return source

def minify_lua_file( filepath : str ) -> str:
	# read the script contents
	file = open(filepath, "r")
	raw_code = file.read()
	file.close()
	# minify the code
	minified_code = minify_lua_source( raw_code )
	# write the code back to file
	file = open(filepath, "w")
	file.write(raw_code)
	# return the minified code
	return minified_code

minify_lua_file( os_path.join(FILE_DIRECTORY, "..", "scripts", "v1_compressor.lua") )
