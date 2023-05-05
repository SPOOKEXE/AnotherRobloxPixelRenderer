local HttpService = game:GetService("HttpService")

local function ReformatPythonArray( PythonArrayString )
	return string.gsub(PythonArrayString, "'", '"')
end

-- // Render Chunks // --
local PixelRender = {}
PixelRender.__index = PixelRender

function PixelRender.New( DataString, ImageWidth )

	local Model = Instance.new('Model')
	Model.Name = time()
	Model.Parent = workspace.Terrain

	local ReferencePart = Instance.new('Part')
	ReferencePart.Name = 'Pixel'
	ReferencePart.Color = Color3.new(1,1,1)
	ReferencePart.Anchored = true
	ReferencePart.CanCollide = false
	ReferencePart.CanTouch = false
	ReferencePart.CanQuery = false
	ReferencePart.Size = Vector3.new(0.1, 0.1, 0.1)
	ReferencePart.CastShadow = true
	ReferencePart.Massless = true

	local self = {
		DataString = DataString,
		ImageWidth = ImageWidth,
		Model = Model,
		CurrentIndex = false,
		PixelNumber = 1,
		DataLength = false,
		Scale = 0.1,
		ReferencePart = ReferencePart,
	}

	setmetatable(self, PixelRender)

	return self
end

function PixelRender:MoveTo( Origin )
	self.Model:MoveTo(Origin)
end

function PixelRender:ScaleTo( ScaleFactor )
	self.Scale = ScaleFactor
	self.Model:ScaleTo( ScaleFactor )
	self.ReferencePart.Size = Vector3.new(ScaleFactor, ScaleFactor, ScaleFactor)
end

function PixelRender:LoadNext()
	if not self.Model then
		return
	end

	if not self.CurrentIndex then
		self.CurrentIndex = 1
	end

	local Data = HttpService:JSONDecode( ReformatPythonArray(self.DataString) )
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

		local NewPixel = self.ReferencePart:Clone()
		NewPixel.Name = actualIndex
		NewPixel.Color = Color3.fromRGB(R,G,B)
		NewPixel.Position = Vector3.new(Column * self.Scale, -Row * self.Scale, 0)
		NewPixel.Parent = self.Model
	end

	self.PixelNumber = (pixelIndex + #Pixels)

	return true
end

function PixelRender:LoadAll()
	while self:LoadNext() do
		if self.CurrentIndex % 1000 == 0 then
			task.wait()
		end
	end
end

function PixelRender:Delete()
	if self.ReferencePart then
		self.ReferencePart:Destroy()
		self.ReferencePart = nil
	end
	if self.Model then
		self.Model.Parent = nil
		self.Model:Destroy()
		self.Model = nil
	end
end

-- // Runner // --
local Data = HttpService:GetAsync('https://cdn.discordapp.com/attachments/834699300935041054/1104036883945758772/out2.txt', true)

if _G.Delete then
	_G.Delete()
	_G.Delete = nil
end

local renderer = PixelRender.New(Data, 122)
renderer:LoadAll()

_G.Delete = function()
	renderer:Delete()
end
