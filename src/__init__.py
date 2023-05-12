from localhost import SetupLocalHost, SET_HOSTED_RAW_DATA
from ngrok import LocalHostTunnel
from media import ConvertImageToDataString, GetImageFromFile
from roblox import GenerateRobloxScript

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
	image = GetImageFromFile( filepath )
	data = ConvertImageToDataString( image )
	SET_HOSTED_RAW_DATA(data)
	print("Data is now hosted - run the (same) loader script again.")

if __name__ == '__main__':
	webserver, ngrok_wrapper = default_setup()
	GenerateRobloxScript( ngrok_wrapper.get_ngrok_addr() )
	while True:
		try:
			run_input()
		except KeyboardInterrupt:
			break
		except Exception as exception:
			print("Error occurred: ")
			print(exception)
	ngrok_wrapper.close_tunnel()
	webserver.shutdown()
