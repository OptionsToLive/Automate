# -*- coding: utf-8 -*-
"""
Zerodha Kite Connect - Storing tick level data in db
"""

from kiteconnect import KiteTicker, KiteConnect
import datetime
import sys
import pandas as pd
import os
import sqlite3
import logging

from insert_ticks import InsertTicks

cwd = os.chdir("D:\\Algo")


# generate log file
logging.basicConfig(filename="D:/Algo/Logging_Console.log", format='%(asctime)s %(message)s', filemode='w',
                        level=logging.DEBUG)
logger = logging.getLogger()
logger.info("Processing has been started")

# generate trading session
access_token = open("access_token.txt", 'r').read()
key_secret = open("api_key.txt", 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#initiating DB
db = sqlite3.connect('D:/Algo/ticks.db')

# get dump of all NSE instruments
instrument_dump = kite.instruments("NFO")
instrument_df = pd.DataFrame(instrument_dump)


def tokenLookup(instrument_df, symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    for symbol in symbol_list:
        if(symbol.__contains__('CE')):
            ce_token = int(instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0])
        else:
            pe_token = int(instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0])
        token_list.append(int(instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]))
    return token_list


#####################update ticker list######################################
tickers = ["NIFTY23N2319700CE", "NIFTY23N2319700PE"]
#############################################################################

# create KiteTicker object
kws = KiteTicker(key_secret[0], kite.access_token)
tokens = tokenLookup(instrument_df, tickers)

a=kite.ltp(260105)
print(a['260105']['last_price'])

def on_ticks(ws, ticks):
    insert_tick = InsertTicks.insert_ticks(kite, ticks, db)
    print(ticks)


def on_connect(ws, response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL, tokens)

prev_price = 0.0
stoploss_price = 0.0
entry_price = 0.0


while True:
    now = datetime.datetime.now()
    # if (now.hour >= 9 and now.minute >= 15):
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.connect()
    # if (now.hour >= 15 and now.minute >= 30):
    #     sys.exit()

db.close()

