
from PIL import Image
from json import dumps as json_dumps

def GetFrequentColors( img : Image.Image, MIN_USAGE_COUNT=5 ) -> dict[str : int]:
	# frequencies of "r-g-b" -> counter
	temp_frequencies = { }
	temp_pallete = { }
	# pallete of "r-g-b" -> [ r,g,b ]
	for r,g,b in list(img.getdata()):
		idx = f"{r},{g},{b}"
		if temp_frequencies.get(idx):
			temp_frequencies[idx] += 1
		else:
			temp_frequencies[idx] = 1
			temp_pallete[idx] = [r,g,b]
	# only get the most frequently appearing
	frequencies = {}
	pallete = {}
	for k, v in temp_frequencies.items():
		if v > MIN_USAGE_COUNT:
			frequencies[k] = v
			pallete[k] = temp_pallete[k]
	# return the frequency stuff
	return frequencies, pallete

def GetRepititionPalleteFill( img : Image.Image, MIN_USAGE_COUNT=5 ) -> tuple[list, list]:
	frequencies, pallete = GetFrequentColors( img, MIN_USAGE_COUNT=MIN_USAGE_COUNT )
	pallete_to_index = { }
	pixel_pallete = []
	pixel_array = []
	for r,g,b in list(img.getdata()):
		idx = f"{r},{g},{b}"
		if frequencies.get(idx):
			if not pallete_to_index.get( idx ):
				pixel_pallete.extend( pallete[idx] )
				pallete_to_index[ idx ] = len(pixel_pallete)-1
			pixel_array.append(f"x{pallete_to_index[idx]}")
		else:
			pixel_array.extend([r,g,b])
	return pixel_array, pixel_pallete

def _greedy_fill( pixels, startIndex ) -> tuple[int, list]:
	value = pixels[startIndex]
	count = 1
	while startIndex < len(pixels) - 1:
		startIndex += 1
		idx_value = pixels[ startIndex ]
		if value == idx_value:
			count += 1
		else:
			break
	return count, value

def _greedy_fill_extended( pixels ) -> str:
	new_pixels = []
	index = 1
	while index < len(pixels):
		count, value = _greedy_fill( pixels, index )
		if count > 2:
			new_pixels.append(str(count) + 'y' + str(value))
			index += count
		else:
			new_pixels.append(value)
			index += 1
	return new_pixels

def GreedyFillRepititionPallete( pixels ) -> tuple[list, list]:
	return _greedy_fill_extended( pixels )

def ConvertImageToDataString( img : Image.Image, MIN_USAGE_COUNT=5 ) -> str:
	# COMPRESS HERE
	pixel_array, pixel_pallete = GetRepititionPalleteFill( img, MIN_USAGE_COUNT=MIN_USAGE_COUNT )
	pixel_array = GreedyFillRepititionPallete( pixel_array )
	string_array = []
	for value in pixel_array:
		if type(value) == list:
			string_array.extend(value)
		else:
			string_array.append(value)
	return str(list(img.size)) + "&[" + json_dumps(pixel_pallete).replace(" ", "") + "," + json_dumps(string_array).replace(" ", "") + "]"
