
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
	def greedy_pallete_fill_pixels( pixels : list ) -> tuple[list, dict]:
		'''
		Compress the given array of RGB pixels with the greedy fill algorithm and frequent colors replacement algorithm.
		'''
		frequencies, pallete = GreedyPixelCompression.get_frequent_colors( pixels )

		new_pixel_array = [ ]
		new_pallete_array = [ ]
		pallete_index_cache = { }

		for r,g,b in pixels:
			# cache index
			idx = f"{r},{g},{b}"
			# if did not appear frequent enough
			if frequencies.get(idx) == None:
				new_pixel_array.append([r,g,b])
				continue
			# if not cached yet, cache it
			cacheId = pallete_index_cache.get( idx )
			if cacheId == None:
				new_pallete_array.append( pallete[idx] )
				cacheId = len(new_pallete_array)
				pallete_index_cache[ idx ] = cacheId
			# append new pixel
			new_pixel_array.append(f"{cacheId}")

		return new_pixel_array, new_pallete_array

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

def complete_pixel_compression( img_size : tuple, pixels : list, zlib_level=9 ) -> str:
	'''
	#### Pipeline #1 for complete image compression:

	returns "{ zlib_level } | { img_dims } | {pallete} | { pixels }"

	with zlib compression applied on the pallete and pixels.
	'''
	# round the pixels
	pixels = round_pixels_to_nearest( pixels, n=5 )
	# pallete greedy-fill pixels
	pixels, pallete_dict = GreedyPixelCompression.greedy_pallete_fill_pixels( pixels )
	# similar-pallete id greedy fill
	pixels = GreedyPixelCompression.greedy_fill_extended( pixels, sep='y' )
	# preprocess pixels array string
	pixels = preprocesses_string(json.dumps(pixels))
	pallete_dict = preprocesses_string(json.dumps(pallete_dict))
	# zlib compression
	if zlib_level != None:
		pallete_dict = zlib.compress( pallete_dict.encode(), level=zlib_level ).hex()
		pixels = zlib.compress(pixels.encode(), level=zlib_level).hex()
	# return the string
	return preprocesses_string( f"{img_size[0]},{img_size[1]}|{pallete_dict}|{pixels}" )

def complete_pixel_reconstruction( compressed_string : str ) -> Image.Image:

	shape, pallete, pixels = compressed_string.split('|')

	pallete = zlib.decompress( bytes.fromhex(pallete) )
	pallete = json.loads( pallete )

	pixels = zlib.decompress( bytes.fromhex(pixels) )
	pixels = json.loads( pixels )

	with open('debug.json', 'w') as file:
		file.write( str(pallete).replace(' ', '').strip() + "\n\n\n" + str(pixels).replace(' ', '').strip() )

	def unpack_pixels( values : list, pallete_list : list ) -> list:
		new_pixels = []
		counter = 0
		for value in values:
			if str(value).count('y') == 0:
				new_pixels.append( value )
				continue
			left, right = value.split('y')
			counter += int(right)
			if type(left) == str:
				if left.find(',') == -1:
					new_pixels.extend( [ pallete_list[int(left)-1] ] * int(right) )
				else:
					new_pixels.extend( [ json.loads(left) ] * int(right) )
			elif type(left) == int:
				new_pixels.extend( [ pallete_list[int(left)-1] ] * int(right) )
			elif type(left) == list:
				new_pixels.extend( [left] * int(right) )
			# print(left, type(left), right)
		print(counter)
		return new_pixels

	pixels = unpack_pixels( pixels, pallete )

	with open('debug2.json', "w") as file:
		file.write( json.dumps(pixels).replace(' ', '').strip() )

	width, height = shape.split(',')
	print( width, height )
	pixels = np.reshape(pixels, ( int(height), int(width), 3 ))
	return Image.fromarray( pixels, mode='RGB' )
