import cv2
import pytesseract
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from ai.dictionary import *
import argparse
import math


MIN_ROW_HEIGHT = 30

def OCRTextLine(img, baseHeight=100, blurSize=5, threshold=200, lang='eng', boxes=False, showPlots=False):
    height, width = img.shape[:2]
    scale = baseHeight/height
    newHeight = int(baseHeight)
    newWidth = int(scale*width)
    imgres = cv2.resize(img,(newWidth, newHeight), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(imgres, cv2.COLOR_RGB2YCrCb)[:,:,0]
    #blur = cv2.GaussianBlur(gray,(blurSize,blurSize),0)
    #binary_output = np.zeros_like(blur)
    #binary_output[blur < threshold] = 1
    img = Image.fromarray(np.uint8((gray)))
    output = pytesseract.image_to_string(img, lang, boxes, config="-psm 7")
    if showPlots:
        plt.figure()
        plt.imshow(gray, cmap='gray')
        plt.show()
        # plt.figure()
        # plt.subplot(141)
        # plt.imshow(imgres)
        # plt.title('original')
        # plt.axis('off')
        # plt.subplot(142)
        # plt.imshow(gray, cmap='gray')
        # plt.title('gray')
        # plt.axis('off')
        # plt.subplot(143)
        # plt.imshow(blur, cmap='gray')
        # plt.title('blur')
        # plt.axis('off')
        # plt.subplot(144)
        # plt.imshow(binary_output, cmap='gray')
        # plt.title('binary')
        # plt.axis('off')
    return output


def histConstruct(img, axis=1, blurSize=9, threshold=220, showPlot=False):
    height, width = img.shape[:2]
    img = cv2.resize(img,(width, height), interpolation = cv2.INTER_NEAREST)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)[:, :, 0].astype(float)
    shape = gray.shape
    background = gray[:, 1].copy() - 255.0
    for i  in range(shape[1]):
        gray[:, i] = gray[:, i] - background
    #equ = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(gray,(blurSize, blurSize), 0)
    #background = blur[:, 0]
    #for i  in range(shape[1]):
    #    blur[:, i] = blur[:,i] - background
    binary_output = np.zeros_like(blur)
    binary_output[blur < threshold] = 1
    hist = np.sum(binary_output, axis)
    if showPlot:
        plt.figure()
        plt.subplot(2,2,1)
        plt.imshow(img)
        plt.subplot(2,2,2)
        plt.imshow(gray, cmap='gray')
        plt.subplot(2,2,3)
        plt.imshow(blur, cmap='gray')
        plt.subplot(2,2,4)
        plt.imshow(binary_output, cmap='gray')
        plt.show()
        plt.figure()
        plt.plot(hist)
        plt.show()
    hist = hist - np.min(hist)
    return hist

iparens = iter('(){}[]<>')
parens = dict(zip(iparens, iparens))
closing = parens.values()
def balanced(astr):
    stack = []
    for c in astr:
        d = parens.get(c, None)
        if d:
            stack.append(d)
        elif c in closing:
            if not stack or c != stack.pop():
                return False
    return not stack


def postprocessDigitsColumn(listOfResults):
    prob = []
    listOfResultsNew = []
    for line in listOfResults:
        val = 1.0
        if not balanced(line):
            val /= 2.0
        else:
            for i in range(len(line)):
                c = line[i]
                if  not( c.isdigit() or c == '.' or c =='(' or c ==')' or c == '$'):
                    val /=2.0
                    if c in dictionaryFordigits:
                        tmp = list(line)
                        tmp[i] = dictionaryFordigits[c]
                        line = ''.join(tmp)
        prob.append(val)
        listOfResultsNew.append(line)
    return listOfResultsNew, prob

def postprocessLettersColumn(listOfResults):
    prob = []
    for line in listOfResults:
        prob.append(1.0)
    return listOfResults, prob

def postprocess(listOfResults):
    digitsCount = 0.0
    totalCharacterCount = 0.0
    for line in listOfResults:
        totalCharacterCount += len(line)
        digitsCount += sum(c.isdigit() for c in line)
    if digitsCount / totalCharacterCount > 0.5:
        listOfResults, prob = postprocessDigitsColumn(listOfResults)
    else:
        listOfResults, prob = postprocessLettersColumn(listOfResults)
    return listOfResults, prob


def findColumns(hist, gap = 10):
    listOfColumns = []
    start = -1
    countZeros = 0
    left_pos = [0]
    for i in range(len(hist) - 1):
        if hist[i] == 0:
            countZeros += 1
        if hist[i] > 0 and (countZeros > gap or start == -1):
            start = i
            countZeros = 0
            if start - gap//2 > left_pos[-1]:
                left_pos.append(start - gap//2)
    left_pos.append(len(hist))
    for i in range(len(left_pos) - 1):
        if left_pos[i+1] - left_pos[i] > 20:
            listOfColumns.append((left_pos[i], left_pos[i+1]))

    return listOfColumns




def findTextLine(hist):
    listOfLines = list()
    start = -1
    for i in range(len(hist) - 1):
        if hist[i] == 0 and hist[i+1] > 0:
            start = i
        if hist[i] > 0 and hist[i+1] == 0 and start != -1:
            end = i+1
            if end - start > 5:
                listOfLines.append((start, end))
    return listOfLines


def cropLines(img, lineloc, offset=4):
    return img[max(lineloc[0] - offset, 0) : lineloc[1] + offset, :]

def findLineLocations(filename, top_left = (0,0), bottom_right = None):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if bottom_right is None:
        bottom_right = (img.shape[0], img.shape[1])
    img = img[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1], :]
    hist = histConstruct(img, showPlot=False)
    linesLocation = findTextLine(hist)
    return linesLocation

def pipelineOneColumn(filename, top_left = (0,0), bottom_right = None):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if bottom_right is None:
        bottom_right = (img.shape[0], img.shape[1])
    img = img[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1], :]
    hist = histConstruct(img, showPlot=False)
    linesLocation = findTextLine(hist)
    listOfResults = list()
    print(linesLocation)
    for lineloc in linesLocation:
        # For Chinese use lang='chi_sim'
        listOfResults.append(OCRTextLine(cropLines(img, lineloc), lang='eng', showPlots=False))
    listOfResults, prob = postprocess(listOfResults)
    return linesLocation, listOfResults, prob

def pipelineMultiColumn(filename, top_left = (0,0), bottom_right = None):
    orgimg = cv2.imread(filename)
    orgimg = cv2.cvtColor(orgimg, cv2.COLOR_BGR2RGB)
    if bottom_right is None:
        bottom_right = (orgimg.shape[0], orgimg.shape[1])
    orgimg = orgimg[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1], :]
    histv = histConstruct(orgimg, showPlot=False, axis=0)
    columns = findColumns(histv)
    columnResults =[]
    for column in columns:
        img = orgimg[:, column[0]:column[1]]
        hist = histConstruct(img, showPlot=False)
        linesLocation = findTextLine(hist)
        listOfResults = list()
        print(linesLocation)
        for lineloc in linesLocation:
            # For Chinese use lang='chi_sim'
            listOfResults.append(OCRTextLine(cropLines(img, lineloc), lang='eng', showPlots=False))
        listOfResults, prob = postprocess(listOfResults)
        columnResults.append({"linesLocation":linesLocation, "listOfResults":listOfResults, "prob":prob})
    return columnResults

def linesHeight(filename, top_left = (0,0), bottom_right = None):
    img = cv2.imread(filename)
    if bottom_right is None:
        bottom_right = (img.shape[0], img.shape[1])
    img = img[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
    hist = histConstruct(img)
    linesLocation = findTextLine(hist)
    return linesLocation


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='OCR text')
    # parser.add_argument(
    #     'filename',
    #     type=str,
    #     help='The image file for OCR'
    # )
    # parser.add_argument(
    #     'x1',
    #     type=int,
    #     help='X position of top left'
    # )
    # parser.add_argument(
    #     'y1',
    #     type=int,
    #     help='Y position of top left'
    # )
    # parser.add_argument(
    #     'x2',
    #     type=int,
    #     help='X position of bottom right'
    # )
    # parser.add_argument(
    #     'y2',
    #     type=int,
    #     help='Y position of bottom right'
    # )
    # args = parser.parse_args()
    # filename = args.filename
    # x1 = args.x1
    # y1 = args.y1
    # x2 = args.x2
    # y2 = args.y2

    filename='../../data/test.png'
    columnResults = pipelineMultiColumn(filename)
    for results in columnResults:
        loc = results['linesLocation']
        result  = results['listOfResults']
        prob = results['prob']
        print('from {} to {} : {} prob {}'.format(loc[0], loc[1], result, prob))