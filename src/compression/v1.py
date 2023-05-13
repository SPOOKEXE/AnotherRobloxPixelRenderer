
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
			new_pixels.extend(fill_color[:3])
			index += count
		else:
			new_pixels.extend(fill_color[:3])
			index += 1
	return str(new_pixels).replace(" ", "")

def ConvertImageToDataString( img : Image.Image ) -> str:
	data = str( _greedy_fill_extended( list(img.getdata()) ) )
	data = f"{str(list(img.size))}&{data}"
	# with open('out.txt', 'w') as file:
	# 	file.write(data)
	return data
