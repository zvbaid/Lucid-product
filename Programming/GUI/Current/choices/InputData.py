from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sys
import pytesseract
from pytesseract import Output
import re
import cv2
import matplotlib
import os
import sqlite3 as sq
import time
import datetime


##hardcoded
client_id = 1


root = Tk()
root.title("Lucid - Input Data")
root.configure(background = '#ffffff')
root.config(height = 1600, width = 800)
root.state('zoomed')

os.chdir('C:/Users/zubi_/Desktop/[project_skyfall]/Programming/GUI/Current')

global filenames
fileQueue = []
#is empty each time data is input

def InputData():
    root.destroy()
    import choices.InputData

def EditData():
    root.destroy()
    import choices.EditData

def GenerateReport():
    root.destroy()
    import choices.GenerateReport


inputImage = ImageTk.PhotoImage(Image.open("input.png"))
editImage = ImageTk.PhotoImage(Image.open("edit.png"))
genImage = ImageTk.PhotoImage(Image.open("genreport.png"))



inputData = Button(image = inputImage, command=InputData, state = DISABLED).place(relx = 0.04, rely = 0, anchor= "n")
EditData = Button(image = editImage, command=EditData).place(relx = 0.115, rely = 0, anchor = "n")
GenReport = Button(image = genImage, command = GenerateReport).place(relx = 0.19, rely = 0, anchor = "n")
fileView = Listbox(root, width = 40, height = 20, font = "Adam")
fileView.place(relx = 0.1, rely = 0.3)



def fileroot():
    root.filename = filedialog.askopenfilenames(initialdir="/",filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
    files = list(root.filename)
    for i in range(len(files)):
        fileView.insert(i, files[i])
        fileQueue.append(files[i])

fileChoose = Button(text = "Choose files", font = 'Adam', command = fileroot)
fileChoose.place (relx = 0.1, rely = 0.8)

def storeToTes(date, subtotal, location, item, itemPrice):
    db = sq.connect('Clients and Receipts.db')
    c = db.cursor()

    try:
        unixDate = time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())
        #date = datetime.datetime.fromtimestamp(unixDate)
        query = ''' INSERT INTO RECEIPTS
                    (client_id ,Date_of_Purchase, unix_date_purchase, total_price, place_of_purchase)
                    VALUES
                    (?,?,?,?,?)
                    '''
        receiptDetails = (client_id, str(date), float(unixDate), str(subtotal), str(location))
    except:
        query = ''' INSERT INTO RECEIPTS
                    (client_id, Date_of_Purchase, total_price, place_of_purchase)
                    VALUES
                    (?,?,?,?)
                    '''
        receiptDetails = (client_id, str(date), str(subtotal), str(location))


    c.execute(query, receiptDetails)

    c.execute('SELECT MAX(receipt_id) FROM RECEIPTS')
    temp = []
    for row in c.fetchall():
        temp.append(int(row[0]))
        receipt_id = int(temp[0])

    for i in range(len(itemPrice)):
        query = ('''INSERT INTO ITEM
                    (receipt_id, item_purchased, item_price)
                    VALUES
                    (?,?,?)''')
        items = (receipt_id, item[i], itemPrice[i])
        c.execute(query, items)

    db.commit()
    db.close()



def storeToReceipts(gui, date, subtotal, location):
        db = sq.connect('Clients and Receipts.db')
        c = db.cursor()

        try:
            unixDate = time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())
            print(unixDate)
            query = ''' INSERT INTO RECEIPTS
                        (client_id ,Date_of_Purchase, unix_date_purchase, total_price, place_of_purchase)
                        VALUES
                        (?,?,?,?,?)'''
            receiptDetails = (client_id, str(date), float(unixDate), str(subtotal), str(location))
            c.execute(query, receiptDetails)
            gui.destroy()
            messagebox.showinfo("Success","Data has been stored")
            db.commit()
            db.close()
        except:
            gui.destroy()
            messagebox.showerror("Error","Please try again.\nEnter the date in dd/mm/yy format")


length = []
for i in range(len(fileQueue)):
    length.append(i)
#tesseract
def tesseractOCR ():
    if len(fileQueue) > 0:
        for i in range(len(fileQueue)):
            path = fileQueue[i]
            print(path)
            image = cv2.imread(path)
            grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grey = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


            if path[-4:] == ".jpg":
                filename = "{}.jpg".format(os.getpid())
            elif path[-4:] == ".png":
                filename = "{}.png".format(os.getpid())

            cv2.imwrite(filename, grey)


            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            d = pytesseract.image_to_data(filename, output_type=Output.DICT)
            os.remove(filename)
            keys = list(d.keys())
            datePattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/([12][0-9])\d\d$'
            pricePattern = '[+]?[0-9]+\.[0-9]+'
            doorNum = '[0-9]{1,3}(?![0-9])'
            Names = '[A-Z]+[a-z]+$'


            def strList(list):
                for i in range(len(list)):
                    try:
                        list[i] = int(list[i])
                    except:
                        None
                return list

            def findSubstring(objectList, string):
                return string in objectList

            date = ''
            prices = []
            numbers = []
            names = []
            checkPrice = 0
            values = d['text']
            values = list(filter(None, values))
            print(values)
            # gets rid of empty spaces in the list

            if len(values) != 0:
                try:
                    priceIndex = (values.index("Subtotal")) + 1
                except:
                    priceIndex = 0

                try:
                    priceIndex = (values.index("Total")) + 1
                except:
                    priceIndex = 0


            totalPrice = values[priceIndex]

            for i in range(len(values)):
                if findSubstring(values[i], 'Road') == True or findSubstring(values[i], 'road') == True or findSubstring(values[i], 'Rd') == True:
                    placeIndex = i
                else:
                    placeIndex = 2


            for i in range(len(values)):
                if re.match(datePattern, values[i]):
                    date = values[i]
                    # any date on the receipt
                if re.match(pricePattern, values[i]):
                    prices.append(values[i])
                    #list of prices to place in db
                if re.match(doorNum, values[i]):
                    numbers.append(values[i])
                    #list of all the numbers in receipt
                if re.match(Names, values[i]):
                    names.append(values[i])
                    #list of all words with capital letters in receipt
            checkList = values[:priceIndex]
            # everything before the word 'total' or eqv.

            items = []
            itemsPrices = []
            for i in range(len(checkList)):
                if re.match(pricePattern, checkList[i]): #if there is a float
                    items.append(checkList[i-1])
                    itemsPrices.append(checkList[i])


            try:
                if int(values[placeIndex - 2]) == int(values[placeIndex - 2]):
                    address = values[placeIndex - 2] , values[placeIndex - 1] , values[placeIndex]
                elif int(values[placeIndex + 1]):
                    address = values[placeIndex + 1]
                else:
                    None
            except:
                address = 1

            placeOfPurchase = names[0]
            address = str(placeOfPurchase) + str(address)
            storeToTes(date, totalPrice, address, items, itemsPrices)
            message = "Scanning is complete; " + "/" + str(len(fileQueue))
            messagebox.showinfo("Success", message)
            fileView.delete(0, END)
            print(date)
            # clears the displayed box of any receipts
    else:
        messagebox.showerror("Error", "No files have been selected")
        #if there is nothing in the listbox, an error box is displayed
    

def storeToSales(gui, Date, Price, Item):
    db = sq.connect('Clients and Receipts.db')
    c = db.cursor()

    try: #exception handling to see if a date exists
        unixDate = time.mktime(datetime.datetime.strptime(Date, "%d/%m/%y").timetuple())
        query = '''INSERT INTO SALES_MADE
        (client_id, Date_Of_Sale, unix_date_sales, Revenue, ItemSold)
        VALUES
        (?,?,?,?,?)
        '''
        sale = (client_id, str(Date), float(unixDate),float(Price), str(Item))

        c.execute(query, sale)
        db.commit()
        db.close()

        gui.destroy()
        messagebox.showinfo("Success","Sales have been added")
    except:
        gui.destroy()
        messagebox.showerror("Error","Please enter the date in dd/mm/yy format")
        #unicode date created to allow sorting of the dates

global receipt_id
receipt_id = []
none = 0

def increment(none):
    none += 1
    return none

def storeToItems(name, price, receipt_id, none):
        none = increment(none)
        print(none)
        db = sq.connect('Clients and Receipts.db')
        c = db.cursor()

        query = ('''SELECT max(receipt_id)
                    FROM RECEIPTS''') # returns the largest receipt_id
        c.execute(query)
        for row in c.fetchall():
            receipt_id.append(int(row[0]) + 1)
            print(receipt_id)
            receipt_id = int(receipt_id[0]) #this will be the new receipt id

        c.execute(''' INSERT INTO RECEIPTS (place_of_purchase)
                    VALUES (?)''', str(none))

        query2 = ('''INSERT INTO ITEM (receipt_id, item_purchased, item_price)
                    VALUES (?,?,?)''')
        values = (receipt_id, name, price)

        c.execute(query2, values)

        db.commit()
        c.close()

def inputItems():
    inputItems = Toplevel()
    inputItems.configure(background = '#ffffff')


    Label(inputItems, text = 'Item Name', font = 'Adam', bg = 'white').grid(row = 1, column = 1)
    itemName = Entry(inputItems)
    itemName.grid(row = 1, column = 2)

    #price of item sold
    Label(inputItems, text = 'Item Price', font = 'Adam', bg = 'white').grid(row = 2, column = 1)
    itemPrice = Entry(inputItems)
    itemPrice.grid(row = 2, column = 2)

    Submit = Button(inputItems, text = 'Submit', font = 'Adam', command = lambda: storeToItems(itemName.get(), itemPrice.get(), receipt_id, none)).grid(row = 3, column = 2)

    inputItems.mainloop()

def inputSales():
    inputSale = Toplevel()

    #date of item sold
    Label(inputSale, text = 'Date', font = 'Adam').grid(row = 1, column = 1)
    Date = Entry(inputSale)
    Date.grid(row = 1, column = 2)

    #price of item sold
    Label(inputSale, text = 'Selling Price', font = 'Adam').grid(row = 2, column = 1)
    Price = Entry(inputSale)
    Price.grid(row = 2, column = 2)

    #item sold
    Label(inputSale, text = 'Item Sold', font = 'Adam').grid(row = 3, column = 1)
    Item = Entry(inputSale)
    Item.grid(row = 3, column = 2)

    Button(inputSale, text = 'Submit', font = 'Adam',command = lambda: storeToSales(inputSale, Date.get(), Price.get(), Item.get())).grid(row = 4, column = 2)

    inputSale.mainloop()

def inputReceiptData():
    inputRD = Toplevel()
    inputRD.configure(background = '#ffffff')
    #date of item sold
    Label(inputRD, text = 'Date', font = 'Adam', bg = 'white').grid(row = 1, column = 1)
    Date = Entry(inputRD)
    Date.grid(row = 1, column = 2)

    #price of item sold
    Label(inputRD, text = 'Subtotal', font = 'Adam', bg = 'white').grid(row = 2, column = 1)
    Subtotal = Entry(inputRD)
    Subtotal.grid(row = 2, column = 2)

    #item sold
    Label(inputRD, text = 'Address', font = 'Adam', bg = 'white').grid(row = 3, column = 1)
    Address = Entry(inputRD)
    Address.grid(row = 3, column = 2)


    Item = Button(inputRD, text = 'Items On Receipt', font = 'Adam', command = lambda: inputItems()).grid(row = 4, column = 2)#, command = lambda: inputItems())
    Submit = Button(inputRD, text = 'Submit', font = 'Adam', command = lambda: storeToReceipts(inputRD, Date.get(), Subtotal.get(), Address.get())).grid(row = 4, column = 1)


    inputRD.mainloop()


runOCR = Button(text = "Run Scanner", font = 'Adam', command = tesseractOCR).place (relx = 0.25, rely = 0.8)

input_sales = Button(text = "Input Sales", font = ('Adam', 20), command = inputSales).place(relx = 0.7, rely = 0.2)
input_costs = Button(text = "Input Receipt Data", font = ('Adam', 20), command = inputReceiptData).place(relx = 0.7, rely = 0.6)



pick = Label(text ="Please select images for scanning", border = 0, font = ("Adam", 26), bg = "white").place( relx=0.05, rely = 0.2 )

root.mainloop()
