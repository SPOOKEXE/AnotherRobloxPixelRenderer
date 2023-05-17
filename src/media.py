
from PIL import Image

def GetImageFromFile( filepath : str, THUMB_SIZE=(600,600) ) -> Image.Image:
	img = Image.open(filepath)
	img.thumbnail( THUMB_SIZE )
	rgb = img.convert("RGB")
	img.close()
	return rgb
