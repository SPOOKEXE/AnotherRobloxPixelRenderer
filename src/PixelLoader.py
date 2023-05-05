from PIL import Image

def GetImagePixels( filepath : str ) -> tuple[tuple, list]:
	img = Image.open(filepath)
	img.convert('RGB')
	img.thumbnail( (240, 180) )
	shape, data = (img.width, img.height), list(img.getdata())
	img.save('out.png')
	img.close()
	return shape, data

def RemoveParantheses(ref_string : str) -> str:
	return ref_string.replace("(", "").replace(")", "")

def TablifyArray(array_str : str) -> str:
	return array_str.replace("[", "{").replace("}", "}")

def BASIC_ToRobloxTableFormat( shape, pixels ) -> str:
	array = [ ]
	for pixel in pixels:
		array.extend( pixel[:3] )
	return str(array).replace(" ", "")

def GreedyFill( pixels, startIndex ) -> tuple[int, list]:
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

def ADV_GreedyRobloxTableFormat( shape, pixels ) -> str:
	new_pixels = []
	index = 1
	while index < len(pixels):
		count, fill_color = GreedyFill( pixels, index )
		fill_color = fill_color[:3]
		if count > 2:
			new_pixels.append('x'+str(count))
			new_pixels.extend(fill_color[:3])
			index += count
		else:
			new_pixels.extend(fill_color[:3])
			index += 1
	return str(new_pixels).replace(" ", "")

FILEPATH = "C:\\Users\\Declan\\Documents\\blah.jpg"
shape, pixels = GetImagePixels(FILEPATH)

print(shape)

table_str = ADV_GreedyRobloxTableFormat(shape, pixels)
with open("out2.txt", "w") as file:
	file.write(table_str)
