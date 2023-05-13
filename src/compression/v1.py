
from math import floor
from PIL import Image

def _greedy_fill( pixels, startIndex ) -> tuple[int, list]:
	color_value = pixels[startIndex]
	want_this_color = str(color_value)
	count = 1
	while startIndex < len(pixels) - 1:
		startIndex += 1
		value = pixels[ startIndex ]
		if str( value ) == want_this_color:
			count += 1
		else:
			break
	return count, color_value

def _greedy_fill_extended( pixels ) -> str:
	new_pixels = []
	index = 1
	while index < len(pixels):
		count, fill_color = _greedy_fill( pixels, index )
		fill_color = fill_color[:3]
		if count > 2:
			new_pixels.append('x'+str(count))
			new_pixels.extend(fill_color)
			index += count
		else:
			new_pixels.extend(fill_color)
			index += 1
	return str(new_pixels).replace(" ", "")

def round_pixels_to_nearest_fifth( pixels : list ) -> list:
	new_pixels = []
	for r,g,b in pixels:
		new_pixels.append( [floor(r/5) * 5, floor(g/5) * 5, floor(b/5) * 5] )
	return new_pixels

def ConvertImageToDataString( img : Image.Image ) -> str:
	pixels = list(img.getdata())
	rounded_pixels = round_pixels_to_nearest_fifth( pixels )
	data = str( _greedy_fill_extended(rounded_pixels) )
	data = f"{str(list(img.size))}&{data}"
	# with open('out.txt', 'w') as file:
	# 	file.write(data)
	return data
