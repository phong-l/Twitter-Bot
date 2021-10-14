import requests
import time
from src import Tweet


def query():
    url = "https://api.opensea.io/api/v1/events"
    querystring = {"event_type": "successful", "only_opensea": "false", "offset": "0", "limit": "200"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()['asset_events']

    return response


def getName(i):
    name = i['asset']['name']
    if name:
        name = name
    else:
        name = i['asset']['asset_contract']['name']

    return name


def getImageLink(i):
    image = i['asset']['image_url']
    if image != '':
        image = image
    else:
        image = i['asset']['asset_contract']['image_url']

    return image


def printData(name, eth, usd, txid, image):
    print("Name: ", name)
    print("ETH: ", eth)
    print("USD: $" + usd)
    print("TXID: ", txid)
    print("Image link: ", image)


def get_payment_token(i):
    payment_token = i['payment_token']
    if payment_token:
        symbol = payment_token['symbol']
        if symbol == 'ETH' or symbol == 'WETH':
            return True
    return False


def getData():
    link = "https://etherscan.io/tx/"
    while True:
        try:
            response = query()
            for i in response:
                eth = round(float(i['total_price']) * (10 ** -18), 2)
                payment_token = get_payment_token(i)
                tx = i['transaction']
                if tx:
                    hashid = tx['transaction_hash']
                    if eth > 5 and payment_token:
                        image = getImageLink(i)
                        contenttype = Tweet.getContentType(image)
                        if 'mp4' in contenttype:
                            continue
                        ethusd = round(float(i['payment_token']['usd_price']), 2)
                        usd = str(round(float(eth)*float(ethusd), 2))
                        txid = link + hashid
                        name = getName(i)
                        message = Tweet.tweetBuilder(name, eth, usd, txid)
                        printData(name, eth, usd, txid, image)
                        Tweet.createTweet(message, image)
            print("Ticking...")
            time.sleep(1200.0)
        except Exception as e:
            print("Error: ", e)


getData()
