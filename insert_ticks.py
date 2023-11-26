import sqlite3
import logging
import datetime
import sys
from create_trade import CreateTrade
logging.basicConfig(filename="D:/Algo/Logging_Console.log", format='%(asctime)s %(message)s', filemode='w',
                        level=logging.DEBUG)
logger = logging.getLogger()



trade_initiated = False

class InsertTicks:
    def insert_ticks(kite, ticks, db):
        global trade_initiated
        c = db.cursor()
        logger.info("Insert ticks is executing successfully every second")
        for tick in ticks:
            try:
                tok = str(tick['instrument_token'])
                vals = [tick['exchange_timestamp'], tick['last_price'], tick['last_traded_quantity']]
                query = "INSERT INTO BANK_NIFTY_CE(ts,price,volume) VALUES (?,?,?)"
                c.execute(query, vals)
            except Exception as x:
                logger.info("Exception in inserting ticks"+ str(x))


        try:
            db.commit()
            now_update = datetime.datetime.now()
            # if (now_update.second == 0):
            #     logger.info("We are at minute interval now")
            if (not trade_initiated):
                CreateTrade.create_trade(ticks, now_update.second, db)
            else:
                CreateTrade.update_stopLoss(ticks, db)
        except Exeception as x:
            logger.info("Exception in trade update" + str(x))
            db.rollback()