
# manually use pastebin until issue is fixed with minifier
# rh/URL_HERE
# https://hastebin.skyra.pw/
# https://hastebin.skyra.pw/raw/{ID}

import os
import sys
import _thread

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join( FILE_DIRECTORY, ".." ) )

from roblox import prepare_scripts
from python import complete_pixel_compression, load_image_file_pixel_data, default_start, LocalHost, Ngrok

sys.path.pop()

# start localhost and ngrok
_thread.start_new_thread( default_start, () )

# generate the roblox script to request to the server (SERVER OWNER)
ngrok_addr = Ngrok.await_ngrok_addr()
print( ngrok_addr )

# roblox scripts to run (output to file)
def prep_scripts_to_file( ngrok_addr ):
	download_src, display_src = prepare_scripts( ngrok_addr )
	with open("download_minified.lua", "w") as file:
		file.write( download_src )
	with open("display_minified.lua", "w") as file:
		file.write( display_src )
prep_scripts_to_file( ngrok_addr )

# main upload loop
def parse_filepath( filepath : str ) -> None:
	if not os.path.exists(filepath):
		print("Filepath does not exist.")
		return
	img_size, pixels = load_image_file_pixel_data( filepath )
	pixels = complete_pixel_compression( img_size, pixels, zlib_level=9 )
	LocalHost.SET_HOSTED_RAW_DATA(pixels)
	print("Host is now hosting the raw pixel data.")

parse_filepath( os.path.join( FILE_DIRECTORY, "jghjghfd.PNG" ) )
while True:
	print("Input a filepath, otherwise input 'x1' to refresh minified files.")
	filepath = input()
	if filepath == "x1":
		prep_scripts_to_file( ngrok_addr )
	else:
		parse_filepath( filepath )
