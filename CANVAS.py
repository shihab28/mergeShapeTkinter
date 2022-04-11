from ast import Return
import os
from tkinter import *
from tkinter import font, OptionMenu, ttk
from venv import create
from PIL import Image, ImageTk
import random

from mergeShape import MERGE



curDir = os.path.dirname(__file__).replace("\\", "/")
iconRelativeDir = "resources/icons"
scriptRelaltiveDir = "resources/script"

imageDict = {}

def getImage(imgSaveDir, imageSize = (24, 24)):
    imgSave =ImageTk.PhotoImage(Image.open(imgSaveDir).resize(imageSize, Image.ANTIALIAS))
    return imgSave

def loadImage(imageSize = (24, 24)):
    imageDict['dot'] = getImage(f"{curDir}/{iconRelativeDir}/dot.png", imageSize)
    imageDict['line'] = getImage(f"{curDir}/{iconRelativeDir}/line.png", imageSize)
    imageDict['circle_border'] = getImage(f"{curDir}/{iconRelativeDir}/circle_border.png", imageSize)
    imageDict['polygon_border'] = getImage(f"{curDir}/{iconRelativeDir}/polygon_border.png", imageSize)
    imageDict['rectangle_border'] = getImage(f"{curDir}/{iconRelativeDir}/rectangle_border.png", imageSize)
    imageDict['text_border'] = getImage(f"{curDir}/{iconRelativeDir}/text_border.png", imageSize)

    return imageDict









# def objectClickedRectangle(eve=None,  obj=None):
#     global toolbarMain, canvasMain, labelInfo
#     print(canvasMain.canvas, eve,  obj)


class AUTOSCROLL(ttk.Scrollbar):
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise root.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise root.TclError('Cannot use place with this widget')


class CANVAS(Canvas):

    objectAttributDict = {}
    penTypeList = [
        'select', 'dot', 'line', 'rectangle', 'polygon', 'circle', 'text', 'eraser'
    ]

    def __init__(self, frame, height = 80, width=200, bg="#D5F3FE", limit=(-10000, 10000)):
        self.height = height
        self.width = width
        self.canvasBg = bg

        self.canvasLimit = limit
        (self.limitNeg, self.limitPos) = self.canvasLimit 

        self.scale = 20
        self.minScale = 1
        self.maxScale = 20
        self.ppmmc = 1000
        self.gridResolution = 25
        self.gridType = 'd'

        self.penType = 'select'
        self.penStatus = 'select'

        self.frame = Frame(frame, bg=self.canvasBg)
        self.frame.pack(expand=True, fill="both")        

        self.centerCord = (0,0)

        self.iconHeight = 35
        self.iconWidth = self.iconHeight
        self.toolBg = bg
        self.toolFg = "Black"
        self.colorActivateBg = "green"
        self.colorActivateFg = "White"
        self.imageDict = loadImage(imageSize=(self.iconWidth, self.iconHeight))
        self.createToolButton()

        self.selectedObject = 'canvas'

        self.selectedObjectList = []

        self.lineWidth = 1
        self.resolution = 5

        self.objectRelease()
        self.initCanvas()

    
    def createToolButton(self):

        self.toolButtonList = []

        self.toolFrame = Frame(self.frame, bg=self.canvasBg)
        self.toolFrame.pack(expand=False) 

        try:
            for wid in self.toolFrame.winfo_children():
                del(wid)
        except:
            pass
        

        i = 0
        self.buttonDot = Button(self.toolFrame, image=self.imageDict['dot'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonDot.pack(expand=True, fill="both", side=LEFT)

        i += 1
        self.buttonLine = Button(self.toolFrame, image=self.imageDict['line'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonLine.pack(expand=True, fill="both", side=LEFT)

        i += 1
        self.buttonRect = Button(self.toolFrame, image=self.imageDict['rectangle_border'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonRect.pack(expand=True, fill="both", side=LEFT)

        i += 1
        self.buttonPolg = Button(self.toolFrame, image=self.imageDict['polygon_border'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonPolg.pack(expand=True, fill="both", side=LEFT)

        i += 1
        self.buttonCrcl = Button(self.toolFrame, image=self.imageDict['circle_border'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonCrcl.pack(expand=True, fill="both", side=LEFT)

        i += 1
        self.buttonText = Button(self.toolFrame, image=self.imageDict['text_border'], bg=self.toolBg, fg=self.toolFg, highlightbackground=self.toolBg, highlightcolor=self.toolBg,\
             border=0, borderwidth=0, highlightthickness=0, command= lambda i = i: self.toolButtonCLicked(i))
        self.buttonText.pack(expand=True, fill="both", side=LEFT)

        self.toolButtonList = [self.buttonDot, self.buttonLine, self.buttonRect, self.buttonPolg, self.buttonCrcl, self.buttonText]
        self.toolButtonCommand = [self.createDot, self.createLine, self.createRect, self.createPolg, self.createCrcl, self.createText]
        # self.drawShapeCommand = [self.createDot, self.createLine, self.createRect, self.createPolg, self.createCrcl, self.createText]
        self.toolButtonCommandStatus = [False, False, False, False, False, False]


    # penTypeList = [
    #     'select', 'dot', 'line', 'rectangle', 'polygon', 'oval', 'text', 'eraser'
    # ]

    def createShape(self, eve=None):
        if eve != None:
            x, y = eve.x, eve.y
            # print(x, y)

            if self.penStatus == 'clicked' and self.prevClickCord != (None, None):
                
                if self.penType == CANVAS.penTypeList[2]:
                    self.currentClickCord = x, y
                    newObj = self.drawLine((self.prevClickCord + self.currentClickCord))
                    self.penStatus = CANVAS.penTypeList[0]
                    self.prevClickCord = self.currentClickCord

                elif self.penType == CANVAS.penTypeList[3]:
                    self.currentClickCord = x, y
                    newObj = self.drawRectangle((self.prevClickCord + self.currentClickCord), fill="Blue")
                    self.penStatus = CANVAS.penTypeList[0]
                    self.prevClickCord = self.currentClickCord
                
                elif self.penType == CANVAS.penTypeList[4]:
                    self.currentClickCord = x, y
                    # print((self.prevClickCord, self.currentClickCord))
                    
                    newObj = self.drawPolygon((self.prevClickCord + self.currentClickCord), fill="Yellow")
                    self.penStatus = CANVAS.penTypeList[0]
                    self.prevClickCord = self.currentClickCord

                elif self.penType == CANVAS.penTypeList[5]:
                    self.currentClickCord = x, y

                    (x0, y0) = self.prevClickCord
                    (x1, y1) = self.currentClickCord

                    r = int((abs(x1 - x0)**2 + abs(y1 - y0)**2)**.5)
                    newObj = self.drawOval((x0 - r, y0 - r, x0 + r, y0 + r), fill="Green")
                    # newObj.bind("<Button-1>", lambda eve = self : print(newObj))
                    self.penStatus = CANVAS.penTypeList[0]
                    self.prevClickCord = self.currentClickCord

                elif self.penType == CANVAS.penTypeList[6]:
                    self.currentClickCord = x, y
                    newObj = self.drawText((self.prevClickCord + self.currentClickCord), fill="Blue")
                    self.penStatus = CANVAS.penTypeList[0]
                    self.prevClickCord = self.currentClickCord

                    self.selectedObject = 'canvas'

                self.prevClickCord = None, None

            else:
                if self.penType != CANVAS.penTypeList[0] and self.penType == CANVAS.penTypeList[1]:
                    self.drawDot((x, y))
                    self.penStatus = 'select'
                    self.prevClickCord = x, y 

                elif self.penType != CANVAS.penTypeList[0]:
                    self.penStatus = 'clicked'
                    self.prevClickCord = x, y 
                
                else:
                    
                    self.prevClickCord = None, None

    def toolButtonCLicked(self, i):
        self.deHighLightButton()
        if self.toolButtonCommandStatus[i] == False:
            self.toolButtonList[i]['bg'] = self.colorActivateBg
            self.toolButtonList[i]['fg'] = self.colorActivateFg
            self.toolButtonCommandStatus[i] = True
            comReturn = self.toolButtonCommand[i]()

        else:
            self.toolButtonCommandStatus[i] = False


    def deHighLightButton(self):

        for butt in self.toolButtonList:
            butt['bg'] = self.toolBg
            butt['fg'] = self.toolFg

        allObjectList = self.canvas.find_all()
        print(allObjectList)

        for obj in allObjectList:
            try:
                self.canvas.itemconfigure(obj, bd=0)
            except:
                pass


        self.clearSelection()
        self.penStatus = 'select'
        self.prevClickCord = None, None



    def initCanvas(self):
        
        self.canvas = Canvas(self.frame, bg=self.canvasBg, highlightbackground=self.canvasBg, highlightcolor=self.canvasBg, border=0, borderwidth=0, highlightthickness=0)
        
        self.scrollCanvasY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollCanvasY.pack(expand=False, fill="y", side=RIGHT)
        self.scrollCanvasY.config(command=self.canvas.yview)

        self.scrollCanvasX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollCanvasX.pack(expand=False, fill="x", side=BOTTOM)
        self.scrollCanvasX.config(command=self.canvas.xview)

        self.canvas.pack(expand=True, fill="both", anchor=CENTER)
        self.canvas.config(xscrollcommand=self.scrollCanvasX.set, yscrollcommand=self.scrollCanvasY.set) 

        self.canvas.bind("<Button-1>", lambda eve = self : self.createShape(eve=eve))
        self.canvas.bind("<Configure>", lambda eve : self.canvas.configure(scrollregion= self.canvas.bbox("all")))

        self.updateCenter()
        self.updateAxis()
        # self.updateGrid()

        # self.canvas.bind("<Motion>", lambda eve = self : self.updateCenter())

    def updateCenter(self):   
        self.canvWidth = self.canvas.winfo_width()
        self.canvHeight = self.canvas.winfo_height()
        self.centerCord = (self.canvWidth//2, self.canvHeight//2)
        (self.centerX, self.centerY) =  self.centerCord
        # self.updateAxis()


    def updateAxis(self):
        try:
            self.canvas.delete(self.xAxis)
            self.canvas.delete(self.yAxis)
        except:
            pass

        self.xAxis = self.drawLine((self.limitNeg, self.centerY, self.limitPos, self.centerY))
        self.yAxis = self.drawLine((self.centerX, self.limitNeg, self.centerX, self.limitPos))

    def makeUnion(self):
        mergePoints = []
        if self.selectedObjectList != []:
            for obj in self.selectedObjectList:
                mergePoints.append(self.canvas.coords(obj))
           
            mergedShape = MERGE(mergePoints)
            newPoints = mergedShape.vertices
            print(newPoints)

            for obj in self.selectedObjectList:
                self.canvas.delete(obj) 

            newObj = self.drawPolygon(newPoints, fill="Purple")
            self.selectedObjectList = []
            root.update()


    def objectRelease(self, eve=None):
        print("Released")
        self.relX, self.rely = 0, 0
        self.inX , self.inY = 0, 0
        self.delX, self.delY = 0, 0  
        
                
                
    def objectClickedRectangle(self, eve=None,  obj=None, delx=None, dely=None):
      
        if obj != None:

            if delx == None or dely == None and eve != None:
                self.curX,  self.curY = eve.x, eve.y
                if  self.inX == 0 and  self.inY == 0:
                    self.delX,  self.delY = 0, 0
                
                else:
                    self.delX, self.delY = self.curX - self.inX, self.curY - self.inY
                    delx, dely= self.delX,  self.delY

            elif delx != None and dely != None:

                try :
                    newCord = []
                    for i, cord in enumerate(self.canvas.coords(obj)):
                        if i % 2 == 0:
                            newCord.append(cord+delx)
                        if i % 2 == 1:
                            newCord.append(cord+dely)

                    self.canvas.coords(obj, newCord)
                    # print(newCord)
                except:
                    self.canvas.coords(obj, self.canvas.coords(obj))

                self.inX , self.inY =  delx, dely

    def controlClicked(self, eve=None,  obj=None):
        self.objectRelease()
        self.deHighLightButton()
        
        if obj not in self.selectedObjectList:
            self.selectedObjectList.append(obj)
        
        
        print("self.controlClicked", self.selectedObjectList)
        
    def objectClicked(self, eve=None,  obj=None):
        self.objectRelease()
        self.deHighLightButton()
        self.selectedObjectList = []
        self.controlClicked(eve, obj)
        # print("self.objectClicked", self.selectedObjectList)

    def deleteObject(self):
        for obj in self.selectedObjectList:
            try:
                self.canvas.delete(obj)
            except:
                pass


    def clearSelection(self):
        print("clearSelection")
        self.penType = 'select'
        pass

    def createDot(self):
        print("createDot")
        self.penType = 'dot'
        
        pass

    def createLine(self):
        print("createLine")
        self.penType = 'line'

    def createRect(self):
        print("createRect")
        self.penType = 'rectangle'
        pass

    def createPolg(self):
        print("createPolg")
        self.penType = 'polygon'
        pass

    def createCrcl(self):
        print("createCrcl")
        self.penType = 'circle'
        pass

    def createText(self):
        print("createText")
        self.penType = 'text'
        pass

    def makeAngularPooints(self, cord):
        r = (self.lineWidth / 2) / (2 ** .5)
        (x0, y0, x1, y1) = cord

        if ( int(x0 -x1) * int(y0 - y1)) >= 0:
            pointList = [x0-r, y0+r, x0+r, y0-r, x1+r, y1-r, x1-r, y1+r]
        
        else:
            pointList =  [x0-r, y0-r, x0+r, y0+r, x1+r, y1+r, x1-r, y1-r]


        return pointList

    def moveObject(self, key=None):

        if self.selectedObjectList != []:
            if len(self.selectedObjectList) == 1:
                if key == 'Up':
                    self.objectClickedRectangle(eve=None, obj= self.selectedObjectList[0], delx=0, dely= -self.resolution)
                elif key == 'Down':
                    self.objectClickedRectangle(eve=None, obj= self.selectedObjectList[0], delx=0, dely= self.resolution)
                elif key == 'Left':
                    self.objectClickedRectangle(eve=None, obj= self.selectedObjectList[0], delx=-self.resolution, dely= 0)
                elif key == 'Right':
                    self.objectClickedRectangle(eve=None, obj= self.selectedObjectList[0], delx= self.resolution, dely=0)


    def drawDot(self, cord, *args, **kwargs):
        (x0, y0) = cord
        obj = self.canvas.create_oval(x0, y0, x0, y0, *args, **kwargs)
        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        return obj
    
    def drawLine(self, cord, *args, **kwargs):
        
        if self.lineWidth > 1:
            recCord = self.makeAngularPooints(cord)
            obj = self.canvas.create_polygon(recCord, *args, **kwargs)
        
        else:
            obj = self.canvas.create_line(cord, *args, **kwargs)

        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Button-1>", lambda  eve = obj : self.objectClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Control-1>", lambda  eve = obj : self.controlClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        

        return obj

    def drawRectangle(self, cord, *args, **kwargs):
        (x0, y0, x1, y1) = cord
        recCord = [x0, y0, x1, y0, x1, y1, x0, y1]

        obj = self.canvas.create_polygon(recCord, *args, **kwargs)
        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Button-1>", lambda  eve = obj : self.objectClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Control-1>", lambda  eve = obj : self.controlClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        
        return obj

    def drawOval(self, cord, *args, **kwargs):
        (x0, y0, x1, y1) = cord
        obj =  self.canvas.create_oval(x0, y0, x1, y1, *args, **kwargs)
        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Button-1>", lambda  eve = obj : self.objectClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Control-1>", lambda  eve = obj : self.controlClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        
        return obj

    def drawPolygon(self, cord, *args, **kwargs):
        obj = self.canvas.create_polygon(cord, *args, **kwargs)
        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Button-1>", lambda  eve = obj : self.objectClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Control-1>", lambda  eve = obj : self.controlClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        

        return obj

    def drawText(self, cord, *args, **kwargs):
        (x0, y0) = cord
        obj =  self.canvas.create_text(x0, y0, *args, **kwargs)
        self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve = obj : self.objectClickedRectangle(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Button-1>", lambda  eve = obj : self.objectClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<Control-1>", lambda  eve = obj : self.controlClicked(eve=eve, obj=obj))
        self.canvas.tag_bind(obj, "<ButtonRelease-1>", lambda eve  : self.objectRelease(eve=eve))
        return obj

    def drawArc(self, cord, *args, **kwargs):
        (x0, y0, x1, y1) = cord
        obj =  self.canvas.create_arc(x0, y0, x1, y1, *args, **kwargs)
        # self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve : self.objectClickedRectangle(eve=eve))
        return obj
    
    def drawImage(self, cord, *args, **kwargs):
        (x0, y0) = cord
        obj =  self.canvas.create_image(x0, y0, *args, **kwargs)
        # self.canvas.tag_bind(obj, "<Button1-Motion>", lambda  eve : self.objectClickedRectangle(eve=eve))
        return obj

    

    def updateToolbarSize(self, currentWindowSize = (100, 100)):
        (self.iconWidth, self.iconHeight) = currentWindowSize

        self.iconWidth = self.iconWidth // 20
        self.iconHeight = self.iconHeight // 20

        self.imageDict = loadImage(imageSize=(self.iconWidth, self.iconHeight))
        self.createToolButton()



class TOOLBAR(CANVAS):   
    def __init__(self, frame, bg="#D5F3FE", height=40):
        self.toolBg = bg
        self.canvasHeight = height

    
        self.frame = Frame(frame, bg=self.toolBg)
        self.frame.pack(expand=False)          
            

def updateWindowSize(eve=None):
    global toolbarMain, canvasMain, labelInfo
    canvasMain.updateCenter()
    canvasSize = (canvasMain.canvWidth, canvasMain.canvHeight)
    scrolSizeX = canvasMain.canvas['scrollregion']
    labelInfo['text'] = f"Canvas Size : {canvasSize},  {scrolSizeX}"
    # toolbarMain.updateToolbarSize(currentWindowSize=canvasSize)
    

def clearSelection(eve=None):
    global toolbarMain, canvasMain, labelInfo
    canvasMain.clearSelection()
    canvasMain.selectedObjectList = []
    canvasMain.deHighLightButton()

def mergeShapes(eve=None):
    global toolbarMain, canvasMain, labelInfo
    print("merging")
    canvasMain.makeUnion()


def deleteShapes(eve=None):
    global toolbarMain, canvasMain, labelInfo
    canvasMain.deleteObject()
    clearSelection()
    

def keyPressed(eve=None):
    global canvasMain
    key = eve.keysym

    if key == 'Up' or key == 'Down' or key == 'Left' or key == 'Right':
        canvasMain.moveObject(key)







if __name__ == "__main__":
    global toolbarMain, canvasMain, labelInfo
    

    root = Tk()
    root.title("VLSI DRAW")


    mainBg = "White"
    frame_main = Frame(root, bg=mainBg, highlightbackground=mainBg, highlightcolor=mainBg, border=0, borderwidth=0, highlightthickness=0)
    frame_main.pack(expand=True, fill="both")

    # toolbarMain = TOOLBAR(frame=frame_main)
    canvasMain = CANVAS(frame=frame_main)

    root.bind("<Motion>", updateWindowSize)
    root.bind("<Configure>", updateWindowSize)
    root.bind("<Escape>", clearSelection)
    root.bind("<Control-Key-m>", mergeShapes)
    root.bind("<Delete>", deleteShapes)
    root.bind('<Key>', keyPressed)

    infoFrame = Frame(frame_main)
    infoFrame.pack(expand=False, fill="x")
    labelInfo = Label(infoFrame)
    labelInfo.pack(expand=False, fill="x")



    root.mainloop()
        


