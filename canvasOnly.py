from tkinter import *
from tkinter import ttk

from mergeShape import MERGE

root = Tk()
root.geometry("800x600")


frameMain = Frame(root, bg = "white")
frameMain.pack(expand=True, fill="both")

canvasMain = Canvas(frameMain)
canvasMain.pack(expand=True, fill="both")

scrolY = Scrollbar(canvasMain, orient=VERTICAL)
scrolY.config(command=canvasMain.yview)
scrolY.pack(expand=False, fill="y", side=RIGHT)

scrolX = Scrollbar(canvasMain, orient=HORIZONTAL)
scrolX.config(command=canvasMain.xview)
scrolX.pack(expand=False, fill="x", side=BOTTOM)
canvasMain.config(xscrollcommand=scrolX.set, yscrollcommand=scrolY.set)


axisX = canvasMain.create_line(-10000,0,10000,0)
axisY = canvasMain.create_line(0,-10000,0,10000)

rect1Points = [226.0, 176.0, 526.0, 176.0, 526.0, 426.0, 226.0, 426.0]
rect1 = canvasMain.create_polygon(rect1Points, fill="blue")
canvasMain.tag_bind(rect1, "<Button1-Motion>", lambda eve = rect1 : objectClickedRectangle(eve=eve, obj=rect1))

rect2Points = [501.0, 398.0, 601.0, 300.0, 601.0, 448.0, 501.0, 448.0]
rect2 = canvasMain.create_polygon(rect2Points, fill="yellow")
canvasMain.tag_bind(rect2, "<Button1-Motion>", lambda eve = rect2 : objectClickedRectangle(eve=eve, obj=rect2))

pointList = [
    (0, 100),
    (100, -20),
    (120, 60),
    (40, 60),
    (40, 20),
]
polg1 = canvasMain.create_polygon(pointList, fill="green")
canvasMain.tag_bind(polg1, "<Button1-Motion>", lambda eve = rect2 : objectClickedRectangle(eve=eve, obj=polg1))

canvasMain.tag_bind(rect1, "<ButtonRelease-1>", lambda eve  : objectRelease(eve=eve))
canvasMain.tag_bind(rect2, "<ButtonRelease-1>", lambda eve : objectRelease(eve=eve))


canvasMain.bind("<Configure>", lambda eve: canvasMain.configure(scrollregion=canvasMain.bbox("all")))

relX, rely = 0, 0
inX , inY = 0, 0


def objectRelease(eve=None):
    global relX, rely, inX , inY, delX, delY
    print("Released")
    relX, rely = curX, curY
    inX , inY = 0, 0
    delX, delY = 0, 0

    print(relX, rely, "\n", inX , inY, "\n", delX, delY)




def findBoundingBox(pointList):
    xList = []
    yList = []
    for (x,y) in pointList:
        xList.append(x)
        yList.append(y)
        
    xmin = min(xList)
    xmax = max(xList)
    ymin = min(yList)
    ymax = max(yList)

    print(xmin, ymin, xmax, ymax)


def makeUnion(pointList = [], objList = []):

        mergePoints = [canvasMain.coords(rect1)+canvasMain.coords(rect2)]

        mergedShape = MERGE(mergePoints)
        newPoints = mergedShape.vertices
        cv2.imshow("MERGED", mergedShape.mainCanvas)
        print(newPoints)
    
        polgNew = canvasMain.create_polygon(newPoints, fill="Purple")

        cv2.waitKey(0)
    


def objectClickedRectangle(eve, obj):
    global curX, curY, relX, rely, inX , inY, delX, delY
    
    curX, curY = eve.x, eve.y

    if inX == 0 and inY == 0:
        delX, delY = 0, 0
    
    else:
        delX, delY = curX - inX, curY - inY


    # print(curX, curY, "\n", inX , inY, "\n", delX, delY)
    try :
        newCord = []
        for i, cord in enumerate(canvasMain.coords(obj)):
            if i % 2 == 0:
                newCord.append(cord+delX)
            if i % 2 == 1:
                newCord.append(cord+delY)

        # x0, y0, x1, y1 =   x0 + delX, y0 + delY, x1 + delX, y1 + delY
        canvasMain.coords(obj, newCord)
        print(newCord)
    except:
        print(canvasMain.coords(obj))


    inX , inY =  curX, curY









root.bind("<Key-p>", lambda eve : findBoundingBox(pointList))
root.bind("<Key-n>", lambda eve : makeUnion([], []))

root.mainloop()