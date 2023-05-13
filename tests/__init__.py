DO_DUMP_TO_FILE = False

from os import path as os_path, makedirs
from sys import path as sys_path
from PIL import Image
from concurrent import futures
from json import dumps as json_dumps

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )
sys_path.append( os_path.join(FILE_DIRECTORY, "../src/") )

from src.compression import v1 as CompressV1, v2 as CompressV2
from src.media import GetImageFromFile

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
	
	test_image = GetImageFromFile( filepath, THUMB_SIZE=(1280, 720) )
	test_pixels = list(test_image.getdata())

	# RAW
	# 578,084
	raw_size = len( str(test_pixels) )
	print( "RAW: ", raw_size )
	values = ["["]
	for r,g,b in test_pixels:
		values.append(f"{r},{g},{b}")
		values.append(",")
	values.pop()
	values.append("]")
	WriteCompressToFile( os_path.join(FILE_DUMP_DIRECTORY, "source.json"), values)

	# GREEDY CURRENT
	# 215,106
	curr_compressed_image = CompressV1.ConvertImageToDataString( test_image.copy() )
	curr_compressed_size = len(curr_compressed_image)
	print( "CURR: ", curr_compressed_size )
	WriteCompressToFile( os_path.join(FILE_DUMP_DIRECTORY, "current.json"), [curr_compressed_image] )

	# NEW MULTI
	# 83,316 (MIN_USAGE_COUNT = 5)
	size_results = []
	for index, min_usage in enumerate([3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 250]):
		new_compressed_image = CompressV2.ConvertImageToDataString( test_image.copy(), MIN_USAGE_COUNT=min_usage )
		if index == 2:
			with open( os_path.join(FILE_DIRECTORY, "dump.txt"), "w") as file:
				file.write(new_compressed_image)
		new_compressed_size = len(new_compressed_image)
		print( "NEW: ", new_compressed_size, " W/ USAGE ", min_usage )
		pathtofile = os_path.join(FILE_DUMP_DIRECTORY, str(min_usage) + ".json")
		WriteCompressToFile( pathtofile, [new_compressed_image] )
		if curr_compressed_size < new_compressed_size:
			print("Current compression is better. ")
			print( min_usage )
			print( new_compressed_size - curr_compressed_size, "character improvement" )
		elif curr_compressed_size > new_compressed_size:
			print("New compression is better. ")
			print( min_usage )
			print( curr_compressed_size - new_compressed_size, "character improvement" )
		size_results.append( [new_compressed_size, min_usage] )

	return filepath, raw_size, curr_compressed_size, size_results

if __name__ == '__main__':
	files = [
		"C:\\Users\\Declan\\Music\\356280sample.jpg"
	]

	executor = futures.ThreadPoolExecutor(max_workers=8)

	promises = []
	for filepath in files:
		promises.append( executor.submit(TestForFile, filepath) )
		# raw_size, current_comp_size, new_comp_size = TestForFile( filepath )

	results = []
	for promise in futures.as_completed(promises):
		filepath, raw_size, current_comp_size, new_comp_size = promise.result()
		results.append( [ filepath, raw_size, current_comp_size, new_comp_size ] )

	with open( os_path.join(FILE_DIRECTORY, "results.json"), "w") as file:
		file.write( json_dumps( results, indent=4 ) )
