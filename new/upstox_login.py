from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint
import urllib.parse
import pandas as pd
import requests
import sys

step = 2
step = int(step)

def main():

    client_id = ""
    client_secret = ""

    redirect_uri = 'https://www.google.com' # str | 
    api_version = '2.0' # str | API Version Header
    grant_type = 'authorization_code'
    parse_url = urllib.parse.quote(redirect_uri, safe="")

    if step == 1:
        uri = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
        print(uri)

    elif step == 2:
        uri = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
        print(uri)
        code = input("Please put code and press enter: ")
        token_url = "https://api-v2.upstox.com/login/authorization/token"
        headers = {
            'accept': 'application/json',
            'Api-Version': api_version,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }

        response = requests.post(token_url, headers=headers, data=data)
        json_response = response.json()
        
        print(json_response)
        print()
        print("Copy this:", json_response['access_token'])
        with open("upstox_access_token.txt", 'w') as file:
            file.write(json_response['access_token'])

if __name__ == "__main__":
    main()