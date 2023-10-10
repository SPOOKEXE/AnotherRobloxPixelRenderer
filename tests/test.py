import os
import sys

from PIL import Image

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

sys.path.append( os.path.join( FILE_DIRECTORY, ".." ) )

import src as pixel_renderer

sys.path.pop()

if __name__ == '__main__':
	filepath = os.path.join( FILE_DIRECTORY, "80707-lametta_v2012.jpeg" )
	# shape, values = pixel_renderer.load_image_file_pixel_data( filepath, image_size=pixel_renderer.ImageSize.SIZE_360p )

	# result = pixel_renderer.complete_pixel_compression( shape, values, zlib_level=9 )
	# print( result )

	# with open("output.json", "w") as file:
	# 	file.write( result )

	# print(len(str(shape).replace(' ', '')) + len(str(values).replace(' ', '')), len(result))

	with open("output.json", "r") as file:
		data = file.read()

	# Image.open(filepath).show()

	img = pixel_renderer.complete_pixel_reconstruction( data )
	img.show()
