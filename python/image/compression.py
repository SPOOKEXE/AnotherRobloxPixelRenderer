
import zlib
import json
import numpy as np

from PIL import Image

def round_pixels_to_nearest( pixels : list, n=5 ) -> list:
	'''
	Round all pixel values to the nearest 'n' divisibility.
	'''
	return [ [ round(r/n), round(g/n), round(b/n) ] for r,g,b in pixels ]

def preprocesses_string( value : str ) -> str:
	'''
	Preprocess the passed string by removing spaces and stripping the edge whitespaces.
	'''
	return value.replace(' ', '').strip()

def split_to_rows_and_cols( pixels : list, image_size : tuple ) -> list[list]:
	t = np.reshape( pixels, (image_size[0], image_size[1], 3) ).tolist()
	return [list(x) for x in zip(*t)]

def complete_pixel_compression( img_size : tuple, pixels : list, zlib_level=9 ) -> str:
	'''
	#### Pipeline #1 for complete image compression:

	returns "{ zlib_level } | { img_dims } | { pixels }"

	with zlib compression applied on the pallete and pixels.
	'''
	# round the pixels
	pixels = round_pixels_to_nearest( pixels, n=5 )
	# split into rows / columns
	pixels = split_to_rows_and_cols( pixels, img_size )
	# preprocess pixels array string
	pixels = preprocesses_string(json.dumps(pixels))
	# zlib compression
	if zlib_level != None:
		pixels = zlib.compress(pixels.encode(), level=zlib_level).hex()
	# return the string
	return preprocesses_string( f"{img_size[0]},{img_size[1]}|{pixels}" )
