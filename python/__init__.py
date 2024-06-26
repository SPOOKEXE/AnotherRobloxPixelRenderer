
from .image import complete_pixel_compression, load_image_file_pixel_data#, complete_pixel_reconstruction
from .network import LocalHost, Ngrok

class ImageSize:
	# DISPLAY RATIO: 16:9
	SIZE_720p = (1280, 720)
	SIZE_480p = (640, 480)
	SIZE_360p = (480, 360)
	SIZE_144p = (192, 144)

def request_user( ) -> None:
	print("Input the filepath to the target image: ")
	filepath = input("")
	shape, pixels = load_image_file_pixel_data( filepath, image_size=ImageSize.SIZE_480p )
	output = complete_pixel_compression( shape, pixels, zlib_level=9 )
	LocalHost.SET_HOSTED_RAW_DATA( output )
	print("Now hosted on localhost webserver.")

def default_start(port=5100) -> None:
	# localhost webserver
	webserver = LocalHost.start_local_host( port )

	# ngrok tunnel
	Ngrok.set_port( port )
	Ngrok.open_tunnel( )

	# ngrok ip
	print("NGROK Address is: ")
	print(Ngrok.get_ngrok_addr())

	# main loop
	while True:
		try:
			request_user()
		except KeyboardInterrupt:
			break
		except Exception as exception:
			print( "Error occurred: " )
			print( exception )

	try:
		Ngrok.close_tunnel( )
	except:
		pass

	webserver.shutdown()
