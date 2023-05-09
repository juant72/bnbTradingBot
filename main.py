import json
import os
import binance_connect
from dotenv import load_dotenv

import strategy

load_dotenv()

BINANCE_API_KEY=os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY=os.getenv('BINANCE_SECRET_KEY')

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

    ETH= project_settings["Tokens"]['ETH']
    BUSD= project_settings["Tokens"]['BUSD']
    BTCB= project_settings["Tokens"]['BTCB']


    # status = binance_connect.query_binance_status(api_key, secret_key)
    # print("Status: ",status)

    account = binance_connect.query_account(api_key, secret_key)
    # print("Account: ", account)
    #
    # testnet= binance_connect.query_testnet(api_key, secret_key)
    #
    # candles=binance_connect.get_candlestick_data("ETHBTC", "1h", 3)
    # print(candles)
    #
    # dataframe= binance_connect.query_quote_asset_list("BTC")
    # print("DataFrame: ", dataframe)

    if account["canTrade"]:
        print("Your account is ready to trade")

        #Calulate the current ratio
        reference_ratio = strategy.check_pair_relation(ETH, BTCB, "bsc")
        current_ratio = strategy.check_pair_relation(BUSD, BTCB, "bsc")

        print("Reference ratio: ", reference_ratio)
        print("Current ratio: ", current_ratio)

        #Calculate the difference between the ratios
        check = strategy.check_ratio_relation(current_ratio, reference_ratio)
        asset_list = binance_connect.query_quote_asset_list("BTC")
        eth_pair = asset_list.loc[asset_list["symbol"] == "ETHBTC"]
        symbol = eth_pair["symbol"].values[0]

        if check:
            print("Buying time")
            analysis= strategy.analyze_symbols(eth_pair, "1m", 0.000001, "buy")
            if analysis:
                print("Buying ETH")
                params=strategy.calculate_buy_params(symbol, eth_pair,"1h")
                response = binance_connect.make_trade_with_params(params)
                print("Response: ", response)
            else:
                print("Not buying ETH")
                print(f"Reason: The analysis is {analysis}")
        else:
            print("Selling time")
            analysis = strategy.analyze_symbols(eth_pair, "1h", 0.000001, "sell")
            if analysis:
                print("Selling ETH")
                params = strategy.calculate_buy_params(symbol, eth_pair, "1h")
                response = binance_connect.make_trade_with_params(params)
                print("Response: ", response)
            else:
                print("Not selling ETH")
                print(f"Reason: The analysis is {analysis}")










