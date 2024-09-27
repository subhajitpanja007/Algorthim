# DISCLAIMER:
# 1) This sample code is for learning purposes only.
# 2) Always be very careful when dealing with codes in which you can place orders in your account.
# 3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
# 4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
# 5) TFU and Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
# 6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
# 7) This is NOT a tip providing service/code.
# 8) This is NOT a software. Its a tool that works as per the inputs given by you.
# 9) Slippage is dependent on market conditions.
# 10) Option trading and automatic API trading are subject to market risks

import datetime
import time
import pandas as pd
import requests

#################### __INPUT__#####################
# TIME TO FIND THE STRIKE
entryHour = 9
entryMinute = 30
entrySecond = 0
startTime = datetime.time(entryHour, entryMinute, entrySecond)

stock = "NIFTY"  # BANKNIFTY OR NIFTY OR FINNIFTY
otm = 100  # If you put -100, that means its 100 points ITM.
SL_point = 10
target_point = 20
SL_percentage = 5
target_percentage = 10
for_every_x_point = 1
trail_by_y_point = 1
PnL = 0
premium = 80
df = pd.DataFrame(columns=['Date', 'CE_Entry_Price',
                  'CE_Exit_Price', 'PE_Entry_Price', 'PE_Exit_Price', 'PnL'])
df["Date"] = [datetime.date.today()]
qty = 50
papertrading = 0  # If paper trading is 0, then paper trading will be done. If paper trading is 1, then live trade

# If you have any below brokers, then make it 1
shoonya_broker = 0
nuvama_broker = 0
icici_broker = 0
angel_broker = 0
alice_broker = 0
fyers_broker = 0
zerodha_broker = 0
upstox_broker = 1
iifl_broker = 0

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
    app_id = open("fyers_client_id.txt", 'r').read()
    access_token = open("fyers_access_token.txt", 'r').read()
    fyers = fyersModel.FyersModel(
        token=access_token, is_async=False, client_id=app_id)

if shoonya_broker == 1:
    from NorenApi import NorenApi
    import helper_shoonya as helper
    api = NorenApi()
    api.token_setter()

if zerodha_broker == 1:
    from kiteconnect import KiteTicker
    from kiteconnect import KiteConnect
    import helper_zerodha as helper
    apiKey = open("zerodha_api_key.txt", 'r').read()
    accessToken = open("zerodha_access_token.txt", 'r').read()
    kc = KiteConnect(api_key=apiKey)
    kc.set_access_token(accessToken)

if upstox_broker == 1:
    import helper_upstox as helper

if iifl_broker == 1:
    from Connect import XTSConnect
    import helper_iifl as helper
    """Dealer credentials"""
    with open('iifl_api_key.txt', 'r') as f:
        API_KEY = f.read()
    with open('iifl_secret_key.txt', 'r') as f:
        API_SECRET = f.read()
    with open('user_id.txt', 'r') as f:
        userID = f.read()
    XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
    source = "WEBAPI"

    """Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
    xt = XTSConnect(API_KEY, API_SECRET, source)

    """Using the xt object we created call the interactive login Request"""
    response = xt.interactive_login()
    print("Login: ", response)
##################################################


def findStrikePriceATM():
    name = helper.getIndexSpot(stock)

    strikeList = []
    prev_diff = 10000
    closest_Strike = 10000

    if stock == "BANKNIFTY":
        intExpiry = helper.getBankNiftyExpiryDate()
    elif stock == "NIFTY":
        intExpiry = helper.getNiftyExpiryDate()
    elif stock == "FINNIFTY":
        intExpiry = helper.getFinNiftyExpiryDate()

    ######################################################
    # FINDING ATM
    ltp = helper.getLTP(name)
    print(ltp)

    if stock == "BANKNIFTY":
        closest_Strike = int(round((ltp / 100), 0) * 100)
        print(closest_Strike)

    elif stock == "NIFTY" or stock == "FINNIFTY":
        # 22519.4/50 = 450.388 = 450 = 22500
        closest_Strike = int(round((ltp / 50), 0) * 50)
        print(closest_Strike)

        quit()

    print("closest", closest_Strike)
    closest_Strike_CE = closest_Strike+otm
    closest_Strike_PE = closest_Strike-otm

    atmCE = helper.getOptionFormat(stock, intExpiry, closest_Strike_CE, "CE")
    atmPE = helper.getOptionFormat(stock, intExpiry, closest_Strike_PE, "PE")

    print(atmCE)
    print(atmPE)

    takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE)


def findStrikePricePremium():
    name = helper.getIndexSpot(stock)

    strikeList = []
    prev_diff = 10000
    closest_Strike = 10000

    if stock == "BANKNIFTY":
        intExpiry = helper.getBankNiftyExpiryDate()
    elif stock == "NIFTY":
        intExpiry = helper.getNiftyExpiryDate()
    elif stock == "FINNIFTY":
        intExpiry = helper.getFinNiftyExpiryDate()

    ######################################################
    # FINDING ATM
    ltp = helper.getLTP(name)

    if stock == "BANKNIFTY":
        for i in range(-8, 8):
            strike = (int(ltp / 100) + i) * 100
            strikeList.append(strike)
        print(strikeList)
    elif stock == "NIFTY" or stock == "FINNIFTY":
        for i in range(-5, 6):
            strike = (int(ltp / 100) + i) * 100  # 220+1 = 22100
            strikeList.append(strike)
            strikeList.append(strike+50)
        print(strikeList)

    # FOR CE
    prev_diff = 10000
    for strike in strikeList:
        ltp_option = findManualPrice(
            helper.getOptionFormat(stock, intExpiry, strike, "CE"))
        print(ltp_option)
        diff = abs(ltp_option - premium)
        print("diff==>", diff)
        if (diff < prev_diff):
            closest_Strike_CE = strike
            prev_diff = diff

    # FOR PE
    prev_diff = 10000
    for strike in strikeList:
        ltp_option = findManualPrice(
            helper.getOptionFormat(stock, intExpiry, strike, "PE"))
        diff = abs(ltp_option - premium)
        print("diff==>", diff)
        if (diff < prev_diff):
            closest_Strike_PE = strike
            prev_diff = diff

    print("closest CE", closest_Strike_CE)
    print("closest PE", closest_Strike_PE)

    atmCE = helper.getOptionFormat(stock, intExpiry, closest_Strike_CE, "CE")
    atmPE = helper.getOptionFormat(stock, intExpiry, closest_Strike_PE, "PE")

    print(atmCE)
    print(atmPE)

    takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE)


def takeEntry(closest_Strike_CE, closest_Strike_PE, atmCE, atmPE):
    global PnL
    ce_entry_price = helper.getLTP(atmCE)
    pe_entry_price = helper.getLTP(atmPE)
    PnL = ce_entry_price + pe_entry_price
    print("Current PnL is: ", PnL)
    df['CE_Entry_Price'] = [ce_entry_price]
    df['PE_Entry_Price'] = [pe_entry_price]

    print(" closest_CE ATM ", closest_Strike_CE,
          " CE Entry Price = ", ce_entry_price)
    print(" closest_PE ATM", closest_Strike_PE,
          " PE Entry Price = ", pe_entry_price)

    # ceSL = round(ce_entry_price + SL_point, 1)
    # peSL = round(pe_entry_price + SL_point, 1)
    # ceTarget = round(ce_entry_price - target_point, 1)
    # peTarget = round(pe_entry_price - target_point, 1)
    # 150 x (1.1) = 165
    ceSL = round(ce_entry_price * (1 + SL_percentage / 100), 1)
    peSL = round(pe_entry_price * (1 + SL_percentage / 100), 1)
    ceTarget = round(ce_entry_price * (1 - target_percentage / 100), 1)
    peTarget = round(pe_entry_price * (1 - target_percentage / 100), 1)

    print("Placing Order CE Entry Price = ", ce_entry_price,
          "|  CE SL => ", ceSL, "| CE Target => ", ceTarget)
    print("Placing Order PE Entry Price = ", pe_entry_price,
          "|  PE SL => ", peSL, "| PE Target => ", peTarget)

    # SELL AT MARKET PRICE
    oidentryCE = placeOrder1(atmCE, "SELL", qty, "MARKET",
                             ce_entry_price, "regular", papertrading)
    oidentryPE = placeOrder1(atmPE, "SELL", qty, "MARKET",
                             pe_entry_price, "regular", papertrading)

    print("The OID of Entry CE is: ", oidentryCE)
    print("The OID of Entry PE is: ", oidentryPE)

    exitPosition(atmCE, ceSL, ceTarget, ce_entry_price,
                 atmPE, peSL, peTarget, pe_entry_price, qty)


def exitPosition(atmCE, ceSL, ceTarget, ce_entry_price, atmPE, peSL, peTarget, pe_entry_price, qty):
    global PnL
    traded = "No"
    originalEntryCE = ce_entry_price
    originalEntryPE = pe_entry_price
    while traded == "No":
        dt = datetime.datetime.now()
        try:
            ltp = helper.getLTP(atmCE)
            ltp1 = helper.getLTP(atmPE)
            # This is for call
            if ((ltp > ceSL) or (ltp < ceTarget) or (dt.hour >= 15 and dt.minute >= 10)) and ltp != -1:
                oidexitCE = placeOrder1(
                    atmCE, "BUY", qty, "MARKET", ceSL, "regular", papertrading)
                PnL = PnL - ltp
                print("Current PnL is: ", PnL)
                df["CE_Exit_Price"] = [ltp]
                print("The OID of Exit CE is: ", oidexitCE)
                traded = "CE"

            # THis is for put
            elif ((ltp1 > peSL) or (ltp1 < peTarget) or (dt.hour >= 15 and dt.minute >= 10)) and ltp1 != -1:
                oidexitPE = placeOrder1(
                    atmPE, "BUY", qty, "MARKET", peSL, "regular", papertrading)
                PnL = PnL - ltp1
                print("Current PnL is: ", PnL)
                df["PE_Exit_Price"] = [ltp1]
                print("The OID of Exit PE is: ", oidexitPE)
                traded = "PE"
            else:
                print("NO SL is hit: ", "CE LTP: ", ltp, "PE LTP: ", ltp1)
                time.sleep(1)

            # trail SL
            # entry 100. sl = 120. every 2 points, 1 point. LTP = 98. SL = 119
            if ltp < originalEntryCE - for_every_x_point:
                originalEntryCE = originalEntryCE - for_every_x_point  # 98
                ceSL = ceSL - trail_by_y_point  # 119

            if ltp1 < originalEntryPE - for_every_x_point:
                originalEntryPE = originalEntryPE - for_every_x_point
                peSL = peSL - trail_by_y_point

        except:
            print(" ")
            time.sleep(1)

    if (traded == "CE"):
        peSL = pe_entry_price
        while traded == "CE":
            dt = datetime.datetime.now()
            try:
                ltp = helper.getLTP(atmPE)
                if ((ltp > peSL) or (ltp < peTarget) or (dt.hour >= 15 and dt.minute >= 15)) and ltp != -1:
                    oidexitPE = placeOrder1(
                        atmPE, "BUY", qty, "MARKET", peSL, "regular", papertrading)
                    PnL = PnL - ltp
                    print("Current PnL is: ", PnL)
                    df["PE_Exit_Price"] = [ltp]
                    print("The OID of Exit PE is: ", oidexitPE)
                    traded = "Close"
                else:
                    print("PE SL not hit. ", "PE LTP: ", ltp)
                    time.sleep(1)

            except:
                print(" ")
                time.sleep(1)

    elif (traded == "PE"):
        ceSL = ce_entry_price
        while traded == "PE":
            dt = datetime.datetime.now()
            try:
                ltp = helper.getLTP(atmCE)
                if ((ltp > ceSL) or (ltp < ceTarget) or (dt.hour >= 15 and dt.minute >= 15)) and ltp != -1:
                    oidexitCE = placeOrder1(
                        atmCE, "BUY", qty, "MARKET", ceSL, "regular", papertrading)
                    PnL = PnL - ltp
                    df["CE_Exit_Price"] = [ltp]
                    print("Current PnL is: ", PnL)
                    print("The OID of Exit CE is: ", oidexitCE)
                    traded = "Close"
                else:
                    print("CE SL not hit. ", "CE LTP: ", ltp)
                    time.sleep(1)
            except:
                print(" ")
                time.sleep(1)

    if (traded == "Close"):
        print("All trades done. Exiting Code")


def placeOrder1(inst, t_type, qty, order_type, price, variety, papertrading=0):
    global api_connect
    global breeze
    global fyers
    global api
    global kc
    global alice
    global xt
    if papertrading == 0:
        return 0
    elif (nuvama_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, api_connect, papertrading)
    elif (icici_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, breeze, papertrading)
    elif (alice_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, alice, papertrading)
    elif (fyers_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, fyers, papertrading)
    elif (shoonya_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, api, papertrading)
    elif (zerodha_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, kc, papertrading)
    elif (iifl_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, xt, papertrading)
    else:
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, papertrading)


def findManualPrice(symbol):
    global api_connect
    global breeze
    global fyers
    global api
    global kc
    global alice
    global xt
    if (zerodha_broker == 1):
        return helper.manualLTP(symbol, kc)
    elif (shoonya_broker == 1):
        return helper.manualLTP(symbol, api)
    elif (icici_broker == 1):
        return helper.manualLTP(symbol, breeze)
    elif (fyers_broker == 1):
        return helper.manualLTP(symbol, fyers)
    elif (alice_broker == 1):
        return helper.manualLTP(symbol, alice)
    elif (angel_broker == 1):
        return helper.manualLTP(symbol)
    elif (nuvama_broker == 1):
        return helper.getLTP(symbol)
    elif (iifl_broker == 1):
        return helper.manualLTP(symbol, xt)
    else:
        return helper.manualLTP(symbol)


def checkTime_tofindStrike():
    x = 1
    while x == 1:
        dt = datetime.datetime.now()
        # if( dt.hour >= entryHour and dt.minute >= entryMinute and dt.second >= entrySecond ):
        if (dt.time() >= startTime):
            print("time reached")
            x = 2
            findStrikePriceATM()
        else:
            time.sleep(1)
            print(dt, " Waiting for Time to check new ATM ")


checkTime_tofindStrike()
df["PnL"] = [PnL]

df.to_csv('template_options.csv', mode='a', index=True, header=True)
