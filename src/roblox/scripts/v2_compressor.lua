
-- // PIXEL LOADER // --
if not _G.PixelData then
	error("You must pull the PixelData from the host using the 'pull_data.lua'")
end

local HttpService = game:GetService('HttpService')

local Shape, RawPixels = unpack(string.split(_G.PixelData, "&"))
print(Shape)
Shape = HttpService:JSONDecode(Shape)
RawPixels = HttpService:JSONDecode(RawPixels)

print("loaded pixel data")


