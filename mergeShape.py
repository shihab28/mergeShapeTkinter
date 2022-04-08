import cv2 as cv2
import numpy as np




class MERGE():
    def __init__(self, objectList, xpos=0, ypos=1):
        self.objectList = objectList
        self.xpos, self.ypos = xpos, ypos 

        self.padx = 1
        self.pady = 1

        self.getBoundary()
        self.makeCanvas()
        self.mergeShape()
        self.findVertices()





    def getBoundary(self):

        self.xList = []
        self.yList = []
        for obj in self.objectList:
            for ind, cord in enumerate(obj):
                if ind % 2 == self.xpos:
                    self.xList.append(cord)
                
                elif ind % 2 == self.ypos:
                    self.yList.append(cord)

        self.xMin = min(self.xList)
        self.xMax = max(self.xList)
        self.yMin = min(self.yList)
        self.yMax = max(self.yList)

        self.canvasWidth = int(abs(self.xMax - self.xMin))
        self.canvasHeight = int(abs(self.yMax - self.yMin))
        self.boundaries = [0, 0, self.canvasWidth, self.canvasHeight]


        self.objectCordList = []
        for obj in self.objectList:
            pointCordList = []
            tempXYList = []
            for ind, cord in enumerate(obj):
                if ind % 2 == self.xpos:
                   tempXYList.append(int(cord-self.xMin))
                
                elif ind % 2 == self.ypos:
                    tempXYList.append((int(cord-self.yMin)))
                    pointCordList.append(tempXYList)
                    tempXYList = []

            self.objectCordList.append(pointCordList)

        # print(self.boundaries, "\n", self.objectCordList)

    
    def makeCanvas(self):
        self.mainCanvas = np.zeros((self.canvasHeight+self.padx, self.canvasWidth+self.pady)).astype('uint8')
    

    def mergeShape(self):
        self.individualArrayList = []
        i = 0
        for obj in self.objectCordList:
            pts = np.array(obj)
            tempShape = cv2.fillPoly(self.mainCanvas, pts=[pts], color=(255, 255, 255))
            self.individualArrayList.append(tempShape)
            # print(obj)
            # cv2.imshow(f"MERGED SHAPE{i}", tempShape)
            i+=1 
        

        # print(self.mainCanvas.shape)
        # self.mergedImage = cv2.cvtColor(self.mainCanvas, cv2.COLOR_BGR2GRAY)
        # print(self.mainCanvas)
        

    def findVertices(self):
        # _,threshold = cv2.threshold(self.mainCanvas, 110, 255, cv2.THRESH_BINARY)
        
        contours,_=cv2.findContours(self.mainCanvas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        

        verticesList = []
        for lev1 in contours:
            for lev2 in lev1:
                [[tempX, tempY]]= lev2.tolist()
                verticesList.append(tempX+self.xMin)
                verticesList.append(tempY+self.yMin)
        
        self.vertices = verticesList
        
        return verticesList
                    





    

if __name__ == "__main__":
    objectList = [
        [226.0, 176.0, 526.0, 176.0, 526.0, 426.0, 226.0, 426.0],
        [501.0, 398.0, 601.0, 300.0, 601.0, 448.0, 501.0, 448.0]
    ]

    mergeShape = MERGE(objectList)
    vertices = mergeShape.vertices
    cv2.imshow("MERGED", mergeShape.mainCanvas)
    print(vertices)
    cv2.waitKey(0)


