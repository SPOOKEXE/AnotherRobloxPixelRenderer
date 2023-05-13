-- // PIXEL DATA GRABBER // --

local URL = "&&&&"

local HttpService = game:GetService("HttpService")

local function ReformatPythonArray( PythonArrayString )
	return string.gsub(PythonArrayString, "'", '"')
end

print("pulling pixel data from host")

local Data = HttpService:GetAsync(URL, true)
Data = ReformatPythonArray(Data)

print("got pixel data from host - setting value under _G.PixelData")

_G.PixelData = Data
