#database setup

import sqlite3 as sq
dbFin = sq.connect('Clients and Receipts.db')
c = dbFin.cursor()

# Create Table - Client Info
c.execute('''CREATE TABLE CLIENTS
             ([client_id] INTEGER PRIMARY KEY,
             [Client_Name] text,
             [Username] text,
             [Password] text)''')

#Create Table for sales made using foreign key

c.execute('''CREATE TABLE SALES_MADE
            ([client_id] REFERENCES CLIENTS(client_id),
            [Sale_ID] INTEGER,
            [Date_Of_Sale] date,
            [Revenue] REAL,
            [ItemSold] text)''')

# create the rest of the tables using foreign keys

c.execute('''CREATE TABLE RECEIPTS
            ([client_id] REFERENCES CLIENTS (client_id),
            [receipt_id] INTEGER,
            [date_of_purchase] date,
            [total_price] REAL,
            [item_price] REAL,
            [contact_info] text,
            [item_purchased] text,
            [payment_method] text,
            [item_id] INTEGER)''')

#create table for item

c.execute('''CREATE TABLE ITEM
            ([item_id] REFERENCES RECEIPTS(item_id),
            [item_purchased] REFERENCES RECEIPTS(item_purchased),
            [receipt_id]REFERENCES RECEIPTS(receipt_id),
            [item_price]REFERENCES RECEIPTS(item_price))''')

#below table will be the one where the user will be able to see

c.execute('''CREATE TABLE SCANNED_RECEIPT_DATA
            ([receipt_id] REFERENCES ITEM(receipt_id),
            [item_id] REFERENCES ITEM(item_id),
            [date_purchased] REFERENCES RECEIPTS(date_purchased),
            [item_purchased] REFERENCES ITEM(item_purchased),
            [item_price] REFERENCES ITEM(item_price),
            [total_price] REFERENCES RECEIPTS(total_price))''')

dbFin.commit()
