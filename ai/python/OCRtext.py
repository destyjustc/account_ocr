import cv2
import pytesseract
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def OCRTextLine(img, baseHeight=100, blurSize=5, threshold=180, lang='eng', boxes=False, showPlots=False):
    height, width = img.shape[:2]
    scale = baseHeight/height
    newHeight = int(baseHeight)
    newWidth = int(scale*width)
    imgres = cv2.resize(img,(newWidth, newHeight), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(imgres, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(blurSize,blurSize),0)
    binary_output = np.zeros_like(blur)
    binary_output[blur < threshold] = 1
    output = cv2.connectedComponentsWithStats(binary_output, 8y, cv2.CV_32S)
    img = Image.fromarray(np.uint8((binary_output)))
    output = pytesseract.image_to_string(img, lang, boxes, config="-psm 7")
    if showPlots:
        plt.figure()
        plt.subplot(141)
        plt.imshow(imgres)
        plt.title('original')
        plt.axis('off')
        plt.subplot(142)
        plt.imshow(gray, cmap='gray')
        plt.title('gray')
        plt.axis('off')
        plt.subplot(143)
        plt.imshow(blur, cmap='gray')
        plt.title('blur')
        plt.axis('off')
        plt.subplot(144)
        plt.imshow(binary_output, cmap='gray')
        plt.title('binary')
        plt.axis('off')
    return output


def histConstruct(img, scale=2, axis=1, blurSize=9, threshold=180, showPlot=False):
    height, width = img.shape[:2]
    img = cv2.resize(img,(width, scale*height), interpolation = cv2.INTER_NEAREST)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(blurSize, blurSize),0)
    binary_output = np.zeros_like(blur)
    binary_output[blur < threshold] = 1
    hist = np.sum(binary_output, axis)
    if showPlot:
        plt.figure()
        plt.plot(hist)
    return(hist)


def findTexLine(hist):
    listOfLines = list()
    start = -1
    for i in range(len(hist) - 1):
        if hist[i] == 0 and hist[i+1] > 0:
            start = i
        if hist[i] > 0 and hist[i+1] == 0 and start != -1:
            end = i+1
            listOfLines.append((start, end))
    return listOfLines

def cropLines(img, lineloc):
    return img