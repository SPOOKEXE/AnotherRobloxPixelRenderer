
from os import path as os_path, remove
from tempfile import gettempdir
from subprocess import run as subprocess_run

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

# https://sourceforge.net/projects/luabinaries/

def minify_lua_source( source : str, level='full' ) -> str:
	# filepaths for the in and out files
	temp_filepath = os_path.join( gettempdir(), "temp.lua" )
	out_filepath = os_path.join( gettempdir(), "temp_out.lua" )
	# write the source to the temporary file
	with open(temp_filepath, "w") as file:
		file.write(source)
	with open(out_filepath, "w") as file:
		file.write('')
	subprocess_run([
		os_path.join(FILE_DIRECTORY, 'lua54.exe'),
		os_path.join(FILE_DIRECTORY, 'minify.lua'),
		'minify',
		os_path.join(FILE_DIRECTORY, temp_filepath),
	], stdout=open(os_path.join(FILE_DIRECTORY, out_filepath), 'w'))
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
