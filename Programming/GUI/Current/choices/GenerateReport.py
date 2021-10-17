from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import sqlite3 as sq
import datetime
import time
from tkinter import messagebox
from fpdf import FPDF


root = Tk()
root.title("Lucid - Generate Report")
root.configure(background = '#ffffff')
root.config(height = 1600, width = 800)
root.state('zoomed')

os.chdir('C:/Users/zubi_/Desktop/[project_skyfall]/Programming/GUI/Current')

plt.style.use('seaborn')

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


root2 = Button(root, image = editImage, command=EditData)
root2.place(relx = 0.115, rely = 0, anchor = "n")


root3 = Button(root, image = genImage, command = GenerateReport, state = DISABLED)
root3.place(relx = 0.19, rely = 0, anchor = "n")





db = sq.connect('Clients and Receipts.db')
c = db.cursor()

###Generate Graph for given dates###
startST = StringVar()
endST = StringVar()

startCT = StringVar()
endCT = StringVar()

startPT = StringVar()
endPT = StringVar()

#==================Sales Time Graph==================#

def salesTimeGraph(start, end):
    try:
        unixStart = time.mktime(datetime.datetime.strptime(start, "%d/%m/%y").timetuple())
        unixEnd = time.mktime(datetime.datetime.strptime(end, "%d/%m/%y").timetuple())

        query = '''SELECT Date_Of_Sale, Revenue FROM SALES_MADE ORDER BY unix_date_sales ASC'''
        c.execute(query)
        dates = []
        revenue = []
        for row in c.fetchall():
            dates.append(row[0])
            revenue.append(row[1])

        unixDates = []
        for i in range(len(dates)): #changes dates to unix
            unixDates.append(time.mktime(datetime.datetime.strptime(dates[i], "%d/%m/%y").timetuple()))

        finalDates = []
        for i in range(len(unixDates)): #finds dates in range given by user
            if unixDates[i] >= unixStart and unixDates[i] <= unixEnd:
                finalDates.append(unixDates[i])

        finalRevenue = []
        for i in range(len(finalDates)):
            a = unixDates.index(finalDates[i])
            print(a)
            finalRevenue.append(revenue[a])
            obj = datetime.datetime.fromtimestamp(finalDates[i])
            finalDates[i] = obj


        plt.plot_date(finalDates, finalRevenue, '-')
        plt.show()
    except:
        messagebox.showerror("Error", "Please input your dates in format dd/mm/yy")

Label(root, text = 'Graph for sales / time', font = ('Adam', 15)).place(relx = 0.05, rely = 0.1)
Label(root, text = 'Start Date', font = 'Adam').place(relx = 0.05, rely = 0.2)
SalesStartDate = Entry(root, textvariable = startST).place(relx = 0.05, rely = 0.25)
Label(root, text = 'End Date', font = 'Adam').place(relx = 0.05, rely = 0.3)
SalesEndDate = Entry(root, textvariable = endST).place(relx = 0.05, rely = 0.35)

Button(root, text = "Generate", font = "Adam", command = lambda: salesTimeGraph(startST.get(), endST.get())).place(relx = 0.1, rely = 0.4)


#==================Costs Time Graph==================#
def costsTimeGraph(start, end):
    db = sq.connect('Clients and Receipts[NEW].db')
    c = db.cursor()
    unixStart = time.mktime(datetime.datetime.strptime(start, "%d/%m/%y").timetuple())
    unixEnd = time.mktime(datetime.datetime.strptime(end, "%d/%m/%y").timetuple())

    query = '''SELECT total_price, Date_of_Purchase FROM RECEIPTS ORDER BY unix_date_purchase ASC'''
    c.execute(query)
    dates = []
    costs = []
    for row in c.fetchall():
        costs.append(row[0])
        dates.append(row[1])

    unixDates = []
    for i in range(len(dates)): #changes dates to unix
        unixDates.append(time.mktime(datetime.datetime.strptime(dates[i], "%d/%m/%y").timetuple()))

    finalDates = []
    for i in range(len(unixDates)): #finds dates in range given by user
        if unixDates[i] >= unixStart and unixDates[i] <= unixEnd:
            finalDates.append(unixDates[i])

    finalCosts = []
    for i in range(len(finalDates)):
        a = unixDates.index(finalDates[i])
        print(a)
        finalCosts.append(costs[a])
        obj = datetime.datetime.fromtimestamp(finalDates[i])
        finalDates[i] = obj


    plt.plot_date(finalDates, finalCosts, '-')
    plt.show()

Label(root, text = 'Graph for costs / time', font = ('Adam', 15)).place(relx = 0.05, rely = 0.6)
Label(root, text = 'Start Date', font = 'Adam').place(relx = 0.05, rely = 0.7)
CostsStartDate = Entry(root, textvariable = startCT).place(relx = 0.05, rely = 0.75)
Label(root, text = 'End Date', font = 'Adam').place(relx = 0.05, rely = 0.8)
CostsEndDate = Entry(root, textvariable = endCT).place(relx = 0.05, rely = 0.85)

Button(root, text = "Generate", font = "Adam", command = lambda: costsTimeGraph(startCT.get(), endCT.get())).place(relx = 0.1, rely = 0.9)


#==================Profits Time Graph==================#

def profitsGraph(start, end):
    unixStart = time.mktime(datetime.datetime.strptime(start, "%d/%m/%y").timetuple())
    unixEnd = time.mktime(datetime.datetime.strptime(end, "%d/%m/%y").timetuple())

    query = '''SELECT total_price, Date_of_Purchase FROM RECEIPTS ORDER BY unix_date_purchase ASC'''
    c.execute(query)
    datesCosts = []
    costs = []
    for row in c.fetchall():
        costs.append(row[0])
        datesCosts.append(row[1])


    query = '''SELECT Date_Of_Sale, Revenue FROM SALES_MADE ORDER BY unix_date_sales ASC'''
    c.execute(query)
    datesSales = []
    revenue = []
    for row in c.fetchall():
        datesSales.append(row[0])
        revenue.append(row[1])

    print(costs)
    print(datesCosts)
    print(datesSales)
    print(revenue)



    for i in range (len(datesCosts)):
        if costs.index(datesCosts[i]):
            costIndex = salesCosts.index(datesCosts[i])
            finalCosts.append(costs[costIndex])
# profits can be between dates
#try something similiar to before
    plt.plot_date(datesSales, revenue, '-')
    plt.plot_date(datesCosts, costs, '-')
    plt.show()

Label(root, text = 'Graph for Profts', font = ('Adam', 15)).place(relx = 0.35, rely = 0.1)
Label(root, text = 'Start Date', font = 'Adam').place(relx = 0.35, rely = 0.2)
ProfitsStartDate = Entry(root, textvariable = startPT).place(relx = 0.35, rely = 0.25)
Label(root, text = 'End Date', font = 'Adam').place(relx = 0.35, rely = 0.3)
ProfitsEndDate = Entry(root, textvariable = endPT).place(relx = 0.35, rely = 0.35)

Button(root, text = "Generate", font = "Adam", command = lambda: profitsGraph(startPT.get(), endPT.get())).place(relx = 0.4, rely = 0.4)



#==================Amount Spent on day X==================#

def DateSpentX(date):
    try:
        unixDate = time.mktime(datetime.datetime.strptime(date, "%d/%m/%y").timetuple())
        query = '''SELECT total_price FROM RECEIPTS WHERE Date_of_Purchase = ?'''
        c.execute(query, (date,))

        spent = []
        for i in c.fetchall():
            spent.append(i[0])

        total = 0

        for i in range(len(spent)):
            total += spent[i]

        message = ("You have spent a total of: £"+ str(total))
        messagebox.showinfo("Success",message)

    except:
        messagebox.showerror("Error", "Date not found")

dateSpent = StringVar()

Label(root, text = "Reports:",font = ("Adam",25)).place(relx = 0.75, rely = 0.05)
Label(root, text = "Money spent on day:", font = 'Adam').place(relx = 0.6, rely = 0.2)
DateSpent = Entry(root, textvariable = dateSpent).place(relx = 0.6, rely = 0.25)

Button(root, text ="Generate", font = 'Adam', command = lambda: DateSpentX(dateSpent.get())).place(relx = 0.65, rely = 0.3)

#==================Amount spent More/Less Than==================#
def AmountSpent(amount, inequality):
    query = '''SELECT Date_of_Purchase, total_price FROM RECEIPTS ORDER BY unix_date_purchase ASC'''
    c.execute(query)

    spent = []
    dates = []
    for i in c.fetchall():
        dates.append(i[0])
        print(dates)
        spent.append(i[1])
        print(spent)

    totalSpent = []
    amountDate = []
    if inequality == "More Than":
        report = FPDF()

        report.add_page()
        report.set_font("Arial", size = 15)
        report_line1 = "Days spent more than: £"+amount
        report.cell(200, 10, txt = report_line1,
             ln = 1, align = 'C')
        for i in range(len(spent)):
            if float(amount) < float(spent[i]):
                totalSpent.append(spent[i])
                print(totalSpent)
                amountDate.append(dates[i])
                print(amountDate)

            report.cell(200, 10, txt = "Date: "+str(amountDate[i]),ln = (2 + i), align = 'L')
            report.cell(200, 10, txt = "Amount: "+str(totalSpent[i]), ln = (2 + i), align = 'C')

        report.output("AmountSpentMoreThanX.pdf", 'F')
        messagebox.showinfo("Success","Please check your folder for the report")

    elif inequality == "Less Than":
        report = FPDF()
        report.add_page()
        report.set_font("Arial", size = 15)
        report_line1 = "Days spent more than: £"+amount
        report.cell(200, 10, txt = report_line1,
             ln = 1, align = 'C')
        for i in range(len(spent)):
            if float(amount) > float(spent[i]):
                totalSpent.append(spent[i])
                amountDate.append(dates[i])

            # add another cell
            report.cell(200, 10, txt = "Date: "+str(amountDate[i]),ln = (2 + i), align = 'L')
            report.cell(200, 10, txt = "Amount: "+str(totalSpent[i]), ln = (2 + i), align = 'C')

        report.output("AmountSpentLessThanX.pdf", 'F')
        messagebox.showinfo("Success","Please check your folder for the report")
    else:
        messagebox.showerror("Error", "Please check your fields")


    print(totalSpent)
    print(amountDate)


amount = StringVar()
inequality = StringVar()

Label(root, text = "Amount spent:", font = 'Adam').place(relx = 0.6, rely = 0.5)
Inequality = Entry(root, textvariable = inequality)
Inequality.place(relx = 0.6, rely = 0.55)
Label(root, text = "More Than/Less Than", font = 'Adam').place(relx = 0.6, rely = 0.5)
Amount = Entry(root, textvariable = amount)
Amount.place(relx = 0.6, rely = 0.65)

Button(root, text ="Generate", font = 'Adam', command = lambda: AmountSpent(amount.get(),inequality.get())).place(relx = 0.65, rely = 0.7)

#==================Profit Loss Statement==================#
def getBalanceSheet(start, end):
    unixStart = time.mktime(datetime.datetime.strptime(start, "%d/%m/%y").timetuple())
    unixEnd = time.mktime(datetime.datetime.strptime(end, "%d/%m/%y").timetuple())

    c.execute('''SELECT total_price, Date_of_Purchase, unix_date_purchase FROM RECEIPTS ORDER BY unix_date_purchase ASC''')
    costsData = c.fetchall()
    costs = []
    costDate = []
    unixPurchase = []
    for row in costsData:
        costs.append(row[0])
        costDate.append(row[1])
        unixPurchase.append(row[2])


    finalDatesCosts = []
    finalCosts = []
    for i in range(len(unixPurchase)):
        if unixPurchase[i] >= unixStart and unixPurchase[i] <= unixEnd:
            finalDatesCosts.append(costDate[i])
            finalCosts.append(costs[i])

    #this loop gives the dates that between the user wants the report between - from the receipts table

    c.execute('''SELECT Date_Of_Sale, Revenue, unix_date_sales FROM SALES_MADE ORDER BY unix_date_sales ASC''')
    salesDate = []
    sales = []
    unixSales = []
    for row in c.fetchall():
        salesDate.append(row[0])
        sales.append(row[1])
        unixSales.append(row[2])

    finalDatesSales = []
    finalSales = []
    for i in range(len(unixSales)):
        if unixSales[i] >= unixStart and unixSales[i] <= unixEnd:
            finalDatesSales.append(salesDate[i])
            finalSales.append(sales[i])

    #this loop gives the dates that between the user wants the report between - from the sales tables
    Revenue = 0
    Costs = 0

    def nothing():
        #for date in range(len(finalDatesCosts)):
        #    for i in range(12): #number of months in a year
        #        if '0'+str(i+1) == finalDatesCosts[date][3:5] or str(i+1) == finalDatesCosts[date][3:5]: #looks for
        #            for a in range(len(finalCosts)):
        #                Revenue += float(finalCosts[date])
        #        else:
        #            totalMonths9 = 0
        None

    for i in range(len(finalCosts)):
        Revenue += float(finalCosts[i])

    for i in range(len(finalSales)):
        Costs += float(finalSales[i])

    Profits = str(Revenue - Costs)
    print('£' +str(Costs))
    print('£'+str(Revenue))
    print(Profits)


    report = FPDF()

    report.add_page()
    report.set_font("Arial", size = 15)
    report_line1 = "Profit/Loss Statement for dates "+ start+ " - " + end
    report.cell(200, 10, txt = report_line1,
         ln = 1, align = 'C')

    # add another cell
    report.cell(200, 10, txt = "Statement for Yunus Saleh",ln = 2, align = 'L')
    report.cell(200, 10, txt = "Statement for Yunus Saleh - Tailoring", ln = 3, align = 'L')
    report.cell(200, 10, txt = "Total Revenue £:", ln = 4, align = 'L')
    report.cell(200, 10, txt = str(Revenue), ln = 4, align = 'R')
    report.cell(200, 10, txt = "Total Costs £:", ln = 5, align = 'L')
    report.cell(200, 10, txt = str(Costs), ln = 5, align = 'R')
    report.cell(200, 10, txt = "Total Proits £:", ln = 6, align = 'L')
    report.cell(200, 10, txt = Profits, ln = 6, align = 'R')

    report.output("Profit/Loss.pdf", 'F')
    #os.rename(file, "Documents/Lucid Reports/"+file)


    print(sales)




    print(salesDate)
    print(unixSales)
    print(finalDatesCosts)



start = StringVar()
end = StringVar()

Label(root, text = 'Graph for Cashflow', font = ('Adam', 15)).place(relx = 0.35, rely = 0.6)
Label(root, text = 'Start Date', font = 'Adam').place(relx = 0.35, rely = 0.7)
CostsStartDate = Entry(root, textvariable = start).place(relx = 0.35, rely = 0.75)
Label(root, text = 'End Date', font = 'Adam').place(relx = 0.35, rely = 0.8)
CostsEndDate = Entry(root, textvariable = end).place(relx = 0.35, rely = 0.85)
Button(root, text = "Generate", font = "Adam", command = lambda: getBalanceSheet(str(start.get()), str(end.get()))).place(relx = 0.35, rely = 0.9)





root.mainloop()
