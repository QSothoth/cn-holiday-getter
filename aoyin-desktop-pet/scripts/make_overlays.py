#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'app/assets/overlays'; ROOT.mkdir(parents=True,exist_ok=True)
S=4
def canvas(w,h): return Image.new('RGBA',(w*S,h*S),(0,0,0,0))
def pts(seq): return [(int(x*S),int(y*S)) for x,y in seq]
def save(im,name,size): im.resize(size,Image.Resampling.LANCZOS).save(ROOT/name,optimize=True)

# Human, earless wine-red hair crown.
w,h=360,210; im=canvas(w,h); d=ImageDraw.Draw(im)
outer=[(20,167),(37,112),(62,119),(66,57),(101,82),(119,25),(148,73),(180,10),(199,67),(235,22),(247,79),(300,49),(290,105),(336,92),(315,164),(278,184),(232,178),(186,191),(133,179),(78,188)]
d.polygon(pts(outer),fill=(35,8,25,255))
inner=[(29,164),(47,119),(72,126),(75,69),(105,91),(123,39),(150,82),(181,22),(201,78),(233,35),(244,91),(290,61),(280,116),(324,104),(305,157),(274,174),(230,168),(187,181),(135,169),(82,178)]
d.polygon(pts(inner),fill=(100,24,55,255))
for i,p in enumerate([[(42,145),(82,105),(71,169)],[(78,151),(119,98),(110,174)],[(121,153),(158,91),(151,176)],[(164,154),(198,88),(190,178)],[(207,153),(245,92),(232,174)],[(251,150),(294,103),(279,166)]]): d.polygon(pts(p),fill=(77+5*i,16+2*i,43+3*i,245))
for path in [[(83,93),(112,63),(132,48)],[(147,69),(177,42),(197,38)],[(214,71),(242,55),(267,62)]]: d.line(pts(path),fill=(184,72,107,180),width=5*S,joint='curve')
save(im.filter(ImageFilter.GaussianBlur(.25*S)),'hair-crown.png',(w,h))

# Thin rectangular glasses.
w,h=230,86; im=canvas(w,h); d=ImageDraw.Draw(im); frame=(49,39,45,248); shine=(211,173,116,120)
for box in [(8,16,101,70),(129,16,222,70)]:
    d.rounded_rectangle(tuple(int(v*S) for v in box),radius=12*S,outline=frame,width=4*S)
    d.rounded_rectangle(tuple(int(v*S) for v in (box[0]+4,box[1]+4,box[2]-4,box[3]-4)),radius=9*S,outline=(255,255,255,38),width=2*S)
d.line(pts([(101,39),(129,39)]),fill=frame,width=4*S); d.line(pts([(13,27),(2,22)]),fill=frame,width=4*S); d.line(pts([(217,27),(228,22)]),fill=frame,width=4*S)
d.line(pts([(20,25),(47,18)]),fill=shine,width=2*S); d.line(pts([(142,25),(169,18)]),fill=shine,width=2*S)
save(im,'glasses.png',(w,h))

# Sharp brows and warm amber irises stay when glasses are removed.
w,h=230,110; im=canvas(w,h); d=ImageDraw.Draw(im); brow=(58,18,39,235)
d.polygon(pts([(22,21),(88,14),(91,22),(29,31)]),fill=brow); d.polygon(pts([(139,15),(207,21),(200,30),(136,23)]),fill=brow)
for cx in (66,164):
    d.ellipse((int((cx-13)*S),int(46*S),int((cx+13)*S),int(83*S)),fill=(101,66,17,210)); d.ellipse((int((cx-7)*S),int(51*S),int((cx+7)*S),int(78*S)),fill=(48,31,12,235)); d.ellipse((int((cx-2)*S),int(52*S),int((cx+3)*S),int(59*S)),fill=(255,234,165,230))
save(im,'face-details.png',(w,h))

# Small chibi hand that follows the glasses.
w,h=72,86; im=canvas(w,h); d=ImageDraw.Draw(im)
d.rounded_rectangle((10*S,20*S,59*S,74*S),radius=22*S,fill=(239,190,164,255),outline=(72,35,39,245),width=4*S)
for x in (17,28,39,50): d.rounded_rectangle((x*S,4*S,(x+12)*S,40*S),radius=7*S,fill=(245,201,177,255),outline=(72,35,39,230),width=3*S)
d.rounded_rectangle((25*S,61*S,53*S,84*S),radius=8*S,fill=(139,39,76,255),outline=(60,24,40,230),width=3*S)
save(im,'hand.png',(w,h))

w,h=64,64; im=canvas(w,h); d=ImageDraw.Draw(im); d.polygon(pts([(32,2),(39,24),(62,32),(39,40),(32,62),(25,40),(2,32),(25,24)]),fill=(255,218,120,230)); save(im.filter(ImageFilter.GaussianBlur(.5*S)),'sparkle.png',(w,h))
