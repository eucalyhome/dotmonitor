#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter, ImageChops, ImageColor, ImageTk, ImageDraw
import time, re, copy, os, codecs, random, datetime, json
import tkinter
import threading

class dotworker(object):
    monimagearray = []
    monanim = 0
    monarray = []
    moncountwait = 0
    bgimagearray = []
    bgimagepos = 0
    bgimagetype = 0
    bgimagenexttype = 0
    fontreg = 0
    fontbold = 0
    statusbg = 0

    def imagenew(self):
        imagecolorspace = 'RGB'
        imagecolorfill = (0, 0, 80)
        imagesizex = 64
        imagesizey = 128
        image = Image.new(imagecolorspace, (imagesizex, imagesizey), imagecolorfill)
        return (image)

    def bginit(self,basedir):
        for x in range(0,3):
            bgimagearraytemp = []
            for y in range(0,3):
                file = str(x) + "_" + str(y) + ".png"
                image = Image.open(basedir + "images/daihaikei/" + file).convert("RGBA")
                bgimagearraytemp.append(image)
            self.bgimagearray.append(bgimagearraytemp)

    def bgdraw(self,parm):
        baseimage = 0
        addimage = 1
        alpha = float( parm / 50 )
        if parm > 49:
            baseimage = 1
            addimage = 2
            alpha = float((parm - 50 ) / 50 )
        self.bgimagepos = self.bgimagepos + 1
        if self.bgimagepos > 255:
            self.bgimagetype = self.bgimagenexttype
            self.bgimagepos = 11
        if self.bgimagepos > 245:
            if self.bgimagenexttype == self.bgimagetype:
                rnd = int (random.uniform(0,2)) + 1
                if rnd == 3:
                    rnd = 1
                self.bgimagenexttype = (self.bgimagetype + rnd) % 3
            bgimagep = Image.blend(self.bgimagearray[self.bgimagetype][baseimage],self.bgimagearray[self.bgimagetype][addimage],alpha)
            bgimagen = Image.blend(self.bgimagearray[self.bgimagenexttype][baseimage],self.bgimagearray[self.bgimagenexttype][addimage],alpha)
            bgimagen.paste(bgimagen,(245,0))
            alphan = 1 - ((255 - self.bgimagepos) / 10)
            if alphan < 0:
                alphan = 0
            bgimage = Image.blend(bgimagep,bgimagen,alphan)
        else:
            bgimage = Image.blend(self.bgimagearray[self.bgimagetype][baseimage],self.bgimagearray[self.bgimagetype][addimage],alpha)
        bgimageposend = self.bgimagepos + 64
        image = bgimage.crop((self.bgimagepos,131,bgimageposend,259))
        return (image)

    def moninit(self,basedir):
        files = os.listdir(basedir + "images/picsqMobchip/4houkou/")
        for file in files:
            if not 'png' in file:
                continue
            image = Image.open(basedir + "images/picsqMobchip/4houkou/" + file).convert("RGBA")
            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    pixel = image.getpixel( (x, y) )
                    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                        image.putpixel( (x, y), (255,255,255,0) )
            monimagearraytempy = []
            for y in range(0,4):
                monimagearraytempx = []
                for x in range(0,3):
                    cropylow = y * 32
                    cropyhigh = cropylow + 32
                    cropxlow = x * 32
                    cropxhigh = cropxlow + 32
                    monimagearraytempx.append(image.crop((cropxlow,cropylow,cropxhigh,cropyhigh)))
                monimagearraytempy.append(monimagearraytempx)
            self.monimagearray.append(monimagearraytempy)

    def mondraw(self,image,parm,parm2):
        self.monanim = self.monanim + 1
        if self.monanim > 11:
            self.monanim = 0
        monanimpointer = int(self.monanim / 4)
        moncounttarget = int(parm / 10)
        monspeedtarget = int(parm2 / 20)
        if monspeedtarget < 1:
            monspeedtarget = 1
        if len(self.monarray) < moncounttarget:
            self.moncountwait = self.moncountwait + 1
            moncountrsv = moncounttarget - len(self.monarray)
            moncountscale = 64 / moncounttarget
            moncountper = ( moncountrsv / 64) * 100
            if self.moncountwait > moncountscale:
                moncountper = moncountper * self.moncountwait
            else:
                moncountper = moncountper / 5
            if random.uniform(0,100) < moncountper:
                self.moncountwait = 0
                montype = int(random.uniform(0,len(self.monimagearray)))
                if montype == len(self.monimagearray):
                    montype = 0
                mony = int(random.uniform(0,30))
                self.monarray.append([montype,monspeedtarget,1000,mony])
        newmonarray = []
        for moni in range(0,len(self.monarray)):
            if self.monarray[moni][2] == 1000:
                self.monarray[moni][2] = -32
            else:
                self.monarray[moni][2] = self.monarray[moni][2] + self.monarray[moni][1]
                if self.monarray[moni][2] > 63:
                    continue
            newmonarray.append(self.monarray[moni])
            monp = self.monarray[moni][0]
            monx = self.monarray[moni][2]
            mony = self.monarray[moni][3] + 65
            monimage = Image.new("RGBA",(64,128),(255,255,255,0))
            monimage.paste(self.monimagearray[monp][2][monanimpointer],(monx,mony))
            image = Image.alpha_composite(image,monimage)
        self.monarray = newmonarray
        return (image)

    def statusinit(self,basedir):
        fontdata = basedir + "PixelMplus10-Regular.ttf"
        self.fontreg = ImageFont.truetype(fontdata, 10)
        fontdata = basedir + "PixelMplus10-Bold.ttf"
        self.fontbold = ImageFont.truetype(fontdata, 10)
        self.statusbg = Image.new("RGBA",(64,128),(0,0,0,0))
        statusspace = Image.new("RGBA",(64,48),(0,0,0,0))
        draw = ImageDraw.Draw(statusspace)
        draw.rectangle((2,2,62,46),fill=(0,0,0,32))
        draw.text((3,3), "CPU", (255, 255, 255,128),font=self.fontbold)
        draw.text((3,25), "GPU", (255, 255, 255,128),font=self.fontbold)
        self.statusbg.paste(statusspace,(0,0))

    def statusdraw(self,image,cpufreq,cpuload,cputemp,gpuload,gputemp):
        cpufreq = int(cpufreq)
        cpufreq = str(cpufreq).rjust(4)
        cpuload = int(cpuload)
        cpuload = str(cpuload).rjust(3)
        cputemp = int(cputemp)
        cputemp = str(cputemp).rjust(2)
        gpuload = int(gpuload)
        gpuload = str(gpuload).rjust(3)
        gputemp = int(gputemp)
        gputemp = str(gputemp).rjust(2)
        statusimage = copy.copy(self.statusbg)
        draw = ImageDraw.Draw(statusimage)
        draw.text((25,4), cpufreq + " MHz", (0, 0, 0, 128),font=self.fontreg)
        draw.text((4,14), cpuload + " % " + cputemp +" C", (0, 0, 0, 128),font=self.fontreg)
        draw.text((4,36), gpuload + " % " + gputemp +" C", (0, 0, 0, 128),font=self.fontreg)
        draw.text((24,3), cpufreq + " MHz", (255, 255, 255,128),font=self.fontreg)
        draw.text((3,13), cpuload + " % " + cputemp +" C", (255, 255, 255,128),font=self.fontreg)
        draw.text((3,35), gpuload + " % " + gputemp +" C", (255, 255, 255,128),font=self.fontreg)

        image = Image.alpha_composite(image,statusimage)
        return (image)

def guiinit():
    global item, canvas, img
    root = tkinter.Tk()
    root.title('test')
    root.geometry("64x128")
    img = Image.new("RGB", (64, 128), (0,0,0))
    img = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(bg = "black", width=64, height=128)
    canvas.place(x=0, y=0)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    root.mainloop()

def main():
    basedir = "./"
    thread1 = threading.Thread(target=guiinit)
    thread1.setDaemon(True)
    thread1.start()
    time.sleep(1)

    dot = dotworker()
    image = dot.imagenew()
    dot.bginit(basedir)
    dot.moninit(basedir)
    dot.statusinit(basedir)

    while True:
        bgimage = dot.bgdraw(60)
        image = dot.mondraw(bgimage,60,60)
        image = dot.statusdraw(image,"5000","60","20","30","40")

        imageoutput = ImageTk.PhotoImage(image)
        canvas.itemconfig(item,image=imageoutput,anchor=tkinter.NW)
        time.sleep(0.05)

if __name__ == '__main__':
    main()
