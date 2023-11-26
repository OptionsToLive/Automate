import logging

logging.basicConfig(filename="D:/Algo/Logging_Console.log", format='%(asctime)s %(message)s', filemode='w',
                        level=logging.DEBUG)
logger = logging.getLogger()

priceValuesSec = {}


class CreateTrade:
    def create_trade(ticks, sec, db):
        logger.info("Checking if eligible trade is identified"+str(ticks[0]))

        global priceValuesSec
        c = db.cursor()

        curr_price = 0
        prev_price = 0
        price_diff = 0

        for tick in ticks:
            try:
                curr_price = tick['last_price']
                try:
                    prev_price = priceValuesSec[sec]
                except:
                    priceValuesSec[sec] = curr_price # initially no val present in dictionary hence assign curr price for this second

                price_diff = curr_price - prev_price

                # We are worried only when price is increasedby 10 percent in last 60 seconds, not concernedif it is decreased
                if(price_diff > 0):
                    perc_change = price_diff/curr_price*100

                logger.info("percentage difference claculated"+str(perc_change))

                if(prev_price != 0 and perc_change > 10):
                    logger.info("we finally found trade with stop loss"+str(prev_price)+". We are entering into trade at "+str(curr_price))
                    entry_price = curr_price
                    stoploss_price = prev_price
                    tok = str(tick['instrument_token'])
                    vals = [tick['exchange_timestamp'], tick['last_price'], tick['last_traded_quantity'],prev_price,tok]
                    query = "INSERT INTO TRADE_CE(ts,price,volume,sl,token) VALUES (?,?,?,?,?)"
                    logger.info("chc 1")
                    try:
                        c.execute(query, vals)
                    except Exception as x:
                        print(x)

                    logger.info("chc 2")
                    trade_initiated = True
                    logger.info("changing trade_initiated variable to true")
                elif(prev_price == 0):
                    logger.info("still in the initial phase")
                else:
                    logger.info("sorry. there was no opportunity. cuur price is"+str(curr_price)+"updating the previous price with this")
                    priceValuesSec[sec] = curr_price
            except:
                logger.info("Exception occured in create_trade")
        try:
            db.commit()
        except:
            db.rollback()


    def update_stopLoss(ticks, db):
        logger.info("Trade is already active at tick" + ticks[0] + ". Hence we entered stoploss function")
        global prev_price
        global stoploss_price
        for tick in ticks:
            try:
                curr_price = tick['last_price']
                price_diff = prev_price-curr_price
                if(curr_price == stoploss_price):
                    logger.info("We had hit stoploss. Exit the trade"+str(curr_price))
                    trade_initiated = False
                elif (curr_price > entry_price*1.25):
                    logger.info("We had reached target. Exit the trade at "+str(curr_price))
                else:
                    logger.info("Let us update the stoploss")

                    tok = "FINALIZED" + str(tick['instrument_token'])
                    vals = [tick['exchange_timestamp'], tick['last_price'], tick['last_traded_quantity'],stoploss_price]
                    query = "INSERT INTO {}(ts,price,volume, sl) VALUES (?,?,?,?)".format(tok)
                    c.execute(query, vals)

                    stoploss_price = curr_price
                    logger.info("Keep updating Stoploss to previous price"+str(stoploss_price))
            except:
                logger.info("Exception occured in update_stoploss")
        try:
            db.commit()
        except:
            db.rollback()