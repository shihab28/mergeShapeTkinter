#!/tool/pandora64/bin/python3.6
import os
from tkinter import *
from PIL import Image, ImageTk


def getImage(imgSaveDir, imageSize = (24, 24)):
    # curDir = os.path.dirname(__file__)
    # imgSaveDir = f"{curDir}/resources/{imgName}"
    imgSave =ImageTk.PhotoImage(Image.open(imgSaveDir).resize(imageSize, Image.ANTIALIAS))
    return imgSave