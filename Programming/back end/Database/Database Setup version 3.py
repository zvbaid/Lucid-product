#database setup

import sqlite3 as sq
dbFin = sq.connect('Clients and Receipts.db')
c = dbFin.cursor()

# Create Table - Client Info, using client_id
c.execute('''CREATE TABLE IF NOT EXISTS CLIENTS
             ([client_id] INTEGER PRIMARY KEY AUTOINCREMENT,
             [Client_Name] text,
             [Username] text,
             [Password] text)''')

#Create Table for sales made using foreign key client_id

c.execute('''CREATE TABLE IF NOT EXISTS SALES_MADE
            ([client_id] INTEGER,
            [Sale_ID] INTEGER PRIMARY KEY AUTOINCREMENT,
            [Date_Of_Sale] text,
            [unix_date_sales] REAL,
            [Revenue] REAL,
            [ItemSold] text,
            CONSTRAINT fk_client
            FOREIGN KEY (client_id) REFERENCES CLIENTS(client_id))''')

# create Table Receipts using client_id as a foreign key
# use receipt_id as a primary key and autoincrement 

c.execute('''CREATE TABLE IF NOT EXISTS RECEIPTS
            ([client_id] INTEGER,
            [receipt_id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [total_price] REAL,
            [place_of_purchase] text,
            [Date_of_Purchase] text,
            [unix_date_purchase] REAL,
            CONSTRAINT fk_client
            FOREIGN KEY(client_id) REFERENCES CLIENTS(client_id))''')

#create table for item use item_id as a primary key
#use receipt_id as a foreign key to set up a link

c.execute('''CREATE TABLE IF NOT EXISTS ITEM(
            [receipt_id] INTEGER,
            [item_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [item_purchased] text,
            [item_price] REAL,
            CONSTRAINT fk_client
            FOREIGN KEY(receipt_id) REFERENCES RECEIPTS(receipt_id))''')

#below table will be the one where the user will be able to see


#when adding the data just take the columns that exist and place it into the other tables

dbFin.commit()
