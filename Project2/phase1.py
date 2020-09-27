#Import some relevant libaries
import tweepy
import json
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import matplotlib.pyplot as plt

#Twitter API credentials
consumer_key = "Enter your consumer key"
consumer_secret = "Enter your consumer secret key"
access_key = "Enter your access key"
access_secret = "Enter your access secret key"

def avg_favs_and_sentiment():
	#Twitter API credentials
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#Instantiate Google NLP client
	client = language.LanguageServiceClient()

	#Inputs for twitter handle and number of tweets to analyze 
	screen_name = "@" + input("Enter the handle of the user you'd like to analyze: @")
	num_tweets = int(input("Enter the number of tweets over which you'd like to average: "))

	#Get tweets
	new_tweets = api.user_timeline(screen_name=screen_name, count=num_tweets) 

	#initialize variables
	avg_fav = 0
	avg_sentiment_score = 0
	avg_sentiment_magnitude = 0

	#compute averages
	for tweet in new_tweets:
		avg_fav += tweet.favorite_count
		text = tweet.text
		#print(text)
		document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
		sentiment = client.analyze_sentiment(document=document).document_sentiment
		avg_sentiment_score += sentiment.score
		avg_sentiment_magnitude += sentiment.magnitude

	print("The average number of favorites over %d tweets is %d"%(num_tweets, avg_fav/num_tweets))
	print('The average sentiment score and magnitude are: {}, {}'.format(avg_sentiment_score/num_tweets, avg_sentiment_magnitude/num_tweets))

if __name__ == '__main__':
    avg_favs_and_sentiment()
