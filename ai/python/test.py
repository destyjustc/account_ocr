from PIL import Image
import pytesseract
import cv2
import numpy as np

filename = "../../data/textline.png"
baseHeight = 40.0
connectivity = 8
img = cv2.imread(filename)
height, width = img.shape[:2]
scale = baseHeight/height
newheight = int(baseHeight)
newwidth = int(scale*width)
imgres = cv2.resize(img,(newwidth, newheight), interpolation = cv2.INTER_NEAREST)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height, width = gray.shape[:2]
res = cv2.resize(gray,(newwidth, newheight), interpolation = cv2.INTER_NEAREST)
blur = cv2.GaussianBlur(res,(3,3),0)
binary_output = np.zeros_like(res)
binary_output[res < 200] = 1
img = Image.fromarray(np.uint8((binary_output)))

# img = Image.open('./account_ocr/data/date1.png')
# img = img.convert('RGBA')
# basewidth = int(float(img.size[0])*3)
#
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((basewidth,hsize), Image.ANTIALIAS)
# img = img.convert('1')



output = pytesseract.image_to_string(img, config="-psm 7 -l eng")
print(output)
#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
