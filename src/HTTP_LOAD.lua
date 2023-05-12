local URL = "https://hastebin.skyra.pw/raw/avococekah"

local HttpService = game:GetService('HttpService')

local Data = HttpService:GetAsync(URL, true)
_G.V111 = Data
