DO_DUMP_TO_FILE = True

from os import path as os_path, makedirs
from sys import path as sys_path
from PIL import Image
from concurrent import futures
from json import dumps as json_dumps
from zlib import compress as zlib_compress

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )
sys_path.append( os_path.join(FILE_DIRECTORY, "../src/") )

from src.media import GetImageFromFile
from src.compression import ConvertImageToRawForRoblox

sys_path.pop()

JSON_DUMP_DIRECTORY = os_path.join( FILE_DIRECTORY, "dumps" )

def WriteCompressToFile( filename : str, linez : list ):
	global DO_DUMP_TO_FILE
	if not DO_DUMP_TO_FILE:
		return
	makedirs( os_path.split(filename)[0] , exist_ok=True)
	with open(filename, "w") as file:
		file.writelines(linez)

def TestForFile( filepath : str ) -> tuple[int, int, list]:
	filename = os_path.basename(filepath)
	global JSON_DUMP_DIRECTORY
	FILE_DUMP_DIRECTORY = os_path.join( JSON_DUMP_DIRECTORY, filename )
	
	test_image = GetImageFromFile( filepath, THUMB_SIZE=(480, 360) )
	print(test_image.size)
	test_pixels = list(test_image.getdata())

	# RAW
	raw_size = len( str(test_pixels) )
	print( "RAW: ", raw_size )
	values = ["["]
	for r,g,b in test_pixels:
		values.append(f"{r},{g},{b}")
		values.append(",")
	values.pop()
	values.append("]")
	with open( os_path.join(FILE_DIRECTORY, "raw.txt"), "w") as file:
		file.write(str(test_pixels).encode().hex())
	with open( os_path.join(FILE_DIRECTORY, "raw_zlib.txt"), "w") as file:
		file.write(zlib_compress( str(test_pixels).encode(), level=9).hex()) 

	WriteCompressToFile( os_path.join(FILE_DUMP_DIRECTORY, "source.json"), values)

	# COMPRESSION (greedy pixel + zlib)
	size_results = []
	for index, min_usage in enumerate([100]):#, 20, 50, 150]):#, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 250]):
		new_compressed_image = ConvertImageToRawForRoblox( test_image.copy(), MIN_USAGE_COUNT=min_usage )
		if index == 0:
			with open( os_path.join(FILE_DIRECTORY, "dump_size5.txt"), "w") as file:
				file.write(new_compressed_image)
		new_compressed_size = len(new_compressed_image)
		print( "NEW: ", new_compressed_size, " W/ USAGE ", min_usage )
		#pathtofile = os_path.join(FILE_DUMP_DIRECTORY, str(min_usage) + ".json")
		#WriteCompressToFile( pathtofile, [new_compressed_image] )
		size_results.append( [new_compressed_size, min_usage] )

	return filepath, raw_size, size_results

if __name__ == '__main__':
	files = [
		"E:\GitHub\AnotherRobloxPixelRenderer\\tests\\wallpaperflare.com_wallpaper.jpg"
	]

	executor = futures.ThreadPoolExecutor(max_workers=8)

	promises = []
	for filepath in files:
		promises.append( executor.submit(TestForFile, filepath) )
		# raw_size, new_comp_size = TestForFile( filepath )

	results = []
	for promise in futures.as_completed(promises):
		filepath, raw_size, new_comp_size = promise.result()
		results.append( [ filepath, raw_size, new_comp_size ] )

	with open( os_path.join(FILE_DIRECTORY, "results.json"), "w") as file:
		file.write( json_dumps( results, indent=4 ) )
