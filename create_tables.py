import sqlite3
import logging


logging.basicConfig(filename="D:/Algo/Logging_Console.log", format='%(asctime)s %(message)s', filemode='a',
                        level=logging.DEBUG)
logger = logging.getLogger()

db = sqlite3.connect('D:/Algo/ticks.db')


def create_tables():

    c = db.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS BANK_NIFTY_CE (ts datetime primary key,price real(15,5), volume integer, token integer)")

    c.execute(
        "CREATE TABLE IF NOT EXISTS BANK_NIFTY_PE (ts datetime primary key,price real(15,5), volume integer, token integer)")

    c.execute(
        "CREATE TABLE IF NOT EXISTS TRADE_CE (ts datetime primary key,price real(15,5), volume integer, sl real(15,5), token integer)")

    c.execute(
        "CREATE TABLE IF NOT EXISTS TRADE_PE (ts datetime primary key,price real(15,5), volume integer, sl real(15,5)), token integer")

    try:
        db.commit()
        logger.info("Bank Nifty Tables have been created successfully")
    except:
        db.rollback()

create_tables()