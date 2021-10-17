#get path from user

from PIL import Image
import pytesseract
import cv2
import matplotlib
import os
from pytesseract import Output

path = input("Please specify file path\n> ")
image = cv2.imread(path)

#cv2.imshow("Hello", image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Jello", gray)

##preprocess = input("Which preprocess would you like?\n> ")
##
##if preprocess == "thresh":
##    gray = cv2.threshold(gray, 0, 255,
##                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
##    cv2.imshow("threshold", gray)
##elif preprocess == "blur":
##    gray = cv2.medianBlur(gray,3)
##    cv2.imshow("blur",gray)


if path[-4:] == ".jpg":
    filename = "{}.jpg".format(os.getpid())
elif path[-4:] == ".png":
    filename = "{}.png".format(os.getpid())

    
cv2.imwrite(filename, gray)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
##text = pytesseract.image_to_string(Image.open(filename))
##os.remove(filename)
##print(text)
##
##f = open ("ocr.txt", "a")
##f.write(text)
##f.close()
##
##with open("ocr.txt") as infile, open('outfile.csv','a') as outfile:
##    for line in infile:
##        outfile.write(line.replace(' ',','))


#img = cv2.imread('image.jpg')
d = pytesseract.image_to_data(image, output_type=Output.DICT)
print(d)
