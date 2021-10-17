from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import sys
import sqlite3 as sq
import os
import datetime
import time

root = Tk()
root.title("Lucid - Edit Data")
root.configure(background = '#ffffff')
root.config(height = 1600, width = 800)
root.state('zoomed')

os.chdir('C:/Users/zubi_/Desktop/[project_skyfall]/Programming/GUI/Current')


#if user clicks on Input/Edit/GenerateReport then the file will load
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



root1 = Button(root, image = inputImage, command=InputData)
root1.place(relx = 0.04, rely = 0, anchor= "n")


root2 = Button(root, image = editImage, command=EditData, state = DISABLED)
root2.place(relx = 0.115, rely = 0, anchor = "n")


root3 = Button(root, image = genImage, command = GenerateReport)
root3.place(relx = 0.19, rely = 0, anchor = "n")


receipts = "Clients and Receipts.db"

#SQL Table in Tkinter



#Function to execute database queries

def runQ(query, para=()):
    with sq.connect(receipts) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, para)
        conn.commit()
    return result

def getTable(Table, query):
    records = Table.get_children()
    print(records)
    for elements in records:
        Table.delete(records)

    tblRows = runQ(query)

    try:
        for row in tblRows:
            Table.insert('', 'end', values=(row[0], row[1], row[2]))
    except:
        for row in tblRows:
            Table.insert('', 'end', values=(row[0], row[1]))

def deleteRecord():
    try:
        sqTable.item(sqTable.selection())['values'][0]
    except IndexError as e:
        messagebox.showerror("Error","Select a record to delete")
        return
    record = sqTable.item(sqTable.selection())['values'][0]
    record2 = sqTable.item(sqTable.selection())['values'][1]
    que = 'DELETE FROM RECEIPTS WHERE total_price = ? and place_of_purchase = ?'
    runQ(que, (record, record2))
    messagebox.showinfo("Success", "Record has been successfully deleted")


    sqTable.delete(*sqTable.get_children())
    que = 'SELECT total_price, place_of_purchase, Date_of_Purchase FROM RECEIPTS'
    tblRows = runQ(que)

    for row in tblRows:
        sqTable.insert('', 'end', values=(row[0], row[1], row[2]))

#def selectItem(a):
#    curItem = sqTable.focus()
#    print sqTable.item(curItem)

def editReceipt():
    try:
        sqTable.item(sqTable.selection())['values'][0]
    except IndexError as e:
        messagebox.showerror("Error","Select a record to edit")
        return

    record = sqTable.item(sqTable.selection())['text']
    currentPrice = sqTable.item(sqTable.selection())['values'][0]
    currentLocation = sqTable.item(sqTable.selection())['values'][1]
    currentDate = sqTable.item(sqTable.selection())['values'][2]

    #print (old_item)
    #print(old_date)
    #print(old_price)

    editRecord = Toplevel()

    editRecord.title = 'Lucid - Edit Data'
    editRecord.configure(background = '#ffffff')

    #old date
    Label(editRecord, text = 'Current Total Price:', font = 'Adam').grid(row = 0, column = 1)
    Entry(editRecord, textvariable = StringVar(editRecord, value = currentPrice), state = 'readonly').grid(row = 0, column = 2)

    #new date
    Label(editRecord, text = 'New Total Price:', font = 'Adam').grid(row = 1, column = 1)
    newPrice = Entry(editRecord)
    newPrice.grid(row = 1, column = 2)

    # Current Item Name
    Label(editRecord, text = 'Current Location:', font = 'Adam').grid(row = 2, column = 1)
    Entry(editRecord, textvariable = StringVar(editRecord, value = currentLocation), state = 'readonly').grid(row = 2, column = 2)

    # Updated item name
    Label(editRecord, text = 'New Location:', font = 'Adam').grid(row = 3, column = 1)
    newLocation= Entry(editRecord)
    newLocation.grid(row = 3, column = 2)

    # old Tprice
    Label(editRecord, text = 'Current Date:', font = 'Adam').grid(row = 4, column = 1)
    Entry(editRecord, textvariable = StringVar(editRecord, value = currentDate), state = 'readonly').grid(row = 4, column = 2)

    # new Tprice
    Label(editRecord, text = 'New Date:', font = 'Adam').grid(row = 5, column = 1)
    newDate= Entry(editRecord)
    newDate.grid(row = 5, column = 2)


    Button(editRecord, text = 'Update', font = 'Adam', command = lambda: updateRecord(editRecord, currentPrice, currentLocation, currentDate, newPrice.get(), newLocation.get(), newDate.get())).grid(row = 6, column = 2, sticky = W)


    editRecord.mainloop()



def updateRecord(gui, oldPrice, oldLocation, oldDate, newPrice, newLocation, newDate):
    try:
        unixDateSales = time.mktime(datetime.datetime.strptime(newDate, "%d/%m/%y").timetuple())
        query = 'UPDATE RECEIPTS SET total_price = ?, place_of_purchase = ?, Date_of_Purchase = ?, unix_date_purchase = ? WHERE total_price = ? and place_of_purchase = ?'
        parameters = (newPrice, newLocation, newDate, unixDateSales, oldPrice, oldLocation)
        runQ(query, parameters)

        sqTable.delete(*sqTable.get_children())

        que = 'SELECT total_price, place_of_purchase, Date_of_Purchase FROM RECEIPTS'
        tblRows = runQ(que)

        for row in tblRows:
            sqTable.insert('', 'end', values=(row[0], row[1], row[2]))
        gui.destroy()
        messagebox.showinfo("Success","Record has been updated")
    except:
        messagebox.showerror("Error", "Please input the date in format dd/mm/yy")



#delete and edit buttons


def createReceipts():
    global sqTable
    sqTable = ttk.Treeview(height = 20, columns = ('Total Price', 'Location', 'Date'))

    #specified one less as treeview uses #0
    sqTable.grid(row = 5, column = 5, columnspan = 7)
    sqTable.place(relx = 0.12, rely = 0.2)
    sqTable.heading('#0', text = '', anchor = CENTER)
    sqTable.column('#0', stretch = NO, minwidth = 0, width = 0)
    sqTable.heading('#1', text = 'Date Purchased', anchor = CENTER)
    sqTable.heading('#2', text = 'Total Price', anchor = CENTER)
    sqTable.heading('#3', text = 'Location', anchor = CENTER)
    que = 'SELECT total_price, place_of_purchase, Date_of_Purchase FROM RECEIPTS'
    getTable(sqTable, que)

#def createItems():
    global itemTable

    itemTable = ttk.Treeview(height = 20, column = ("Item Name", "Item Price"))
    itemTable.grid(row = 5, column = 5, columnspan = 7)
    itemTable.place(relx = 0.6, rely = 0.2)
    itemTable.heading('#0', text = '', anchor = CENTER)
    itemTable.column('#0', stretch = NO, minwidth = 0, width = 0)
    itemTable.heading('#1', text = 'Item Name', anchor = CENTER)
    itemTable.heading('#2', text = 'Item Price', anchor = CENTER)
    query = 'SELECT item_purchased, item_price FROM ITEM'
    getTable(itemTable, query)


createReceipts()


Button(text = 'Delete Record', font = 'Adam', command = deleteRecord).place(relx = 0.6, rely = 0.81)
Button(text = 'Edit Record', font = 'Adam' , command = editReceipt).place(relx = 0.3, rely = 0.81)



root.mainloop()
