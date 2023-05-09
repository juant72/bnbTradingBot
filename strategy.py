import pandas
import numpy
import binance_connect
import time
import requests



#Functions to convert binance data into dataframes
def get_and_transform_data(symbol, timeframe, number_of_candles):
    raw_data = binance_connect.get_candlestick_data(
        symbol, timeframe, number_of_candles
    )

    df = pandas.DataFrame(raw_data)
    df['time'] =pandas.to_datetime(df['time'], unit='ms')
    df['close_time'] = pandas.to_datetime(df['close_time'], unit='ms')
    df['RedOrGreen'] = numpy.where(  (df['open'] < df['close']), "Green","Red")

    return df

# Get the token price
def get_token_price(address, chain ):
    #Make API call to get the price
    url=f" http://127.0.0.1:5002/getPrice?chain={chain}&address={address}"
    response = requests.get(url)
    data=response.json()
    usd_price = data['usdPrice']
    return usd_price

#Check the pair relation between
def check_pair_relation(address1, address2,chain):
    price1=get_token_price(address1,chain)
    price2=get_token_price(address2,chain)
    ratio= price1/price2

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






