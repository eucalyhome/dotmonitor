#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter, ImageChops, ImageColor, ImageTk, ImageDraw
import time, re, copy, os, codecs, random, datetime, json
import tkinter
import threading

class statusworker(object):
    fontreg = 0
    fontbold = 0
    statusdata = ["LOADING: loading"]
    statusdict = dict()
    imagecanvas = 0
    imagespeed = []
    imagelength = []
    imagebgbright = []
    imagebgcolor = 0

    def imagenew(self):
        imagecolorspace = 'RGB'
        imagecolorfill = (0, 0, 80)
        imagesizex = 128
        imagesizey = 64
        image = Image.new(imagecolorspace, (imagesizex, imagesizey), imagecolorfill)
        return (image)

    def statusinit(self,basedir):
        fontdata = basedir + "PixelMplus10-Regular.ttf"
        self.fontreg = ImageFont.truetype(fontdata, 10)
        fontdata = basedir + "PixelMplus10-Bold.ttf"
        self.fontbold = ImageFont.truetype(fontdata, 10)
        self.imagecanvas = Image.new("RGB", (1024, 64), (0,0,0))
        for i in range(0,8):
            self.imagespeed.append(1)
            self.imagelength.append(0)
            self.imagebgbright.append(0)

    def statusdraw(self):
        draw = ImageDraw.Draw(self.imagecanvas)
        imagetemp = Image.new("RGB", (1024, 9), (0,0,0))
        imagebg = Image.new("RGB", (128, 64), (0,0,0))
        drawbg = ImageDraw.Draw(imagebg)
        rnd = random.uniform(0,10)
        if rnd > 9.9:
            self.imagebgcolor = int(random.uniform(0,8))
        for row in range(0,7):
            if self.imagelength[row] < 128:
                rnd = int (random.uniform(0,len(self.statusdata)))
                drawtextarray = self.statusdata[rnd].split(':')
#                drawtextarray[1] = ":" + drawtextarray[1]
                drawlengthb = draw.textsize(drawtextarray[0], font=self.fontbold)
                drawlengthr = draw.textsize(drawtextarray[1], font=self.fontreg)
                drawxpos = self.imagelength[row] + 9
                drawypos = row * 9
                draw.text((drawxpos,drawypos), drawtextarray[0], (255, 255, 255),font=self.fontbold)
                drawxpos = drawxpos + drawlengthb[0]
                draw.text((drawxpos,drawypos), drawtextarray[1], (255, 255, 255),font=self.fontreg)
                self.imagelength[row] = self.imagelength[row] + drawlengthb[0] + drawlengthr[0] + 9
                self.imagebgbright[row] = 16
                rnd = int(random.uniform(0,8))
                self.imagespeed[row] = self.imagespeed[row] - 4 + rnd
                if self.imagespeed[row] < 1:
                    self.imagespeed[row] = 1
                if self.imagespeed[row] > 6:
                    self.imagespeed[row] = 6
            drawypos = row * 9 * (-1)
            imagetemp.paste(self.imagecanvas,(0,drawypos))
            drawxpos = self.imagespeed[row] * (-1)
            drawypos = row * 9
            self.imagecanvas.paste(imagetemp,(drawxpos,drawypos))
            self.imagelength[row] = self.imagelength[row] - self.imagespeed[row]
            drawbgystart = row * 9
            drawbgyend = drawbgystart + 9
            drawbright = self.imagebgbright[row] * 4
            drawbright = drawbright + 192
            if drawbright > 255:
                drawbright = 255
            drawcolor = (80,80,80)
            if self.imagebgcolor > 6:
                drawcolor = (drawbright,drawbright,drawbright)
            elif self.imagebgcolor > 5:
                drawcolor = (0,drawbright,drawbright)
            elif self.imagebgcolor > 4:
                drawcolor = (drawbright,0,drawbright)
            elif self.imagebgcolor > 3:
                drawcolor = (drawbright,drawbright,0)
            elif self.imagebgcolor > 2:
                drawcolor = (0,0,drawbright)
            elif self.imagebgcolor > 1:
                drawcolor = (0,drawbright,0)
            else:
                drawcolor = (drawbright,0,0)
            self.imagebgbright[row] = self.imagebgbright[row] - 1
            if self.imagebgbright[row] < 0:
                self.imagebgbright[row] = 0
            drawbg.rectangle((0, drawbgystart, 128, drawbgyend), fill=drawcolor)
        drawbg.rectangle((0, 63, 128, 64), fill=(0,0,0))
        image = ImageChops.darker(imagebg, self.imagecanvas)
        return (image)

    def statusload(self,target):
        if not os.path.exists(target):
            return
        try:
            with open(target, encoding='utf-8') as f:
                jsondata = json.load(f)
        except:
            return
        for rootstatus in jsondata['Children'][0]['Children']:
            for rawstatus1 in rootstatus['Children']:
                if len(rawstatus1['Children']) > 0:
                    for rawstatus2 in rawstatus1['Children']:
                        if len(rawstatus2['Children']) > 0:
                            for rawstatus3 in rawstatus2['Children']:
                                self.statusstore(rawstatus3['Text'],rawstatus3['Value'])
                        else:
                            self.statusstore(rawstatus2['Text'],rawstatus2['Value'])
                else:
                    self.statusstore(rawstatus1['Text'],rawstatus1['Value'])
        self.statusdata = []
        for title, value in self.statusdict.items():
            self.statusdata.append(title + ": " + value)

    def statusstore(self,title,value):
        if value.startswith('0.0 '):
            return
        self.statusdict[title] = value

def guiinit():
    global item, canvas, img
    root = tkinter.Tk()
    root.title('test')
    root.geometry("128x64")
    img = Image.new("RGB", (128, 64), (0,0,0))
    img = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(bg = "black", width=128, height=64)
    canvas.place(x=0, y=0)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    root.mainloop()

def main():
    basedir = "./"
    statusfile = "data.json"
    thread1 = threading.Thread(target=guiinit)
    thread1.setDaemon(True)
    thread1.start()
    time.sleep(1)

    stw = statusworker()
    image = stw.imagenew()
    stw.statusinit(basedir)

    while True:
        stw.statusload(statusfile)
        image = stw.statusdraw()

        imageoutput = ImageTk.PhotoImage(image)
        canvas.itemconfig(item,image=imageoutput,anchor=tkinter.NW)
        time.sleep(0.05)

if __name__ == '__main__':
    main()
