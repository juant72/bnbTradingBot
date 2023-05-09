from binance.spot import Spot
from binance.client import Client
import pandas

from main import BINANCE_API_KEY, BINANCE_SECRET_KEY


# Function to get the status
def query_binance_status(api_key, secret_key):
    client = Client(api_key, secret_key)
    status = client.get_system_status()
    if status["status"] == 0:
        return True
    else:
        raise ConnectionError


# Function query account
def query_account(api_key, api_secret):
    # client = Client(api_key, secret_key)
    # status = client.get_account_status()
    print("APIKEY: ", api_key)
    print("SecretKEY: ", api_secret)

    # client = Client(api_key, api_secret)
    client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
    return client.get_account()


# query testnet
def query_testnet(api_key, secret_key):
    client = Spot(base_url="https://testnet.binance.vision")
    print(client.time())

def get_candlestick_data(symbol, timeframe, qty ):
    #get raw data from binance
    raw_data=Spot().klines(symbol=symbol,interval=timeframe,limit=qty)
    converted_data=[]

    for candle in raw_data:
        converted_candle={
            "time": candle[0],
            "opem": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
            "close_time":candle[6],
            "quote_asset_volume": float(candle[7]),
            "number_of_trades": float(candle[8]),
            "taker_buy_asset_volume": float(candle[9]),
            "taker_buy_quote_asset_volume": float(candle[10]),
        }

        converted_data.append(converted_candle)

    return converted_data

# Function to query all symbols from a base asset
def query_quote_asset_list(quote_asset_symbol):
    symbol_dictionary = Spot().exchange_info()
    #convert this info into a dataframe
    symbol_dataframe= pandas.DataFrame(symbol_dictionary["symbols"])
    #extract all the symbols with the base asset pair
    quote_symbol_dataframe= symbol_dataframe.loc[
        symbol_dataframe["quoteAsset"] == quote_asset_symbol
    ]
    quote_symbol_dataframe = symbol_dataframe.loc[
        symbol_dataframe["status"] == "TRADING"
    ]
    return quote_symbol_dataframe

# Function to make a trade with parameters
def make_trade_with_params(params):
    print("Making a trade with params")
    #Set API
    api_key=BINANCE_API_KEY
    secret_key=BINANCE_SECRET_KEY

    #Create client
    client =Spot(
        api_key=api_key,
        secret_key=secret_key,
        base_url="https://testnet.binance.vsion",
    )

    #Make the trade
    try:
        response = client.new_order(**params)
        return response
    except ConnectionRefusedError as error:
        print("Error: ", error)

# Function to query open trades
def query_open_trades():
    #set de API keys
    api_key=BINANCE_API_KEY
    secret_key=BINANCE_SECRET_KEY

    #Create client
    client = Spot(
        api_key=api_key,
        secret_key=secret_key,
        base_url="https://testnet.binance.vsion",
    )

    #get Trades
    try:
        response=client.get_open_orders()
        return response
    except ConnectionRefusedError as error:
        print("Error: ",error)

# Function to cancel a trade
def cancel_prder_by_symbol(symbol ):
    #set de API keys
    api_key=BINANCE_API_KEY
    secret_key=BINANCE_SECRET_KEY

    #Create client
    client = Spot(
        api_key=api_key,
        secret_key=secret_key,
        base_url="https://testnet.binance.vsion",
    )
    #cancel trades
    try:
        response=client.cancel_open_orders(symbol=symbol)
        return response
    except ConnectionRefusedError as error:
        print("Error: ",error)


# Function to palce a limit order for symbol
def place_limit_order(symbol, side, quantity, price):
    # Set the API Key
    api_key = BINANCE_API_KEY
    # Set the secret key
    secret_key = BINANCE_SECRET_KEY
    # Setup the client
    client = Spot(
        key=api_key, secret=secret_key, base_url="https://testnet.binance.vision"
    )

    # Place the limit order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Found error {error}")


def place_stop_loss_order(
    symbol, side, quantity, stop_price, limit_price
):
    # Set the API Key
    api_key = BINANCE_API_KEY
    # Set the secret key
    secret_key = BINANCE_SECRET_KEY
    # Setup the client
    client = Spot(
        key=api_key, secret=secret_key, base_url="https://testnet.binance.vision"
    )

    # Place the stop loss order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            stopPrice=stop_price,
            price=limit_price,
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Found error {error}")


def place_take_profit_order(
    symbol, side, quantity, stop_price, limit_price
):
    # Set the API Key
    api_key = BINANCE_API_KEY
    # Set the secret key
    secret_key = BINANCE_SECRET_KEY
    # Setup the client
    client = Spot(
        key=api_key, secret=secret_key, base_url="https://testnet.binance.vision"
    )

    # Place the take profit order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT_LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            stopPrice=stop_price,
            price=limit_price,
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Found error {error}")


