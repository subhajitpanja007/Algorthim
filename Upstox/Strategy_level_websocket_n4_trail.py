#DISCLAIMER:
#1) This sample code is for learning purposes only.
#2) Always be very careful when dealing with codes in which you can place orders in your account.
#3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
#4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
#5) TFU and Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
#6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
#7) This is NOT a tip providing service/code.
#8) This is NOT a software. Its a tool that works as per the inputs given by you.
#9) Slippage is dependent on market conditions.
#10) Option trading and automatic API trading are subject to market risks



import time
import math
from datetime import datetime,timedelta
from pytz import timezone
import ta    # Python TA Lib
import pandas as pd
import pandas_ta as pta    # Pandas TA Libv
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def importLibrary():
    global shoonya_broker
    global nuvama_broker
    global icici_broker
    global angel_broker
    global alice_broker
    global fyers_broker
    global zerodha_broker
    global upstox_broker
    global helper
    global api_connect
    global breeze
    global alice
    global fyers
    global kc
    global api
    global xt
    global xt1

    if nuvama_broker == 1:
        import nuvama_login
        import helper_nuvama as helper
        api_connect = nuvama_login.api_connect

    if icici_broker == 1:
        import icici_login
        import helper_icici as helper
        breeze = icici_login.breeze

    if angel_broker == 1:
        import helper_angel as helper
        helper.login_trading()
        time.sleep(15)
        helper.login_historical()

    if alice_broker == 1:
        import alice_login
        import helper_alice as helper
        alice = alice_login.alice

    if fyers_broker == 1:
        from fyers_apiv3 import fyersModel
        import helper_fyers as helper
        app_id = open("fyers_client_id.txt",'r').read()
        access_token = open("fyers_access_token.txt",'r').read()
        fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=app_id)

    if shoonya_broker == 1:
        from NorenApi import NorenApi
        import helper_shoonya as helper
        api = NorenApi()
        api.token_setter()

    if zerodha_broker == 1:
        from kiteconnect import KiteTicker
        from kiteconnect import KiteConnect
        import helper_zerodha as helper
        apiKey = open("zerodha_api_key.txt",'r').read()
        accessToken = open("zerodha_access_token.txt",'r').read()
        kc = KiteConnect(api_key=apiKey)
        kc.set_access_token(accessToken)

    if upstox_broker == 1:
        import helper_upstox as helper

    if iifl_broker == 1:
        from Connect import XTSConnect
        import helper_iifl as helper
        """Dealer credentials"""
        with open('iifl_api_key.txt','r') as f:
            API_KEY = f.read()
        with open('iifl_secret_key.txt','r') as f:
            API_SECRET = f.read()
        with open('user_id.txt','r') as f:
            userID = f.read()
        XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
        source = "WEBAPI"

        """Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
        xt = XTSConnect(API_KEY, API_SECRET, source)

        """Using the xt object we created call the interactive login Request"""
        response = xt.interactive_login()
        print("Login: ", response)

        with open('iifl_market_api_key.txt','r') as f:
            API_KEY_M = f.read()
        with open('iifl_market_secret_key.txt','r') as f:
            API_SECRET_M = f.read()
        # Initialise
        xt1 = XTSConnect(API_KEY_M, API_SECRET_M, source)
        # Login for authorization token
        response = xt1.marketdata_login()
        print("Market Data: ", response)


#If you have any below brokers, then make it 1
shoonya_broker = 0
nuvama_broker = 0
icici_broker = 0
angel_broker = 0
alice_broker = 0
fyers_broker = 0
zerodha_broker = 0
upstox_broker = 0
iifl_broker = 1

importLibrary()

def findStrikePriceATM(stock, cepe):
    global tradePEoption
    global tradeCEoption
    global original_entry

    name = helper.getIndexSpot(stock)

    strikeList=[]
    prev_diff = 10000
    closest_Strike=10000

    if stock == "BANKNIFTY":
        intExpiry=helper.getBankNiftyExpiryDate()
    elif stock == "NIFTY":
        intExpiry=helper.getNiftyExpiryDate()
    elif stock == "FINNIFTY":
        intExpiry=helper.getFinNiftyExpiryDate()
    ######################################################
    #FINDING ATM
    ltp = helper.getLTP(name)

    if stock == "BANKNIFTY":
        closest_Strike = int(round((ltp / 100),0) * 100)
        print(closest_Strike)

    elif stock == "NIFTY" or stock == "FINNIFTY":
        closest_Strike = int(round((ltp / 50),0) * 50)
        print(closest_Strike)

    print("closest",closest_Strike)
    closest_Strike_CE = closest_Strike+otm
    closest_Strike_PE = closest_Strike-otm

    atmCE = helper.getOptionFormat(stock, intExpiry, closest_Strike_CE, "CE")
    atmPE = helper.getOptionFormat(stock, intExpiry, closest_Strike_PE, "PE")

    print(atmCE)
    print(atmPE)

    if (cepe == "CE"):
        #BUY AT MARKET PRICE
        print("In CE placeorder")
        oidentry = placeOrder1( atmCE, "BUY", qty, "MARKET", 0, "regular",papertrading)
        original_entry = helper.getLTP(atmCE)
        tradeCEoption = atmCE
        print("CE Entry OID: ", oidentry)
    else:
        #BUY AT MARKET PRICE
        print("In PE placeorder")
        oidentry = placeOrder1( atmPE, "BUY", qty, "MARKET", 0, "regular",papertrading)
        original_entry = helper.getLTP(atmPE)
        tradePEoption = atmPE
        print("PE Entry OID: ", oidentry)

    return oidentry

def exitPosition(tradeOption):
    global tradePEoption
    global tradeCEoption
    #Sell existing option
    oidentry = placeOrder1( tradeOption, "SELL", qty, "MARKET", 0, "regular",papertrading)
    print("Exit OID: ", oidentry)
    return oidentry

def placeOrder1(inst ,t_type,qty,order_type,price,variety, papertrading=0):
    global api_connect
    global breeze
    global fyers
    global api
    global kc
    global alice
    global xt
    global tradesDF
    global originalEntryPrice
    print("Trade taken. Symbol: ",inst, " Direction: ", t_type, " Quantity: ", qty)

    dt1 = datetime.now()
    tempLtp = helper.getLTP(inst)
    tradesDF.loc[len(tradesDF.index)] = [dt1, inst, t_type, tempLtp, qty, papertrading]
    #originalEntryPrice = tempLtp

    if papertrading == 0:
        return 0
    elif (nuvama_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, api_connect,papertrading)
    elif (icici_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, breeze,papertrading)
    elif (alice_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, alice,papertrading)
    elif (fyers_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,fyers, papertrading)
    elif (shoonya_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,api, papertrading)
    elif (zerodha_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,kc, papertrading)
    elif (iifl_broker == 1):
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety,xt, papertrading)
    else:
        return helper.placeOrder (inst ,t_type,qty,order_type,price,variety, papertrading)

def getHistorical1(ticker,interval,duration):
    global api_connect
    global breeze
    global fyers
    global kc
    global alice
    global api
    global xt
    global xt1
    if (nuvama_broker == 1):
        #THIS NEEDS TO BE UPDATED FOR STOCK/ETC
        #For index == INDEX, stock == EQUITY, future == FUTUREINDEX, option == OPTIONINDEX
        #optional_param1 = "INDEX", optional_param2 = api_connect
        return helper.getHistorical(ticker,interval,duration,"INDEX",api_connect)
    elif (icici_broker == 1):
        #optional_param1 = breeze
        return helper.getHistorical(ticker,interval,duration,breeze)
    elif (alice_broker == 1):
        #For index == INDEX, otherise == "NO"
        #optional_param1 = alice, optional_param2 = "INDEX"
        return helper.getHistorical(ticker,interval,duration,alice,"INDEX")
    elif (fyers_broker == 1):
        return helper.getHistorical(ticker,interval,duration,fyers)
    elif (shoonya_broker == 1):
        return helper.getHistorical(ticker,interval,duration,api)
    elif (zerodha_broker == 1):
        return helper.getHistorical(ticker,interval,duration,kc)
    elif (iifl_broker == 1):
        return helper.getHistorical(ticker,interval,duration,xt1)
    else:
        return helper.getHistorical(ticker,interval,duration)
####################__INPUT__#####################

entryHour   = 9
entryMinute = 25
entrySecond = 0
startTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, entryHour, entryMinute, entrySecond)
startTime = startTime.time()
print(startTime)

tradeOption = 1
stock = "NIFTY"

if tradeOption == 1:
    checkInstrument = helper.getIndexSpot(stock)
else:
    checkInstrument = stock
timeFrame = 1
otm = 100  #If you put -100, that means its 100 points ITM.
SL_percentage = 0.02
target_percentage = 0.4
qty = 50
papertrading = 0   #If paper trading is 0, then paper trading will be done. If paper trading is 1, then live trade
tradeCEoption = ""
tradePEoption = ""
originalEntryPrice = 0
for_every_x_point = 1
trail_by_y_point = 1

# order's details dataframe
tradesDF = pd.DataFrame(columns=["Date", "Symbol", "Direction", "Price", "Qty", "PaperTrading"])

x = 1
close=[]
opens=[]
high=[]
low=[]
volume = []

st=0
#0 means no trde, but want to enter.
# 1 means buy trade.
# 2 means sell trade.
# -1 no trade and dont want to enter.

upperLevel = 21800
lowerLevel = 19900
maxtrade = 4
number_of_trade = 0

while x == 1:
    dt1 = datetime.now()

    #keep checking if entry time is reached
    if (dt1.time() >= startTime):
        print("time reached")
        x = 2
    else:
        time.sleep(1)
        print(dt1 , " Waiting for Time to check new ATM ")

while x == 2:
    dt1 = datetime.now()

    if st == 0 :
        ltp = helper.getLTP(checkInstrument)
        print(ltp)
        print("upperLevel", upperLevel)
        print("lowerLevel", lowerLevel)

        #check entry at the close of the candle
        if ltp>upperLevel and number_of_trade < maxtrade:
            print('Upper Level Broken')
            sl=float(ltp)*(1-SL_percentage/100)
            target=float(ltp)*(1+target_percentage/100)
            print("sl", sl, "target", target)
            st=1
            originalEntryPrice = ltp
            if tradeOption == 1:
                oidentry = findStrikePriceATM(stock, "CE")
            else:
                oidentry = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
            number_of_trade = number_of_trade  + 1

        elif ltp<lowerLevel and number_of_trade < maxtrade:
            print('Lower Level Broken')
            sl=float(ltp)*(1+SL_percentage/100)
            target=float(ltp)*(1-target_percentage/100)
            st=2
            originalEntryPrice = ltp
            if tradeOption == 1:
                oidentry = findStrikePriceATM(stock, "PE")
            else:
                oidentry = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
            number_of_trade = number_of_trade  + 1

        else:
            print("No Entry Yet. Current Second", dt1.second)
            time.sleep(0.5)

    #IN BUY TRADE
    elif st==1 :
        ltp = helper.getLTP(checkInstrument)
        print("ltp", ltp)

        if ltp<=sl:
            print('SL Hit')
            st=0
            if tradeOption == 1:
                oidexit = exitPosition(tradeCEoption)
            else:
                oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
        elif ltp>=target:
            print('Target hit')
            st=-1
            if tradeOption == 1:
                oidexit = exitPosition(tradeCEoption)
            else:
                oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
        else:
            print("In Buy Trade. No Exit Yet. Current Second", dt1.second)
            time.sleep(0.5)

        #Trailing
        if ltp > originalEntryPrice + for_every_x_point:
            originalEntryPrice = originalEntryPrice + for_every_x_point
            sl = sl + trail_by_y_point


    #IN SELL TRADE
    elif st==2 :
        ltp = helper.getLTP(checkInstrument)
        if ltp>=sl:
            print('SL Hit')
            st=0
            if tradeOption == 1:
                oidexit = exitPosition(tradePEoption)
            else:
                oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
        elif ltp<=target:
            print('Target hit')
            st=-1
            if tradeOption == 1:
                oidexit = exitPosition(tradePEoption)
            else:
                oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
        else:
            print("In Sell Trade. No Exit Yet. Current Second", dt1.second)
            time.sleep(0.5)

        #Trailing
        if ltp < originalEntryPrice - for_every_x_point:
            originalEntryPrice = originalEntryPrice - for_every_x_point
            sl = sl - trail_by_y_point

    else:
        print("No Entry Yet", dt1.second)
        time.sleep(0.5)

    #TIME EXIT
    if (dt1.hour >= 15 and dt1.minute >= 15):
        if st==2 :
            print("EOD Exit")
            #Exit Position
            if tradeOption == 1:
                oidexit = exitPosition(tradePEoption)
            else:
                oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
        elif st==1 :
            print("EOD Exit")
            #Exit position
            if tradeOption == 1:
                oidexit = exitPosition(tradeCEoption)
            else:
                oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
        print('End Of the Day')
        x = 3
        break


#------------Saving the final lists in csv file------------------
tradesDF.to_csv("template_level.csv")


