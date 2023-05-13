
from localhost import SetupLocalHost, SET_HOSTED_RAW_DATA
from ngrok import LocalHostTunnel, ngrok
from media import GetImageFromFile
from roblox import GenerateRobloxScript
from compression import v1 as CompressV1, v2 as CompressV2

# DISPLAY RATIO: 16:9
#THUMBNAIL_SIZE = (1280, 720) # 720p
THUMBNAIL_SIZE = (640, 480) # 480p
#THUMBNAIL_SIZE = (480, 360) # 360p
#THUMBNAIL_SIZE = (192, 144) # 144p

def default_setup(PORT = 5100):
	webserver = SetupLocalHost(port=PORT)
	ngrok_wrapper = LocalHostTunnel(port=PORT)
	ngrok_wrapper.open_tunnel()
	print("NGROK Address is: ")
	print(ngrok_wrapper.get_ngrok_addr())
	return webserver, ngrok_wrapper

def run_input() -> str:
	print("Input the filepath to the image: ")
	filepath = input("")
	image = GetImageFromFile( filepath, THUMB_SIZE=THUMBNAIL_SIZE )
	data = CompressV2.ConvertImageToDataString( image )
	SET_HOSTED_RAW_DATA(data)
	print("Data is now hosted - run the (same) loader script again.")

if __name__ == '__main__':
	# create the localhost server and ngrok tunnel
	webserver, ngrok_wrapper = default_setup()
	# generate the roblox script to connect to the tunnel & localhost
	GenerateRobloxScript( ngrok_wrapper.get_ngrok_addr(), 2 )
	# allow the user to update active data on the localhost
	while True:
		try:
			run_input()
		except KeyboardInterrupt:
			break
		except Exception as exception:
			print("Error occurred: ")
			print(exception)
	# when exited, close the ngrok tunnel and webserver
	try:
		ngrok.disconnect(ngrok_wrapper.get_ngrok_addr())
	except:
		pass
	webserver.shutdown()
