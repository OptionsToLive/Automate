import datetime
import sys
import pandas as pd
import os
import sqlite3

db = sqlite3.connect('D:/Algo/ticks.db')

c = db.cursor()

for n in c.execute('SELECT name from sqlite_master where type= "table"'):
    print(n)
c.fetchall()

c.execute('''PRAGMA table_info(BANK_NIFTY_CE)''')
c.fetchall()

for m in c.execute('''SELECT * FROM TRADE_CE'''):
    print(m)