
import zlib
import json
import numpy as np

from PIL import Image

class GreedyPixelCompression:

	@staticmethod
	def greedy_fill_search( pixels : list, startIndex : int ) -> tuple[int, list]:
		'''
		With the value at the startIndex in the pixels list, search every item after this one and see how many items are counted before the value changes.
		'''
		matchValue = pixels[startIndex]
		count = 1
		while startIndex < len(pixels) - 1:
			indexValue = pixels[ startIndex ]
			if matchValue != indexValue:
				break
			count += 1
			startIndex += 1
		return count, matchValue

	@staticmethod
	def greedy_fill_extended( values : list, sep='y', minimum=2 ) -> list:
		'''
		Run the greedy fill algorithm and replace n occurances with "{value}{sep}{n}".
		'''
		new_values = []
		index = 0
		while index < len(values):
			count, value = GreedyPixelCompression.greedy_fill_search( values, index )
			if count > minimum:
				new_values.append( f"{str(value)}{sep}{str(count)}" )
			else:
				new_values.append( value )
			index += max(count, 1)
		return new_values

	@staticmethod
	def get_frequent_colors( pixels : list, min_usage=3 ) -> tuple[dict, dict]:
		'''
		Returns two dictionaries as a tuple.

		Dictionary A is the frequency at which this pixel occurs.

		Dictionary B is the hash index of the RGB color to a list of the RGB data.
		'''
		# frequencies of "r-g-b" -> counter
		temp_frequencies = { }
		# pallete of "r-g-b" -> [ r,g,b ]
		temp_pallete = { }
		for r,g,b in pixels:
			idx = f"{r},{g},{b}"
			if temp_frequencies.get(idx):
				temp_frequencies[idx] += 1
			else:
				temp_frequencies[idx] = 1
				temp_pallete[idx] = [r,g,b]
		# only get the most frequently appearing and ignore the rest
		frequencies = {}
		pallete = {}
		for k, v in temp_frequencies.items():
			if v > min_usage:
				frequencies[k] = v
				pallete[k] = temp_pallete[k]
		# return the frequency stuff
		return frequencies, pallete

	@staticmethod
	def compress_row( row : list[list], pallete : dict ) -> list[list]:
		frequencies, pallete = GreedyPixelCompression.get_frequent_colors( row, min_usage=3 )
		new_pixel_array = [ ]
		new_pallete_array = [ ]
		for r,g,b in row:
			# cache index
			idx = f"{r},{g},{b}"
			# if did not appear frequent enough
			if frequencies.get(idx) == None:
				new_pixel_array.append([r,g,b])
				continue
			# if not cached yet, cache it
			cacheId = pallete.get( idx )
			if cacheId == None:
				new_pallete_array.append( pallete[idx] )
				cacheId = len(new_pallete_array)
				pallete[ idx ] = cacheId
			# append new pixel
			new_pixel_array.append(f"{cacheId}")
		return new_pixel_array, new_pallete_array

	@staticmethod
	def compress_rows_to_pallete( pixels : list[list] ) -> tuple[dict, list[list]]:
		pallete = { }
		return [ GreedyPixelCompression.compress_row(row, pallete) for row in pixels ], pallete

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

def split_to_rounds_cols( pixels : list, image_size : tuple ) -> list[list]:
	return np.reshape( pixels, (image_size[0], image_size[1], 3) ).tolist()

def complete_pixel_compression( img_size : tuple, pixels : list, zlib_level=9 ) -> str:
	'''
	#### Pipeline #1 for complete image compression:

	returns "{ zlib_level } | { img_dims } | { pixels }"

	with zlib compression applied on the pallete and pixels.
	'''
	# round the pixels
	pixels = round_pixels_to_nearest( pixels, n=5 )
	# split into rows / columns
	pixels = split_to_rounds_cols( pixels, img_size )
	# compress pallete
	pixels, pallete_dict = GreedyPixelCompression.compress_rows_to_pallete( pixels )
	# compress rows
	pixels = GreedyPixelCompression.greedy_fill_extended( pixels, sep='y' )
	# preprocess pixels array string
	pallete_dict = preprocesses_string(json.dumps(pallete_dict, indent=4))
	pixels = preprocesses_string(json.dumps(pixels, indent=4))
	# zlib compression
	if zlib_level != None:
		pixels = zlib.compress(pixels.encode(), level=zlib_level).hex()
		pallete_dict = zlib.compress(pallete_dict.encode(), level=zlib_level).hex()
	# return the string
	return preprocesses_string( f"{img_size[0]},{img_size[1]}|{pallete_dict}|{pixels}" )


