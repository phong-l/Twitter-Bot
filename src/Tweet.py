import tweepy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)


# Builds tweet
def tweetBuilder(name, eth, usd, txid):
    message = "NFT Name: " + str(name) + " \n" + \
              "Ether price: " + str(eth) + " Ether " + "\n" + \
              "Estimated USD Price: $" + str(usd) + "\n" + \
              "Etherscan: " + str(txid) + "\n" + \
              "#NFT" + " #crypto" + " #opensea" + " #NFTCommunity"
    return message


# Create a tweet
def createTweet(message, url):
    request = requests.get(url, stream=True)
    content_type = request.headers['content-type']
    if 'svg' in content_type:
        filename = 'temp.svg'
    else:
        filename = 'temp.jpg'

    if request.status_code == 200:
        if 'svg' in filename:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            Image.svgtopng('temp.svg')
            filename = 'temp.png'
        else:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

        media = api.media_upload(filename)
        api.update_status(status=message, media_ids=[media.media_id])
        os.remove(filename)
        return message
    else:
        print("Unable to download image")


def getContentType(url):
    request = requests.get(url, stream=True)
    content_type = request.headers['content-type']
    return content_type
