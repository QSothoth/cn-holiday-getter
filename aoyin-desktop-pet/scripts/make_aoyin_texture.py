#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'app/assets/model/aoyin/_upstream-texture.png'; OUT=ROOT/'app/assets/model/aoyin/texture_00.png'
a=np.array(Image.open(SRC).convert('RGBA')).copy(); mask=a[:,:,3]>10
lab,_=ndimage.label(mask); objs=ndimage.find_objects(lab); components={}; idx=0
for i,s in enumerate(objs,1):
    if s is None: continue
    local=(lab[s]==i); area=int(local.sum())
    if area<100: continue
    idx+=1; full=np.zeros(mask.shape,bool); full[s]=local; components[idx]=(full,s)

def recolor(ids,dark,light,alpha_fill=False):
    dark=np.array(dark,float); light=np.array(light,float); rgb=a[:,:,:3].astype(float)
    lum=(rgb[:,:,0]*.2126+rgb[:,:,1]*.7152+rgb[:,:,2]*.0722)/255.; t=np.clip((lum-.08)/.84,0,1)[...,None]
    col=dark+(light-dark)*(t**.75)
    for cid in ids:
        if cid not in components: continue
        m,_=components[cid]; a[m,:3]=np.clip(col[m],0,255).astype(np.uint8)
        if alpha_fill: a[m,3]=255

def transparent(ids):
    for cid in ids:
        if cid in components: a[components[cid][0],3]=0

transparent([51,52,58])
hair=[2,4,6,7,10,12,26]; recolor(hair,(42,7,27),(181,65,101))
ygrid,xgrid=np.indices(mask.shape)
for cid in hair:
    if cid not in components: continue
    m,_=components[cid]; hi=m & (((xgrid+2*ygrid+cid*17)%95)<6) & (a[:,:,3]>80)
    a[hi,:3]=np.clip(a[hi,:3].astype(int)+np.array([22,8,13]),0,255)
recolor([22,23,25,29,33,34,35,36,37,44,45,47],(18,8,14),(62,22,39),True)
recolor([1,46,53,59],(72,16,39),(181,61,96),True)
transparent([3,57,60,61,62,63,64,65,66,67])
for cid in [1,46,53,59]:
    if cid not in components: continue
    m,_=components[cid]; rr=m & ((((xgrid%22)<2)|(((xgrid+11)%44)<1))) & (a[:,:,3]>64)
    a[rr,:3]=np.clip(a[rr,:3].astype(int)-np.array([12,5,7]),0,255)
if 53 in components:
    m,_=components[53]; a[m,:3]=np.array([143,39,76],np.uint8); a[m,3]=255
recolor([9],(19,19,28),(74,70,82),True)
for cid in [54,55]:
    if cid not in components: continue
    m,s=components[cid]; y0,y1=s[0].start,s[0].stop; x0,x1=s[1].start,s[1].stop
    f=(ygrid-y0)/max(1,y1-y0); pants=m&(f<.73); shoes=m&(f>=.73)
    centre=(x0+x1)/2; shade=np.clip(1-np.abs(xgrid-centre)/max(1,(x1-x0)/2),0,1)
    col=np.stack([29+18*shade,28+17*shade,38+18*shade],2)
    a[pants,:3]=col[pants].astype(np.uint8); a[pants,3]=255
    a[shoes,:3]=np.array([235,232,236],np.uint8); a[shoes,3]=255
    a[shoes&(f>.91),:3]=np.array([47,43,51],np.uint8)
for cid in [5,8,11,13,14,15,16,20,24,27,30,31,32,49,50,56]:
    if cid not in components: continue
    m,_=components[cid]; rgb=a[m,:3].astype(float); rgb[:,0]*=.99; rgb[:,1]*=1.015; rgb[:,2]*=1.025; a[m,:3]=np.clip(rgb,0,255).astype(np.uint8)
a[a[:,:,3]==0,:3]=255
Image.fromarray(a,'RGBA').save(OUT,optimize=True)
print(OUT)
