
import numpy as np

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

DEFAULT_MAX_IMAGE_DIMENSIONS = (1280, 720)

def load_image_from_filepath( filepath : str ) -> Image.Image:
	return Image.open( filepath ).convert('RGB')

def image_to_pixel_data( image : Image.Image, image_size=DEFAULT_MAX_IMAGE_DIMENSIONS ) -> tuple[tuple, list]:
	'''
	Simple wrapper to return the image size and the flattened pixel array of the image.
	'''
	image = image.copy()
	image.thumbnail(image_size)
	return image.size, [ rgb for row in np.array( image ).tolist() for rgb in row ]

def load_image_file_pixel_data( filepath : str, image_size=DEFAULT_MAX_IMAGE_DIMENSIONS ) -> tuple[tuple, list]:
	img = load_image_from_filepath( filepath )
	return image_to_pixel_data( img, image_size=image_size )
