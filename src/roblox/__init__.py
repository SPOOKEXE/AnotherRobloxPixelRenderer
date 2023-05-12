
from os import path as os_path, popen

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

def GenerateRobloxScript( ngrok_url : str, script="v1_compressor.lua" ) -> str:
	raw_code = ""
	with open( os_path.join(FILE_DIRECTORY, script), "r" ) as file:
		raw_code = file.read()

	new_code = raw_code.replace("&&&&", ngrok_url)

	filepath = os_path.join(FILE_DIRECTORY, "..", "..", "loader.lua")
	with open( filepath, "w") as file:
		file.write(new_code)

	popen("notepad " + filepath)

	return raw_code