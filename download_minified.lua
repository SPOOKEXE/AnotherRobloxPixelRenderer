
local NGROK_TUNNEL_URL = 'https://597ecb7fc882.ngrok.app'

print('Downloading Image from NGROK tunnel.')

_G.ImagePixelData = game:GetService('HttpService'):GetAsync( NGROK_TUNNEL_URL, true )

print('Downloaded Image from NGROK tunnel.')
print(#_G.ImagePixelData)
