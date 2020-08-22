#!/usr/bin/python3

from PIL import Image

png = Image.open("romandesignco1.png")
png.load() # required for png.split()

background = Image.new("RGB", png.size, (255, 255, 255))
background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

background.save('foo-test3.jpg', 'JPEG', quality=80)