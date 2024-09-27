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

from __future__ import print_function
import datetime
import time
import requests
from datetime import timedelta
from pytz import timezone
import pandas as pd
import gzip
from io import BytesIO
import upstox_client
from upstox_client.rest import ApiException
import ast

######PIVOT POINTS##########################
####################__INPUT__#####################
access_token = open("upstox_access_token.txt", 'r').read()
gzipped_file_url  = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
# Download the gzipped file from the URL
response = requests.get(gzipped_file_url)
gzipped_content = BytesIO(response.content)

with gzip.open(gzipped_content, 'rb') as f:
    df2 = pd.read_csv(f)
    #df2.to_csv('111.csv')

def getNiftyExpiryDate():
    nifty_expiry = {
        datetime.datetime(2023, 11, 16).date(): "23N16",
        datetime.datetime(2023, 11, 23).date(): "23N23",
        datetime.datetime(2023, 11, 30).date(): "23NOV",
        datetime.datetime(2023, 12, 7).date(): "23D07",
        datetime.datetime(2023, 12, 14).date(): "23D14",
        datetime.datetime(2023, 12, 21).date(): "23D21",
        datetime.datetime(2023, 12, 28).date(): "23DEC",
        datetime.datetime(2024, 1, 4).date(): "24104",
        datetime.datetime(2024, 1, 11).date(): "24111",
        datetime.datetime(2024, 1, 18).date(): "24118",
        datetime.datetime(2024, 1, 25).date(): "24JAN",
        datetime.datetime(2024, 2, 1).date(): "24201",
        datetime.datetime(2024, 2, 8).date(): "24208",
        datetime.datetime(2024, 2, 15).date(): "24215",
        datetime.datetime(2024, 2, 22).date(): "24222",
        datetime.datetime(2024, 2, 29).date(): "24FEB",
        datetime.datetime(2024, 3, 7).date(): "24307",
        datetime.datetime(2024, 3, 14).date(): "24314",
        datetime.datetime(2024, 3, 21).date(): "24321",
        datetime.datetime(2024, 3, 28).date(): "24MAR",
        datetime.datetime(2024, 4, 4).date(): "24404",
        datetime.datetime(2024, 4, 10).date(): "24410",
        datetime.datetime(2024, 4, 18).date(): "24418",
        datetime.datetime(2024, 4, 25).date(): "24APR",
        datetime.datetime(2024, 5, 2).date(): "24502",
        datetime.datetime(2024, 5, 9).date(): "24509",
        datetime.datetime(2024, 5, 16).date(): "24516",
        datetime.datetime(2024, 5, 23).date(): "24523",
        datetime.datetime(2024, 5, 30).date(): "24MAY",
        datetime.datetime(2024, 6, 6).date(): "24606",
        datetime.datetime(2024, 6, 13).date(): "24613",
        datetime.datetime(2024, 6, 20).date(): "24620",
        datetime.datetime(2024, 6, 27).date(): "24JUN",
        datetime.datetime(2024, 7, 4).date(): "24704",
        datetime.datetime(2024, 7, 11).date(): "24711",
        datetime.datetime(2024, 7, 18).date(): "24718",
        datetime.datetime(2024, 7, 25).date(): "24JUL",
        datetime.datetime(2024, 8, 1).date(): "24801",
        datetime.datetime(2024, 8, 8).date(): "24808",
        datetime.datetime(2024, 8, 14).date(): "24814",
        datetime.datetime(2024, 8, 22).date(): "24822",
        datetime.datetime(2024, 8, 29).date(): "24AUG",
        datetime.datetime(2024, 9, 5).date(): "24905",
        datetime.datetime(2024, 9, 12).date(): "24912",
        datetime.datetime(2024, 9, 19).date(): "24919",
        datetime.datetime(2024, 9, 26).date(): "24SEP",
        datetime.datetime(2024, 10, 3).date(): "24O03",
        datetime.datetime(2024, 10, 10).date(): "24O10",
        datetime.datetime(2024, 10, 17).date(): "24O17",
        datetime.datetime(2024, 10, 24).date(): "24O24",
        datetime.datetime(2024, 10, 31).date(): "24OCT",
        datetime.datetime(2024, 11, 7).date(): "24N07",
        datetime.datetime(2024, 11, 14).date(): "24N14",
        datetime.datetime(2024, 11, 21).date(): "24N21",
        datetime.datetime(2024, 11, 28).date(): "24NOV",
        datetime.datetime(2024, 12, 5).date(): "24D05",
        datetime.datetime(2024, 12, 12).date(): "24D12",
        datetime.datetime(2024, 12, 19).date(): "24D19",
        datetime.datetime(2024, 12, 26).date(): "24DEC",
    }

    today = datetime.datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value

def getBankNiftyExpiryDate():
    banknifty_expiry = {
        datetime.datetime(2023, 11, 15).date(): "23N15",
        datetime.datetime(2023, 11, 22).date(): "23N22",
        datetime.datetime(2023, 11, 30).date(): "23NOV",
        datetime.datetime(2023, 12, 6).date(): "23D06",
        datetime.datetime(2023, 12, 13).date(): "23D13",
        datetime.datetime(2023, 12, 20).date(): "23D20",
        datetime.datetime(2023, 12, 28).date(): "23DEC",
        datetime.datetime(2024, 1, 3).date(): "24103",
        datetime.datetime(2024, 1, 10).date(): "24110",
        datetime.datetime(2024, 1, 17).date(): "24117",
        datetime.datetime(2024, 1, 25).date(): "24JAN",
        datetime.datetime(2024, 1, 31).date(): "24131",
        datetime.datetime(2024, 2, 7).date(): "24207",
        datetime.datetime(2024, 2, 14).date(): "24214",
        datetime.datetime(2024, 2, 21).date(): "24221",
        datetime.datetime(2024, 2, 29).date(): "24FEB",
        datetime.datetime(2024, 3, 6).date(): "24306",
        datetime.datetime(2024, 3, 13).date(): "24313",
        datetime.datetime(2024, 3, 20).date(): "24320",
        datetime.datetime(2024, 3, 27).date(): "24MAR",
        datetime.datetime(2024, 4, 3).date(): "24403",
        datetime.datetime(2024, 4, 10).date(): "24410",
        datetime.datetime(2024, 4, 16).date(): "24416",
        datetime.datetime(2024, 4, 24).date(): "24APR",
        datetime.datetime(2024, 4, 30).date(): "24430",
        datetime.datetime(2024, 5, 8).date(): "24508",
        datetime.datetime(2024, 5, 15).date(): "24515",
        datetime.datetime(2024, 5, 22).date(): "24522",
        datetime.datetime(2024, 5, 29).date(): "24MAY",
        datetime.datetime(2024, 6, 5).date(): "24605",
        datetime.datetime(2024, 6, 12).date(): "24612",
        datetime.datetime(2024, 6, 19).date(): "24619",
        datetime.datetime(2024, 6, 26).date(): "24JUN",
        datetime.datetime(2024, 7, 3).date(): "24703",
        datetime.datetime(2024, 7, 10).date(): "24710",
        datetime.datetime(2024, 7, 16).date(): "24716",
        datetime.datetime(2024, 7, 24).date(): "24724",
        datetime.datetime(2024, 7, 31).date(): "24JUL",
        datetime.datetime(2024, 8, 7).date(): "24807",
        datetime.datetime(2024, 8, 14).date(): "24814",
        datetime.datetime(2024, 8, 21).date(): "24821",
        datetime.datetime(2024, 8, 28).date(): "24AUG",
        datetime.datetime(2024, 9, 4).date(): "24904",
        datetime.datetime(2024, 9, 11).date(): "24911",
        datetime.datetime(2024, 9, 18).date(): "24918",
        datetime.datetime(2024, 9, 25).date(): "24SEP",
        datetime.datetime(2024, 10, 1).date(): "24O01",
        datetime.datetime(2024, 10, 9).date(): "24O09",
        datetime.datetime(2024, 10, 16).date(): "24O16",
        datetime.datetime(2024, 10, 23).date(): "24O23",
        datetime.datetime(2024, 10, 30).date(): "24OCT",
        datetime.datetime(2024, 11, 6).date(): "24N06",
        datetime.datetime(2024, 11, 13).date(): "24N13",
        datetime.datetime(2024, 11, 20).date(): "24N20",
        datetime.datetime(2024, 11, 27).date(): "24NOV",
        datetime.datetime(2024, 12, 4).date(): "24D04",
        datetime.datetime(2024, 12, 11).date(): "24D11",
        datetime.datetime(2024, 12, 18).date(): "24D18",
        datetime.datetime(2024, 12, 24).date(): "24DEC",
    }

    today = datetime.datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getFinNiftyExpiryDate():
    finnifty_expiry = {
        datetime.datetime(2024, 2, 20).date(): "24220",
        datetime.datetime(2024, 2, 27).date(): "24FEB",
        datetime.datetime(2024, 3, 5).date(): "24305",
        datetime.datetime(2024, 3, 12).date(): "24312",
        datetime.datetime(2024, 3, 19).date(): "24319",
        datetime.datetime(2024, 3, 26).date(): "24MAR",
        datetime.datetime(2024, 4, 2).date(): "24402",
        datetime.datetime(2024, 4, 9).date(): "24409",
        datetime.datetime(2024, 4, 16).date(): "24416",
        datetime.datetime(2024, 4, 23).date(): "24423",
        datetime.datetime(2024, 4, 30).date(): "24APR",
        datetime.datetime(2024, 5, 7).date(): "24507",
        datetime.datetime(2024, 5, 14).date(): "24514",
        datetime.datetime(2024, 5, 21).date(): "24521",
        datetime.datetime(2024, 5, 28).date(): "24MAY",
        datetime.datetime(2024, 6, 4).date(): "24604",
        datetime.datetime(2024, 6, 11).date(): "24611",
        datetime.datetime(2024, 6, 18).date(): "24618",
        datetime.datetime(2024, 6, 25).date(): "24JUN",
        datetime.datetime(2024, 7, 2).date(): "24702",
        datetime.datetime(2024, 7, 9).date(): "24709",
        datetime.datetime(2024, 7, 16).date(): "24716",
        datetime.datetime(2024, 7, 23).date(): "24723",
        datetime.datetime(2024, 7, 30).date(): "24JUL",
        datetime.datetime(2024, 8, 6).date(): "24806",
        datetime.datetime(2024, 8, 13).date(): "24813",
        datetime.datetime(2024, 8, 20).date(): "24820",
        datetime.datetime(2024, 8, 27).date(): "24AUG",
        datetime.datetime(2024, 9, 3).date(): "24903",
        datetime.datetime(2024, 9, 10).date(): "24910",
        datetime.datetime(2024, 9, 17).date(): "24917",
        datetime.datetime(2024, 9, 24).date(): "24SEP",
        datetime.datetime(2024, 10, 1).date(): "24O01",
        datetime.datetime(2024, 10, 8).date(): "24O08",
        datetime.datetime(2024, 10, 15).date(): "24O15",
        datetime.datetime(2024, 10, 22).date(): "24O22",
        datetime.datetime(2024, 10, 29).date(): "24OCT",
        datetime.datetime(2024, 11, 5).date(): "24N05",
        datetime.datetime(2024, 11, 12).date(): "24N12",
        datetime.datetime(2024, 11, 19).date(): "24N19",
        datetime.datetime(2024, 11, 26).date(): "24NOV",
        datetime.datetime(2024, 12, 3).date(): "24D03",
        datetime.datetime(2024, 12, 10).date(): "24D10",
        datetime.datetime(2024, 12, 17).date(): "24D17",
        datetime.datetime(2024, 12, 24).date(): "24D24",
        datetime.datetime(2024, 12, 31).date(): "24DEC",
    }

    today = datetime.datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getExpiryFormat(year, month, day, monthly):
    if monthly == 0:
        day1 = day
        if month == "JAN":
            month1 = 1
        elif month == "FEB":
            month1 = 2
        elif month == "MAR":
            month1 = 3
        elif month == "APR":
            month1 = 4
        elif month == "MAY":
            month1 = 5
        elif month == "JUN":
            month1 = 6
        elif month == "JUL":
            month1 = 7
        elif month == "AUG":
            month1 = 8
        elif month == "SEP":
            month1 = 9
        elif month == "OCT":
            month1 = "O"
        elif month == "NOV":
            month1 = "N"
        elif month == "DEC":
            month1 = "D"
    elif monthly == 1:
        day1 = ""
        month1 = month

    return str(year)+str(month1)+str(day1)

def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "Nifty Bank"
    elif stock == "NIFTY":
        name = "Nifty 50"
    elif stock == "FINNIFTY":
        name = "Nifty Fin Service"

    return name

def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return str(stock) + str(intExpiry)+str(strike)+str(ce_pe)

def getLTP(instrument):
    print(instrument)
    token = df2[df2['tradingsymbol'] == instrument]['instrument_key']
    token2 = df2[df2['name'] == instrument]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    url = "http://localhost:4000/ltp?instrument=" + instrument_key

    try:
        resp = requests.get(url)
        resp2 = (resp.json())
        resp3 = resp2['ltp']
    except Exception as e:
        print(e)
    data = resp3
    return data

def manualLTP(symbol):
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token
    # create an instance of the API class
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

    token = df2[df2['tradingsymbol'] == symbol]['instrument_key']
    token2 = df2[df2['name'] == symbol]['instrument_key']
    ex = df2[df2['tradingsymbol'] == symbol]['exchange']
    ex2 = df2[df2['name'] == symbol]['exchange']

    if not token.empty:
        instrument_key = token.values[0]
        ex = ex.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]
        ex = ex2.values[0]

    try:
        # Market quotes and instruments - LTP quotes.
        api_response = api_instance.ltp(instrument_key, api_version)
        #print(api_response)
        api_response_str = str(api_response)
        #print(api_response_str)
        my_dict = ast.literal_eval(api_response_str)
        print(my_dict)
        symb = ex + ":" + symbol
        last_price = my_dict['data'][symb]['last_price']
        return(float(last_price))
    except ApiException as e:
        print("Exception when calling MarketQuoteApi->ltp: %s\n" % e)

def placeOrder(inst ,t_type,qty,order_type,price,variety, papertrading=0):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    instrument_key = df2[df2['tradingsymbol'] == inst]['instrument_key'].values[0]

    #papertrading = 1 #if this is 1, then real trades will be placed
    dt = datetime.datetime.now()

    if order_type == "MARKET":
        price = 0

    try:
        if (papertrading == 1):
            order_details = {
                "quantity": qty,
                "product": "I",
                "validity": "DAY",
                "price": price,
                "tag": "string",
                "instrument_token": instrument_key,
                "order_type": order_type,
                "transaction_type": t_type,
                "disclosed_quantity": 0,
                "trigger_price": price,
                "is_amo": False
            }

            api_instance = upstox_client.OrderApi(
                upstox_client.ApiClient(configuration))
            api_response = api_instance.place_order(order_details, api_version)
            print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , api_response.data.order_id)
            return api_response.data.order_id
        else:
            return 0

    except Exception as e:
        print(dt.hour,":",dt.minute,":",dt.second ," => ", inst , "Failed : {} ".format(e))

def getHistorical(ticker,interval,duration):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    token = df2[df2['tradingsymbol'] == ticker]['instrument_key']
    token2 = df2[df2['name'] == ticker]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    if interval == 1:
        interval_str = "1minute"
    elif interval == 30:
        interval_str = "30minute"

    interval_str = "1minute"
    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    duration1 = timedelta(days=int(duration))
    from_date = datetime.datetime.now() - duration1
    from_date_str = from_date.strftime("%Y-%m-%d")
    print(from_date_str)

    #getting historical data
    try:
        # Historical candle data
        api_instance = upstox_client.HistoryApi()
        api_response = api_instance.get_historical_candle_data1(instrument_key, interval_str, to_date, from_date_str, api_version)
        #print(api_response)
        candles_data = api_response.data.candles

        # Define column names
        column_names = ["date", "open", "high", "low", "close", "volume", "openinterest"]

        # Create a DataFrame with the specified column names
        df = pd.DataFrame(candles_data, columns=column_names)
        df['datetime2'] = df['date'].copy()
        df.set_index("date",inplace=True)
        #print(df)

    except ApiException as e:
        print("Exception when calling HistoryApi->get_historical_candle_data1: %s\n" % e)

    #getting intraday data
    try:
        # Intra day candle data
        api_response = api_instance.get_intra_day_candle_data(instrument_key, interval_str, api_version)
        #pprint(api_response)
        candles_data = api_response.data.candles

        # Create a DataFrame with the specified column names
        df3 = pd.DataFrame(candles_data, columns=column_names)
        df3['datetime2'] = df3['date'].copy()
        df3.set_index("date",inplace=True)
        #print(df3)
    except ApiException as e:
        print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)

    merged_df = pd.concat([df3, df], ignore_index=False)
    # Convert the index to datetime explicitly
    merged_df.index = pd.to_datetime(merged_df.index)
    sorted_df = merged_df.sort_index(ascending=True)
    #finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval)  + "min"
    elif interval == 375:
        finaltimeframe = "D"

    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = sorted_df.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first'
    })

    # If you want to fill any missing values with a specific method, you can use fillna
    #resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    #print(resampled_df)
    resampled_df = resampled_df.dropna(subset=['open'])

    return(resampled_df)

def getHistorical_old(ticker,interval,duration):
    # Configure OAuth2 access token for authorization: OAUTH2
    #https://upstox.com/developer/api-documentation/#tag/Order/operation/placeOrder
    configuration = upstox_client.Configuration()
    api_version = '2.0'
    # Login and authorization
    configuration.access_token = access_token

    token = df2[df2['tradingsymbol'] == ticker]['instrument_key']
    token2 = df2[df2['name'] == ticker]['instrument_key']

    if not token.empty:
        instrument_key = token.values[0]
    elif not token2.empty:
        instrument_key = token2.values[0]

    if interval == 1:
        interval_str = "1minute"
    elif interval == 30:
        interval_str = "30minute"

    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    duration1 = timedelta(days=int(duration))
    from_date = datetime.datetime.now() - duration1
    from_date_str = from_date.strftime("%Y-%m-%d")
    print(from_date_str)

    #getting historical data
    try:
        # Historical candle data
        api_instance = upstox_client.HistoryApi()
        api_response = api_instance.get_historical_candle_data1(instrument_key, interval_str, to_date, from_date_str, api_version)
        #print(api_response)
        candles_data = api_response.data.candles

        # Define column names
        column_names = ["date", "open", "high", "low", "close", "volume", "oi"]

        # Create a DataFrame with the specified column names
        df = pd.DataFrame(candles_data, columns=column_names)
        df.set_index("date",inplace=True)
        #print(df)

    except ApiException as e:
        print("Exception when calling HistoryApi->get_historical_candle_data1: %s\n" % e)

    #getting intraday data
    try:
        # Intra day candle data
        api_response = api_instance.get_intra_day_candle_data(instrument_key, interval_str, api_version)
        #pprint(api_response)
        candles_data = api_response.data.candles

        # Create a DataFrame with the specified column names
        df3 = pd.DataFrame(candles_data, columns=column_names)
        df3.set_index("date",inplace=True)
        #print(df3)
    except ApiException as e:
        print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)

    merged_df = pd.concat([df3, df], ignore_index=False)
    sorted_df = merged_df.sort_index(ascending=True)
    #print(merged_df)
    return(sorted_df)