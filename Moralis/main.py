from flask import Flask, request
from moralis import evm_api
from dotenv import load_dotenv
import datetime
import locale
import os

load_dotenv()

api_key= os.environ.get('MORALIS_API_KEY')

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
app = Flask(__name__)

@app.route('/getPrice', methods=["GET"])
def prices():
    address = request.args.get('address')
    chain= request.args.get('chain')
    params = {
        "chain": chain,
        "exchange": "pancakeswap-v2",
        "address": address
    }
    result = evm_api.token.get_token_price(
        api_key=api_key,
        params=params,
    )
    return result


if __name__ == '__main__':
    app.run(port=5002,debug=True)



