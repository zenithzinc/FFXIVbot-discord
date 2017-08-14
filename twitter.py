import tweepy
import json

keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()

auth = tweepy.OAuthHandler(key["consumer_key"], key["consumer_secret"])
auth.set_access_token(key["access_token"], key["access_token_secret"])
api = tweepy.API(auth)


def tweet_now(content):
    try:
        api.update_status(content)
    except:
        pass
