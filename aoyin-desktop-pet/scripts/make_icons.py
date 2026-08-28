#!/usr/bin/env python3
from PIL import Image,ImageDraw
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'src-tauri/icons'; OUT.mkdir(parents=True,exist_ok=True)
S=1024; im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle((80,80,944,944),radius=220,fill=(248,236,243,255),outline=(102,28,61,255),width=36)
d.ellipse((236,250,788,802),fill=(242,199,177,255),outline=(63,26,43,255),width=28)
hair=[(210,420),(245,210),(330,260),(390,135),(470,240),(548,110),(605,240),(720,170),(700,360),(790,310),(760,470),(680,365),(590,430),(500,350),(420,430),(330,350)]
d.polygon(hair,fill=(105,25,58,255),outline=(48,10,31,255))
for box in [(270,430,470,565),(554,430,754,565)]: d.rounded_rectangle(box,radius=38,outline=(56,42,49,255),width=22)
d.line((470,494,554,494),fill=(56,42,49,255),width=22); d.arc((330,570,690,770),20,160,fill=(91,37,60,255),width=18)
for size,name in [(32,'32x32.png'),(128,'128x128.png'),(256,'128x128@2x.png')]: im.resize((size,size),Image.Resampling.LANCZOS).save(OUT/name)
im.resize((256,256),Image.Resampling.LANCZOS).save(OUT/'icon.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
im.save(OUT/'icon.icns')
