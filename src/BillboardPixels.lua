local HttpService = game:GetService("HttpService")

local SCALE = 2

local function ReformatPythonArray( PythonArrayString )
	return string.gsub(PythonArrayString, "'", '"')
end

local Functions = { }

function Functions.LoadNext(self)
	if not self.Billboard then
		return
	end

	if not self.CurrentIndex then
		self.CurrentIndex = 1
	end

	local Data = self.DataRaw
	if not self.DataLength then
		self.DataLength = #Data
	end

	if self.CurrentIndex >= self.DataLength then
		return false
	end

	local Pixels = { }

	local value = Data[self.CurrentIndex]
	if string.find(value, 'x') then
		local R, G, B = Data[self.CurrentIndex+1], Data[self.CurrentIndex+2], Data[self.CurrentIndex+3]
		local repetitions = tonumber(string.sub(value, 2, #value))
		for _ = 1, repetitions do
			table.insert(Pixels, {R, G, B})
		end
		self.CurrentIndex += 4
	else
		local R, G, B = Data[self.CurrentIndex], Data[self.CurrentIndex+1], Data[self.CurrentIndex+2]
		table.insert(Pixels, {R, G, B})
		self.CurrentIndex += 3
	end

	local pixelIndex = self.PixelNumber
	for index, pixelColor in ipairs(Pixels) do
		local actualIndex = (self.PixelNumber + index)
		local Row = math.floor(actualIndex / self.ImageWidth)
		local Column = actualIndex % self.ImageWidth

		local R,G,B = unpack(pixelColor)

		local NewPixel = self.ReferenceFrame:Clone()
		NewPixel.Name = actualIndex
		NewPixel.BackgroundColor3 = Color3.fromRGB(R,G,B)
		NewPixel.LayoutOrder = actualIndex
		NewPixel.Position = UDim2.fromOffset(Column * SCALE, Row * SCALE)
		NewPixel.Parent = self.Billboard

		if index % 2500 == 0 then
			task.wait()
		end
	end

	self.PixelNumber = (pixelIndex + #Pixels)

	return true
end

function Functions.LoadAll(self)
	local Counter = 0
	while Functions.LoadNext(self) do
		if Counter % 500 == 0 then
			Counter = 0
			task.wait()
		end
		Counter += 1
	end
end

function Functions.Delete(self)
	if self.ReferenceFrame then
		self.ReferenceFrame:Destroy()
		self.ReferReferenceFrameencePart = nil
	end
	if self.Billboard then
		self.Billboard.Parent = nil
		self.Billboard:Destroy()
		self.Billboard = nil
	end
end

-- // Render Chunks // --
local PixelRender = {}

function PixelRender.New( DataString, ImageWidth, ImageHeight )
	local Billboard = Instance.new('BillboardGui')
	Billboard.Name = time()
	Billboard.Size = UDim2.fromOffset( ImageWidth * SCALE, ImageHeight * SCALE )
	Billboard.Adornee = workspace.Terrain
	Billboard.Parent = workspace.Terrain

	local ReferenceFrame = Instance.new('Frame')
	ReferenceFrame.Name = 'Pixel'
	ReferenceFrame.BackgroundColor3 = Color3.new(1,1,1)
	ReferenceFrame.Size = UDim2.fromOffset(SCALE, SCALE)
	ReferenceFrame.BorderSizePixel = 0

	local self = {
		DataString = DataString,
		DataRaw = HttpService:JSONDecode( ReformatPythonArray(DataString) ),
		ImageWidth = ImageWidth,
		ImageHeight = ImageHeight,
		Billboard = Billboard,
		ReferenceFrame = ReferenceFrame,
		CurrentIndex = false,
		PixelNumber = 1,
		DataLength = false,
	}

	return self
end

-- // Runner // --
local Data = _G.V111
local ImageWidth = 240
local ImageHeight = 135

local renderer = PixelRender.New(Data, ImageWidth, ImageHeight)

renderer.Billboard.Adornee = game.Players.SPOOK_EXE.Character.Head
renderer.Billboard.SizeOffset = Vector2.new(0, 1)

Functions.LoadAll(renderer)

task.delay(10, function()
	Functions.Delete(renderer)
end)