#database setup

import sqlite3 as sq
dbFin = sq.connect('Clients and Receipts.db')
c = dbFin.cursor()

# Create Table - Client Info
c.execute('''CREATE TABLE IF NOT EXISTS CLIENTS
             ([client_id] INTEGER PRIMARY KEY AUTOINCREMENT,
             [Client_Name] text,
             [Username] text,
             [Password] text)''')

#Create Table for sales made using foreign key

c.execute('''CREATE TABLE IF NOT EXISTS SALES_MADE
            ([client_id] INTEGER,
            [Sale_ID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [Date_Of_Sale] date,
            [Revenue] REAL,
            [ItemSold] text,
            CONSTRAINT fk_client
            FOREIGN KEY (client_id) REFERENCES CLIENTS(client_id))''')

# create the rest of the tables using foreign keys

c.execute('''CREATE TABLE IF NOT EXISTS RECEIPTS
            ([client_id] INTEGER,
            [receipt_id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [date_purchased] date,
            [total_price] REAL,
            [item_price] REAL,
            [contact_info] text,
            [item_purchased] text,
            [payment_method] text,
            [item_id] INTEGER,
            UNIQUE(client_id, item_id)
            CONSTRAINT fk_client
            FOREIGN KEY(client_id) REFERENCES CLIENTS(client_id))''')
#create table for item

c.execute('''CREATE TABLE IF NOT EXISTS ITEM(
            [item_id] INTEGER, 
            [item_purchased] text,
            [receipt_id] INTEGER,
            [item_price] REAL)''')

#below table will be the one where the user will be able to see

c.execute('''CREATE TABLE IF NOT EXISTS SCANNED_RECEIPT_DATA(
            [receipt_id] INTEGER,
            [item_id] INTEGER,
            [date_purchased] date,
            [item_purchased] text,
            [total_price] REAL,
            [item_price] REAL)''')


#when adding the data just take the columns that exist and place it into the other tables

dbFin.commit()
