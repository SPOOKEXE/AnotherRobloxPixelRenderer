print("Deleting items under terrain")
for _, Model in ipairs( workspace.Terrain:GetChildren() ) do
	for i, Child in ipairs( Model:GetChildren() ) do
		Child:Destroy()
		if i%100 == 0 then
			task.wait()
		end
	end
end

local SCALE = 0.1

if not _G.PixelData then
	error("You must pull the data from the host.")
end

local HttpService = game:GetService('HttpService')

print("Loading Data from global")
local Shape, Data = unpack(string.split(_G.PixelData, "&"))
Shape = HttpService:JSONDecode(Shape)
Data = HttpService:JSONDecode(Data)

local Width, Height = unpack(Shape)
print("Loaded image with shape; ", Width, Height)

local UnpackedPallete = Data[1]
local PackedPixels = Data[2]

local Model = Instance.new('Model')
Model.Name = time()
Model.Parent = workspace.Terrain

local ReferencePart = Instance.new('Part')
ReferencePart.Name = 'Pixel'
ReferencePart.Anchored = true
ReferencePart.CanCollide = false
ReferencePart.CanTouch = false
ReferencePart.CanQuery = false
ReferencePart.CastShadow = false
ReferencePart.Massless = true
ReferencePart.Color = Color3.new(1,1,1)
ReferencePart.Size = Vector3.new(SCALE, SCALE, SCALE)

-- TODO: Greedy Fill Color (along rows, then along columns)

local OriginCFrame = game:GetService('Players').SPOOK_EXE.Character:GetPivot()
OriginCFrame = OriginCFrame * CFrame.new((Width/2) * -SCALE, 1 + (Height * SCALE), 0)

local StorePixelsInThis = false

local function CreatePixelBlock( Index, R, G, B, CFrame )
	local NewPixel = ReferencePart:Clone()
	NewPixel.Name = Index
	NewPixel.Color = Color3.fromRGB(R*15,G*15,B*15)
	NewPixel.CFrame = CFrame
	NewPixel.Parent = StorePixelsInThis
end

print("Repacking Pallete - ", #UnpackedPallete)
local Pallete = { }

local index = 1
while index < #UnpackedPallete do
	table.insert(Pallete, { UnpackedPallete[index], UnpackedPallete[index+1], UnpackedPallete[index+2] } )
	index = index + 3
end

print("Repacked Pallete - ", #Pallete)

print("Unpacking Image - ", #PackedPixels)

local Pixels = {}
for _, Value in ipairs( PackedPixels ) do
	if typeof(Value) == "number" then
		table.insert(Pixels, Value)
	else
		local Splits = string.split(Value, "y")
		if #Splits == 1 then
			table.insert(Pixels, Value) -- is just x#
		else -- is #yx#
			for _ = 1, tonumber(Splits[1]) do
				table.insert(Pixels, Splits[2])
			end
		end
	end
end

print("Loading Image - ", #Pixels)

index = 1
local actualIndex = 0
while index <= #Pixels do
	local Row = math.floor(actualIndex / Width)
	local Column = (actualIndex % Width)

	if (index == 1) or (index % 1000 == 0) then
		StorePixelsInThis = Instance.new('Model')
		StorePixelsInThis.Name = index
		StorePixelsInThis.Parent = Model
	end

	local OffsetCFrame = OriginCFrame * CFrame.new(Column * SCALE, -Row * SCALE, 0)

	local Value = Pixels[index]
	if typeof(Value) == "number" or tonumber(Value) then
		-- normal pixel values
		Value = tonumber(Value)
		local G, B = Pixels[index+1], Pixels[index+2]
		CreatePixelBlock(index, Value, G, B, OffsetCFrame )
		index = index + 3
	else
		-- compressed pixels
		local RGB = Pallete[ tonumber(string.sub(Value, 2)) ]
		CreatePixelBlock(index, RGB[1], RGB[2], RGB[3], OffsetCFrame )
		index = index + 1
	end
	actualIndex = actualIndex + 1
end

print("Loaded Image")