import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import MetaTrader5 as mt5
import json
import os
from dotenv import load_dotenv
from pandas_datareader import data as web

# Load environment variables
load_dotenv()

class Trading:
    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.server = server
        self.orders = {}

    def Login(self):
        if not mt5.initialize(login=self.username, server=self.server, password=self.password):
            print("initialize() failed, error code =", mt5.last_error())
            quit()
        authorized = mt5.login(self.username, password=self.password)
        if authorized:
            account_info = mt5.account_info()
            if account_info != None:
                # convert the dictionary into DataFrame and print
                account_info_dict = mt5.account_info()._asdict()
                df=pd.DataFrame(list(account_info_dict.items()), columns=['property','value'])
                print(df)
        else:
            print("Failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =", mt5.last_error()) 
            quit()
    

    def Check(self, lot, symbol):
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found.")
            mt5.shutdown()
            quit()   
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)
                mt5.shutdown()
                quit()


    def Buy(self, lot, symbol):
        trade.Check(lot, symbol)
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 100 * point,
            "tp": price + 100 * point,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict=result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field,result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field=="request":
                    traderequest_dict=result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
            print("shutdown() and quit")
            mt5.shutdown()
        else:
            self.orders[symbol] = result.order
        return



    def Sell(self, lot, symbol):
        trade.Check(lot, symbol)
        position_id = self.orders[symbol]
        price = mt5.symbol_info_tick(symbol).bid
        deviation=20
        request={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # send a trading request
        result=mt5.order_send(request)
        # check the execution result
        print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("4. order_send failed, retcode={}".format(result.retcode))
            print("   result",result)
        else:
            print("4. position #{} closed, {}".format(position_id,result))
            # request the result as a dictionary and display it element by element
            result_dict=result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field,result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field=="request":
                    traderequest_dict=result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        
        # shut down connection to the MetaTrader 5 terminal
        mt5.shutdown()
        return


# Load credentials from environment variables
username = int(os.getenv('MT5_USERNAME', '0'))
password = os.getenv('MT5_PASSWORD', '')
server = os.getenv('MT5_SERVER', '')

if username == 0 or not password or not server:
    print("Error: MT5 credentials not found in .env file")
    print("Please create a .env file with MT5_USERNAME, MT5_PASSWORD, and MT5_SERVER")
    quit()

try:
    with open('data/datadump.json') as json_file:
        data = json.load(json_file)
        print(data)
except:
    print("Could not open .json file")
quit()


# Main Loop
trade = Trading(username, password, server)
trade.Login()

trade.Buy(0.1, 'EURUSD')
trade.Sell(0.1, 'EURUSD')
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
