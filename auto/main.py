
from PIL import Image
from os import path as os_path

from pydantic import FilePath

FILE_DIRECTORY = os_path.dirname(os_path.abspath(__file__))

THUMB_SIZE = (300, 225)

def ImageFileToPixelData( filepath : str ) -> tuple[tuple, list]:
	shape, data = None, None
	try:
		with Image.open(filepath) as img:
			img.convert('RGB')
			img.thumbnail( THUMB_SIZE )
			shape, data = (img.width, img.height), list(img.getdata())
			img.save( os_path.join(FILE_DIRECTORY, 'AUTO_thumb.png') )
	except:
		pass
	return shape, data

def RemoveParantheses(ref_string : str) -> str:
	return ref_string.replace("(", "").replace(")", "")

def TablifyArray(array_str : str) -> str:
	return array_str.replace("[", "{").replace("}", "}")

def GreedyFill( pixels, startIndex ) -> tuple[int, list]:
	color_value = pixels[startIndex]
	want_this_color = str(color_value)
	count = 1
	while startIndex < len(pixels) - 1:
		startIndex += 1
		value = pixels[ startIndex ]
		if str( value ) == want_this_color:
			count += 1
		else:
			break
	return count, color_value

def ADV_GreedyRobloxTableFormat( pixels ) -> str:
	new_pixels = []
	index = 1
	while index < len(pixels):
		count, fill_color = GreedyFill( pixels, index )
		fill_color = fill_color[:3]
		if count > 2:
			new_pixels.append('x'+str(count))
			new_pixels.extend(fill_color[:3])
			index += count
		else:
			new_pixels.extend(fill_color[:3])
			index += 1
	return str(new_pixels).replace(" ", "")

#FILEPATH = "C:\\Users\\Declan\\Documents\\BryanModelerOceanGuy.png"

print("Enter the filepath of the image you want to convert to pixels. ")
FILEPATH = input()
print(FilePath)

image_size, pixels = ImageFileToPixelData(FILEPATH)
print(image_size, len(pixels))

pixels = ADV_GreedyRobloxTableFormat(pixels)

with open( os_path.join(FILE_DIRECTORY, "AUTO_PixelDataLoader.lua"), "w" ) as file:
	file.write(f"""local Data = '{pixels.replace("'", '"')}'
_G.V111 = '['..Data..']'""")

with open( os_path.join(FILE_DIRECTORY, "AUTO_PartPixels.lua"), "w" ) as file:
	file.write("""local HttpService = game:GetService("HttpService")
local SCALE = 1

local function ReformatPythonArray( PythonArrayString )
	return string.gsub(PythonArrayString, "'", '"')
end

local Functions = { }

function Functions.LoadNext(self)
	if not self.Model then
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
		local Column = (actualIndex % self.ImageWidth)

		local R,G,B = unpack(pixelColor)

		local NewPixel = self.ReferencePart:Clone()
		NewPixel.Name = actualIndex
		NewPixel.Color = Color3.fromRGB(R,G,B)
		NewPixel.Position = Vector3.new(Column * SCALE, -Row * SCALE, 0)
		NewPixel.Parent = self.Model

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

-- // Render Chunks // --
local PixelRender = {}

function PixelRender.New( DataString, ImageWidth, ImageHeight )
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
		DataString = DataString,
		DataRaw = HttpService:JSONDecode( ReformatPythonArray(DataString) ),
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
local Data = _G.V111
local ImageWidth = ^&^&^&^1
local ImageHeight = ^&^&^&^2

local renderer = PixelRender.New(Data, ImageWidth, ImageHeight)

print("Start Loading Pixels")
Functions.LoadAll(renderer)
print("Loaded Pixels")

renderer.Model:PivotTo( game.Players.SPOOK_EXE.Character:GetPivot() * CFrame.new(0, ImageHeight/2, 0) )

task.delay(10, function()
	Functions.Delete(renderer)
end)""".replace("^&^&^&^1", str(image_size[0])).replace("^&^&^&^2", str(image_size[1])))
