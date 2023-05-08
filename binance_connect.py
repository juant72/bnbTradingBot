from binance.spot import Spot
from binance.client import Client
import pandas


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
    account_status=client.get_account()
    print(account_status)
    # if account_status==0:
    #     return True
    # else:
    #     raise ConnectionError


    # params = {        {"recvWindow": 10000}    }

    # print(client.get_account_status())

    # if status["status"] == 0:
    #     return True
    # else:
    #     raise ConnectionError


# query testnet
def query_testnet(api_key, secret_key):
    client = Spot(base_url="https://testnet.binance.vision")
    print(client.time())
