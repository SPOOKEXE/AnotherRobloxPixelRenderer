
from src.localhost import SetupLocalHost, SET_HOSTED_RAW_DATA
from src.ngrok import LocalHostTunnel, ngrok
from src.media import GetImageFromFile
from src.roblox import GenerateRobloxScript
from src.compression import v1 as CompressV1, v2 as CompressV2

#THUMBNAIL_SIZE = (900, 675)
THUMBNAIL_SIZE = (450, 337)

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
	data = CompressV1.ConvertImageToDataString( image )
	SET_HOSTED_RAW_DATA(data)
	print("Data is now hosted - run the (same) loader script again.")

if __name__ == '__main__':
	# create the localhost server and ngrok tunnel
	webserver, ngrok_wrapper = default_setup()
	# generate the roblox script to connect to the tunnel & localhost
	GenerateRobloxScript( ngrok_wrapper.get_ngrok_addr() )
	# allow the user to update active data on the localhost
	while True:
		try:
			run_input()
		except KeyboardInterrupt:
			break
		except Exception as exception:
			print("Error occurred: ")
			print(exception)
	# when exited
	# close the ngrok tunnel
	try:
		ngrok.disconnect(ngrok_wrapper.get_ngrok_addr())
	except:
		pass
	# close the localhost server
	webserver.shutdown()
