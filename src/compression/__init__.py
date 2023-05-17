import zlib

from PIL import Image
from compression.v2 import ConvertImageToDataString as V2Compression

def CompressString( source : str, level=9 ) -> str:
	return zlib.compress(source.encode(), level=level).hex()

def ConvertImageToRawForRoblox( img : Image.Image, MIN_USAGE_COUNT=5, zlib=True ) -> str:
	source = V2Compression(img, MIN_USAGE_COUNT=MIN_USAGE_COUNT)
	# if zlib:
	# 	source = CompressString(source)
	return source
