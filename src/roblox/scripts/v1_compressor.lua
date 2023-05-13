
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

-- // // --

local SCALE = 0.1

local Functions = { }

function Functions.LoadNext(self)
	if not self.Model then
		return
	end

	if not self.CurrentIndex then
		self.CurrentIndex = 1
	end

	if not self.DataLength then
		self.DataLength = #self.Pixels
	end

	if self.CurrentIndex >= self.DataLength then
		return false
	end

	local Pixels = { }

	local value = self.Pixels[self.CurrentIndex]
	if string.find(value, 'x') then
		local R, G, B = self.Pixels[self.CurrentIndex+1], self.Pixels[self.CurrentIndex+2], self.Pixels[self.CurrentIndex+3]
		local repetitions = tonumber(string.sub(value, 2, #value))
		for _ = 1, repetitions do
			table.insert(Pixels, {R, G, B})
		end
		self.CurrentIndex += 4
	else
		local R, G, B = self.Pixels[self.CurrentIndex], self.Pixels[self.CurrentIndex+1], self.Pixels[self.CurrentIndex+2]
		table.insert(Pixels, {R, G, B})
		self.CurrentIndex += 3
	end

	local pixelIndex = self.PixelNumber

	local PixelGroup = Instance.new('Model')
	PixelGroup.Name = 'PixelGroup_'..pixelIndex

	for index, pixelColor in ipairs(Pixels) do
		local actualIndex = (self.PixelNumber + index)
		local Row = math.floor(actualIndex / self.ImageWidth)
		local Column = (actualIndex % self.ImageWidth)

		local R,G,B = unpack(pixelColor)

		local NewPixel = self.ReferencePart:Clone()
		NewPixel.Name = actualIndex
		NewPixel.Color = Color3.fromRGB(R,G,B)
		NewPixel.Position = Vector3.new(Column * SCALE, -Row * SCALE, 0)
		NewPixel.Parent = PixelGroup

		if index % 3000 == 0 then
			task.wait()
		end
	end

	PixelGroup.Parent = self.Model

	self.PixelNumber = (pixelIndex + #Pixels)

	return true
end

function Functions.LoadAll(self)
	local Counter = 0
	while Functions.LoadNext(self) do
		if Counter % 750 == 0 then
			Counter = 0
			task.wait()
		end
		Counter += 1
	end
end

function Functions.Delete(self)
	if self.ReferencePart then
		self.ReferencePart:Destroy()
		self.ReferencePart = nil
	end
	if self.Model then
		self.Model:ClearAllChildren()
		self.Model:Destroy()
		self.Model = nil
	end
end

-- // Render Chunks // --
local PixelRender = {}

function PixelRender.New( Pixels, ImageWidth, ImageHeight )
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

	local self = {
		Pixels = Pixels,
		ImageWidth = ImageWidth,
		ImageHeight = ImageHeight,
		Model = Model,
		ReferencePart = ReferencePart,
		CurrentIndex = false,
		PixelNumber = 1,
		DataLength = false,
	}

	return self
end

-- // Runner // --
local ImageWidth = Shape[1]
local ImageHeight = Shape[2]

local renderer = PixelRender.New(RawPixels, ImageWidth, ImageHeight)

local GoalCFrame = game.Players.SPOOK_EXE.Character:GetPivot() * CFrame.new((-ImageWidth/2) * SCALE, (ImageHeight/2) * SCALE, 0)

local Att = Instance.new('Attachment')
Att.Visible = true
Att.WorldCFrame = GoalCFrame
Att.Parent = workspace.Terrain

print("Start Loading Pixels - ", #RawPixels)
local s, e = pcall(Functions.LoadAll, renderer)
print("Loaded Pixels")

if s then
	local CurrentOriginCF = renderer.Model:GetPivot()
	for i, Model in ipairs( renderer.Model:GetChildren() ) do
		local ModelOriginOffset = Model:GetPivot():ToObjectSpace( CurrentOriginCF )
		Model:PivotTo( GoalCFrame * ModelOriginOffset )
		if i % 200 == 0 then
			task.wait()
		end
	end
else
	warn(e)
end

task.delay(10, function()
	Att:Destroy()
	Functions.Delete(renderer)
end)