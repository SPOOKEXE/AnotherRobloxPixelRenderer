
local HttpService = game:GetService('HttpService')

-- Pixel part folder
local PixelsFolder = workspace:FindFirstChild('PixelBoard')
if not PixelsFolder then
	PixelsFolder = Instance.new('Folder')
	PixelsFolder.Name = 'PixelBoard'
	PixelsFolder.Parent = workspace
end

local function fromHex(str)
	return str:gsub('..', function(cc)
		return string.char(tonumber(cc, 16))
	end)
end

local function DecodePixelData( EncodedData )
	local data = string.split(EncodedData, '|')

	local imageSize, pixels_2d = data[1], data[2]

	imageSize = string.split(imageSize, ',')
	imageSize = { tonumber(imageSize[1]), tonumber(imageSize[2]) }

	pixels_2d = fromHex(pixels_2d)
	pixels_2d = Compression.Zlib.Decompress(pixels_2d)
	pixels_2d = HttpService:JSONDecode( pixels_2d )

	--return string.gsub( EncodedData, "'", '"' )
	return imageSize, pixels_2d
end

-- clear pixels
local step = (#PixelsFolder:GetChildren() / 60)
for index, child in ipairs( PixelsFolder:GetChildren() ) do
	child:Destroy()
	if index % step == 0 then
		task.wait()
	end
end

-- decode values
local Size, Pixels = DecodePixelData( _G.ImagePixelData )
print( Size, #Pixels, #Pixels[1] )

-- create parts
local origin = CFrame.new(-788, 200, 3483)

local pixelPart = Instance.new('Part')
pixelPart.Name = 'Pixel'
pixelPart.Anchored = true
pixelPart.TopSurface = Enum.SurfaceType.Smooth
pixelPart.BottomSurface = Enum.SurfaceType.Smooth
pixelPart.CanCollide = false
pixelPart.CanQuery = false
pixelPart.CanTouch = false
pixelPart.CastShadow = false
pixelPart.Massless = true
for rowN, row in ipairs( Pixels ) do
	local n = rowN * Size[1]
	for colN, pixel in ipairs( row ) do
		local cloneBlock = pixelPart:Clone()
		cloneBlock.CFrame = origin * CFrame.new( colN, rowN, 0 )
		cloneBlock.Color = Color3.fromRGB( 5 * tonumber(pixel[1]), 5 * tonumber(pixel[2]), 5 * tonumber(pixel[3]) )
		cloneBlock.Parent = PixelsFolder
		if (n + colN) % 500 == 0 then
			task.wait()
		end
	end
end
