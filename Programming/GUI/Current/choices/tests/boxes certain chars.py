import re
import cv2
import pytesseract
from pytesseract import Output


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
img = cv2.imread('image1.png')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
keys = list(d.keys())
datePattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/([12][0-9])\d\d$'
pricePattern = '[+]?[0-9]+\.[0-9]+'
doorNum = '[0-9]{1,3}(?![0-9])'
Names = '[A-Z]+[a-z]+$'


def str_list(str_list):
    n = 0
    while n < len(str_list):
        str_list[n] = int(str_list[n])
        n += 1
    return(str_list)

def findSubstring(objectList, string):
    return string in objectList


cv2.imshow('img', img)
cv2.waitKey(0)


prices = []
numbers = []
names = []
checkPrice = 0
values = d['text']
values = list(filter(None, values))
#values = list(map(int, values))
# gets rid of empty spaces in the list

try:
    priceIndex = (values.index("Subtotal")) + 1
except:
    priceIndex = (values.index("Total")) + 1

totalPrice = values[priceIndex]



for i in range(len(values)):
    if findSubstring(values[i], 'Road') == True or findSubstring(values[i], 'road') == True or findSubstring(values[i], 'Rd') == True:
        placeIndex = i


for i in range(len(values)):
    if re.match(datePattern, values[i]):
        date = values[i] # any date on the receipt
    if re.match(pricePattern, values[i]):
        prices.append(values[i]) #list of prices to place in db
    if re.match(doorNum, values[i]):
        numbers.append(values[i]) #list of all the numbers in receipt
    if re.match(Names, values[i]):
        names.append(values[i]) #list of all words with capital letters in receipt

checkList = values[:priceIndex] # everything before the word 'total' or eqv.
for i in range(len(checkList)):
    if re.match(pricePattern, checkList[i]): #if there is a float
        temp = float(checkList[i])
        checkPrice = temp + checkPrice #add all floats for a checkPrice value


if placeIndex == None:
    None
else:
    if int(values[placeIndex - 2]) == int(values[placeIndex - 2]):
        address = values[placeIndex - 2] , values[placeIndex - 1] , values[placeIndex]
    elif int(values[placeIndex + 1]):
        address = values[placeIndex + 1]

placeOfPurchase = names[0]

##########################COMPLETE##########################
#placeOfPurchase
#Date
#subtotal
#Address

############################TODO############################
#prices of individual items
#item names
#contact details?
#iintegrate into your codes

print (values)
print (data)

print(hello)
