
from os import path as os_path, remove
from tempfile import gettempdir
from subprocess import run as subprocess_run

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

def minify_lua_source( source : str ) -> str:
	# filepaths for the in and out files
	temp_filepath = os_path.join( gettempdir(), "temp.lua" )
	out_filepath = os_path.join( gettempdir(), "temp_out.lua" )
	# write the source to the temporary file
	with open(temp_filepath, "w") as file:
		file.write(source)
	subprocess_run([
		os_path.join(FILE_DIRECTORY, 'lua51.exe'),
		os_path.join(FILE_DIRECTORY, 'simpleSquishCl.lua'),
		os_path.join(FILE_DIRECTORY, temp_filepath),
		os_path.join(FILE_DIRECTORY, out_filepath),
		'--minify-level=full'
	])
	# read the minified file
	with open(out_filepath, "r") as file:
		source = file.read()
	source = source.replace("\n", " ")
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

#minify_lua_file( os_path.join(FILE_DIRECTORY, "..", "scripts", "v1_compressor.lua") )
