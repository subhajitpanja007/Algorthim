# Import necessary modules
import asyncio
import time
import json
import ssl
import upstox_client
import websockets
from google.protobuf.json_format import MessageToDict
from zipfile import ZipFile
import requests
import os
from csv import DictReader
import pandas as pd
import csv
from flask import Flask, request
import threading
import ast
import re
import helper_upstox as helper
import MarketDataFeed_pb2 as pb




FEED_ERROR = False

access_token = open("upstox_access_token.txt", 'r').read()
print(access_token)
instr_dir = './csvs'   #'./csvs" for mac
instr_token_dict = {}
instr_ltp_dict = {}

nf_expiry=helper.getNiftyExpiryDate()
bnf_expiry = helper.getBankNiftyExpiryDate()
fin_expiry = helper.getFinNiftyExpiryDate()

#Put all options in the beginning
symbolList1 = [
    'NSE_INDEX|Nifty 50',
    'NSE_INDEX|Nifty Bank',
    'NSE_INDEX|NIFTY MID SELECT',
    'NSE_INDEX|Nifty Fin Service',
]

app = Flask(__name__)

def get_ltp(api_version, configuration, instrument_key):
    api_instance = upstox_client.MarketQuoteApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.ltp(instrument_key, api_version)

    parsed = ast.literal_eval(str(api_response))

    return parsed

def get_market_data_feed_authorize(api_version, configuration):
    """Get authorization for market data feed."""
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    return api_response


def decode_protobuf(buffer):
    """Decode protobuf message."""
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response

def download_csv(url):
    r = requests.get(url, allow_redirects=True)

    if not os.path.isdir(instr_dir):
        os.mkdir(instr_dir)
    
    filepath = f"{instr_dir}/{url.split('/')[-1]}"

    open(filepath, 'wb').write(r.content)

def csv_process():
    global instr_token_dict

    download_csv("https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz")

    # open file in read mode
    df = pd.read_csv(f"{instr_dir}/complete.csv.gz", delimiter=",", quoting=csv.QUOTE_NONE)
    df.to_csv(f"{instr_dir}/temp.csv")

    with open(f"{instr_dir}/temp.csv", newline='') as csvfile:
        row_csv = csv.DictReader(csvfile, delimiter=',')
        for row in row_csv:
            if row['"tradingsymbol"'].replace('"', '') not in instr_token_dict:
                
                instr_token_dict[row['"tradingsymbol"'].replace('"', '')] = row['"instrument_key"'].replace('"', '')

async def fetch_market_data():
    global symbolList1

    """Fetch market data using WebSocket and print it."""
    csv_process()

    # Configure OAuth2 access token for authorization
    configuration = upstox_client.Configuration()

    api_version = '2.0'
    configuration.access_token = access_token

    nf_intExpiry = nf_expiry
    bnf_intExpiry = bnf_expiry
    fin_intExpiry = fin_expiry
    strikeList = []
    symbolList = []

    #NIFTY
    ltp = get_ltp(api_version, configuration, "NSE_INDEX|Nifty 50")
    a = float(ltp['data']['NSE_INDEX:Nifty 50']['last_price'])

    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)
        strikeList.append(strike+50)

    #Add CE
    for strike in strikeList:
        ltp_option = "NIFTY" + str(nf_intExpiry)+str(strike)+"CE"
        symbolList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "NIFTY" + str(nf_intExpiry)+str(strike)+"PE"
        symbolList.append(ltp_option)

    strikeList=[]

    #BANKNIFTY
    ltp = get_ltp(api_version, configuration, "NSE_INDEX|Nifty Bank")
    a = float(ltp['data']['NSE_INDEX:Nifty Bank']['last_price'])

    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)

    #Add CE
    for strike in strikeList:
        ltp_option = "BANKNIFTY" + str(bnf_intExpiry)+str(strike)+"CE"
        symbolList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "BANKNIFTY" + str(bnf_intExpiry)+str(strike)+"PE"
        symbolList.append(ltp_option)

    #FINNIFTY
    strikeList=[]
    ltp = get_ltp(api_version, configuration, "NSE_INDEX|Nifty Fin Service")
    a = float(ltp['data']['NSE_INDEX:Nifty Fin Service']['last_price'])

    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)
        strikeList.append(strike+50)

    #Add CE
    for strike in strikeList:
        ltp_option = "FINNIFTY" + str(fin_intExpiry)+str(strike)+"CE"
        symbolList.append(ltp_option)

    #Add PE
    for strike in strikeList:
        ltp_option = "FINNIFTY" + str(fin_intExpiry)+str(strike)+"PE"
        symbolList.append(ltp_option)


    symbolList = symbolList + symbolList1
    # symbolList = symbolList1
    print("BELOW IS THE COMPLETE INSTRUMENT LIST")
    print(symbolList)
    backup_symbolList = symbolList[:]
    count = 0

    for symbol in symbolList:
        opt_search = re.search(r"(\d{2})(\w{3})((\d+)|(\d+\.\d+))(CE|PE)", symbol)
        fut_search = re.search(r"(\d{2}\w{3})(FUT)", symbol)

        if opt_search or fut_search or symbol not in symbolList1:
            symbolList[count] = instr_token_dict[symbol]
        
        count += 1

    #print(instr_token_dict)
    print(symbolList)

    symbol_dict = dict(zip(symbolList, backup_symbolList))
    print(symbol_dict)

    ###### INPUTS END ######

    # Create default SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Get market data feed authorization
    response = get_market_data_feed_authorize(
        api_version, configuration)
    
    await connect_websocket(response, ssl_context, symbolList, symbol_dict)
    

async def connect_websocket(response, ssl_context, symbolList, symbol_dict):
    global FEED_ERROR
    while True:
        try:
            async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
                print('Connection established')

                await asyncio.sleep(1)  # Wait for 1 second

                # Data to be sent over the WebSocket
                data = {
                    "guid": "someguid",
                    "method": "sub",
                    "data": {
                        "mode": "full",
                        "instrumentKeys": symbolList
                    }
                }

                # Convert data to binary and send over WebSocket
                binary_data = json.dumps(data).encode('utf-8')
                await websocket.send(binary_data)

                # Set a timeout for receiving messages
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=60)
                        decoded_data = decode_protobuf(message)

                        # Convert the decoded data to a dictionary
                        data_dict = MessageToDict(decoded_data)

                        print(" Feeds Received = " ,  len(data_dict['feeds']) )
                        # for stock in instr_ltp_dict:
                        #     print(f"{symbol_dict[stock]}: {instr_ltp_dict[stock]}")
                        #     pass

                        #print("---------------------------------")

                        # Print the dictionary representation
                        for key in data_dict['feeds']:
                            try:
                                if data_dict['feeds'][key]['ff'].get('marketFF') is not None:
                                    instr_ltp_dict[key] = float(data_dict['feeds'][key]['ff']['marketFF']['ltpc']['ltp'])
                                else:
                                    instr_ltp_dict[key] = float(data_dict['feeds'][key]['ff']['indexFF']['ltpc']['ltp'])

                            except Exception as e:
                                print(e)

                    except asyncio.TimeoutError:
                        FEED_ERROR = True
                        print("ERROR No data received for 1 minutes, attempting to reconnect...")
                        raise

        except websockets.exceptions.ConnectionClosed as e:
            FEED_ERROR = True
            print(f" ERROR : WebSocket connection closed: {e}. Reconnecting...")
            raise


        except Exception as e:
            print(f"ERROR : An error occurred: {e}")
            FEED_ERROR = True
            raise



@app.route('/ltp')
def getLTP():
    global FEED_ERROR
    try:
        instrument = request.args.get('instrument')
        ltp = 0

        if FEED_ERROR == True:
            return {
                "ltp" : -1
            }
        else :
            print(instrument)

            if instr_token_dict.get(instrument) != None:
                ltp = instr_ltp_dict[instr_token_dict.get(instrument)]
            else:
                ltp = instr_ltp_dict[instrument]

            print("ltp:", ltp)
            
            return {
                "ltp": ltp
            }
    except Exception as e:
        return {
            "error": str(e)
        }

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4000)

def main():
    global FEED_ERROR
    print("Inside main()")
    t1 = threading.Thread(target=startServer)
    t1.start()

    while True:
        try:
            # Execute the function to fetch market data
            print(" STARTING FEED ")
            FEED_ERROR = False
            asyncio.run(fetch_market_data())
        except Exception as e:
            print("EXCEPTION : Exception while connection to socket->socket: %s\n" % e)
            print(" Waiting for 5 Seconds before trying to reconnect !!")
            time.sleep(5)

main()
