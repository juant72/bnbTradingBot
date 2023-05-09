import pandas
import numpy
import binance_connect
import time
import requests

# Functions to convert binance data into dataframes
def get_and_transform_data(symbol, timeframe, number_of_candles):
    raw_data = binance_connect.get_candlestick_data(
        symbol, timeframe, number_of_candles
    )

    df = pandas.DataFrame(raw_data)
    df["time"] = pandas.to_datetime(df["time"], unit="ms")
    df["close_time"] = pandas.to_datetime(df["close_time"], unit="ms")
    df["RedOrGreen"] = numpy.where((df["open"] < df["close"]), "Green", "Red")

    # return de data frame
    return df


# Get the token price
def get_token_price(address, chain):
    # Make API call to get the price
    url = f" http://127.0.0.1:5002/getPrice?chain={chain}&address={address}"
    response = requests.get(url)
    data = response.json()
    usd_price = data['usdPrice']
    return usd_price


# Check the pair relation between
def check_pair_relation(address1, address2, chain):
    price1 = get_token_price(address1, chain)
    price2 = get_token_price(address2, chain)
    ratio = price1 / price2
    print(f"Price 1: {price1}, Price 2: {price2} Ratio: {ratio}")
    return ratio


def check_ratio_relation(current_ratio, reference_ratio):
    # Calculate the difference between the ratios
    # ratio1= token1/token3
    # ratio2= token2/token3
    if current_ratio > reference_ratio:
        # The current ratio is overvalued relative to the reference ratio
        # Consider to sell Token1 for Token3
        return False
    elif current_ratio < reference_ratio:
        # The current ratio is undervalued relative to the reference ratio
        # Consider buying Token1 for Token3
        return True


# Function to determine the consecutive raise or decrease
def determine_trade_event(symbol, timeframe, percentage_change, candle_color):
    candlestick_data = get_and_transform_data(symbol, timeframe, 3)
    # Review if the candles has the same color
    print("Candle 1 color: " + candlestick_data.loc[0, "RedOrGreen"])
    print("Candle 2 color: " + candlestick_data.loc[1, "RedOrGreen"])
    print("Candle 3 color: " + candlestick_data.loc[2, "RedOrGreen"])

    print("Candle color desired: " + candle_color)

    if (
        candlestick_data.loc[0, "RedOrGreen"] == candle_color
        and candlestick_data.loc[1, "RedOrGreen"] == candle_color
        and candlestick_data.loc[2, "RedOrGreen"] == candle_color
    ):
        # Determine the percentage change
        change_one = determine_percent_change(
            candlestick_data.loc[0, "open"], candlestick_data.loc[0, "close"]
        )
        change_two = determine_percent_change(
            candlestick_data.loc[1, "open"], candlestick_data.loc[1, "close"]
        )
        change_three = determine_percent_change(
            candlestick_data.loc[2, "open"], candlestick_data.loc[2, "close"]
        )

        if candle_color == "Red":
            print(f"First Drop: {change_one}")
            print(f"Second Drop: {change_two}")
            print(f"Third Drop: {change_three}")
        elif candle_color == "Green":
            print(f"First Increase: {change_one}")
            print(f"Second Increase: {change_two}")
            print(f"Third Increase: {change_three}")

        # Compare the price changes agains stated percentage change

        # The minimun treshold of increase or decrease we want to see in the price
        # in order to make the sell/buy decision worth it
        if (
            change_one >= percentage_change
            and change_two >= percentage_change
            and change_three >= percentage_change
        ):
            # We can trade
            return True
        else:
            # We can't trade
            return False
    else:
        # We can't trade
        return False


def determine_percent_change(close_previous, close_current):
    return (close_current - close_previous) / close_previous


def analyze_symbols(symbol_dataframe, timeframe, percentage, type):
    # Iterate trough the symbols
    for index in symbol_dataframe.index:
        # Analyze symbol
        if type == "buy":
            analysis = determine_trade_event(
                symbol=symbol_dataframe["symbol"][index],
                timeframe=timeframe,
                percentage_change=percentage,
                candle_color="Green",
            )
            if analysis:
                print(f'{symbol_dataframe["symbol"][index]} has 3 consecutive rises')
            else:
                print(
                    f'{symbol_dataframe["symbol"][index]} does not have 3 consecutive rises'
                )
            # sleep 1 sec
            time.sleep(1)
            return analysis
        elif type == "sell":
            analysis = determine_trade_event(
                symbol=symbol_dataframe["symbol"][index],
                timeframe=timeframe,
                percentage_change=percentage,
                candle_color="Red",
            )
            if analysis:
                print(f'{symbol_dataframe["symbol"][index]} has 3 consecutive drops')
            else:
                print(
                    f'{symbol_dataframe["symbol"][index]} does not have 3 consecutive drops'
                )
            # sleep 1 sec
            time.sleep(1)
            return analysis


#Buying params function
def calculate_buy_params(symbol, pair, timeframe ):
    #Retrieve the candel data
    raw_data= binance_connect.get_candlestick_data(symbol,timeframe,1)
    #Determine the precision
    precision= pair.iloc[0]['baseAssetPrecision']
    #Filters
    filters= pair.iloc[0]['filters']
    for f in filters:
        if f['filterType']=="LOT_SIZE":
            step_size=float(f['stepSize'])
            min_qty=float(f['minQty'])
        elif f['filterType']=="PRICE_FILTER":
            tick_size=float(f['tickSize'])

    #Calculate the close price
    close_price=raw_data[0]['close']
    #Calculate the buy stop. This will be the 1% of the previous close price
    buy_stop=close_price *1.01
    #Round the buy stop price to the nearest valid tick size
    buy_stop= round(buy_stop / tick_size) * tick_size
    #Calculate the quantity. This will be the buy_Stop
    raw_quantity=0.1/buy_stop
    #Round
    quantity= max(min_qty, round(raw_quantity - (raw_quantity % step_size), precision ))
    params={
        "symbol": symbol,
        "side": "BUY",
        "type":"STOP_LOSS_LIMIT",
        "timeInForce":"GTC",
        "quantity": quantity,
        "price": buy_stop,
        "trailingDelta":100,
    }

    return params


#Selling params function
def calculate_sell_params(symbol, pair, timeframe ):
    #Retrieve the candel data
    raw_data= binance_connect.get_candlestick_data(symbol,timeframe,1)
    #Determine the precision
    precision= pair.iloc[0]['baseAssetPrecision']
    #Filters
    filters= pair.iloc[0]['filters']
    for f in filters:
        if f['filterType']=="LOT_SIZE":
            step_size=float(f['stepSize'])
            min_qty=float(f['minQty'])
        elif f['filterType']=="PRICE_FILTER":
            tick_size=float(f['tickSize'])

    #Calculate the close price
    close_price=raw_data[0]['close']
    #Calculate the buy stop. This will be the 0.99% of the previous close price
    sell_stop=close_price *0.99
    #Round the buy stop price to the nearest valid tick size
    sell_stop= round(sell_stop / tick_size) * tick_size
    #Calculate the quantity. This will be the buy_Stop
    raw_quantity=0.1/sell_stop
    #Round
    quantity= max(min_qty, round(raw_quantity - (raw_quantity % step_size), precision ))
    params={
        "symbol": symbol,
        "side": "SELL",
        "type":"STOP_LOSS_LIMIT",
        "timeInForce":"GTC",
        "quantity": quantity,
        "price": sell_stop,
        "trailingDelta":100,
    }

    return params






