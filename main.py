import json
import os

import binance

import binance_connect
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY=  os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY=  os.getenv('BINANCE_SECRET_KEY')

import_path="settings.json"

# import settings
def get_settings(import_path):
    # ensure thr path exists
    if os.path.exists(import_path):
        file = open(import_path, 'r')
        project_settings=json.load(file)
        file.close()
        return project_settings
    else:
        return ImportError

if __name__ =="__main__":
    project_settings = get_settings(import_path)

    api_key=BINANCE_API_KEY
    secret_key=BINANCE_SECRET_KEY

    status = binance_connect.query_binance_status(api_key, secret_key)
    print("Status: ",status)

    account = binance_connect.query_account(api_key, secret_key)
    print("Account: ", account)

    testnet= binance_connect.query_testnet(api_key, secret_key)

    candles=binance_connect.get_candlestick_data("ETHBTC", "1h", 3)
    print(candles)

    dataframe= binance_connect.query_quote_asset_list("BTC")
    print("DataFrame: ", dataframe)




