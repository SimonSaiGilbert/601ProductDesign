#Copyright Simon Gilbert 2020
#Help from https://gist.github.com/alexdeloy/fdb36ad251f70855d5d6

#Import some relevant libaries
import tweepy
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import warnings

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Need to run $ export GOOGLE_APPLICATION_CREDENTIALS="/Users/sgilbert/Desktop/SimonEC601Project2-b98f5c1852e5.json"

#Twitter API credentials
consumer_key = "Enter your consumer key"
consumer_secret = "Enter your consumer secret key"
access_key = "Enter your access key"
access_secret = "Enter your access secret key"


def smash_sentiment():
	#Twitter API credentials
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#Instantiate Google NLP client
	client = language.LanguageServiceClient()

	#Enter up to 8 players' twitter handles
	player_list = ["@LiquidHBox", "@TSM_Leffen", "@C9Mang0", "@TempoAxe", "@ZainNaghmi","@PG_Plup", "@iBDWSSBM", "@MVG_Mew2King"]
	# "@TrifSmash", "@SSBM_Faceroll", "@SSB_Swedish", "@ssbmhax", "@Legend0fLucky", "@SsbmGinger", "@SSBM_Spark", 
	#"@lloD74", "@LiquidChu", "@CLG_PewPewU","@aMSaRedyoshi"]

	#User input for date
	startinput = input("Enter the start date over which you'd like search <YYYYMMDD>: ")
	stringdate = startinput[4:6] + "/" + startinput[-2:] + "/" + startinput[0:4]
	startDate = datetime.datetime.strptime(startinput, '%Y%m%d')
	endDate = startDate
	endDate += datetime.timedelta(days=1)

	color_index = 0
	color_list = ["b", "g", "r", "c", "m", "y", "k", "darkorange"]

	sentiment_score_dict = {}
	sentiment_mag_dict = {}
	fig = plt.figure()
	
	for user in player_list:
		#Initialize lists for plotting
		tweets = []
		x_vals = []
		sentiment_score_dict[user] = []
		sentiment_mag_dict[user] = []

		#Get tweets in specified date range
		tmpTweets = api.user_timeline(user)
		for tweet in tmpTweets:
			if tweet.created_at < endDate and tweet.created_at > startDate and not tweet.retweeted and tweet.in_reply_to_status_id == None:
				tweets.append(tweet)
		while (tmpTweets[-1].created_at > startDate):
			#print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
			tmpTweets = api.user_timeline(user, max_id = tmpTweets[-1].id)
			for tweet in tmpTweets:
				if tweet.created_at < endDate and tweet.created_at > startDate and not tweet.retweeted and tweet.in_reply_to_status_id == None:
					tweets.append(tweet)
		print("Gathering tweets for %s"%user)

		#Perform sentiment analysis
		for tweet in tweets:
			print(tweet.created_at)
			text = tweet.text
			document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
			sentiment = client.analyze_sentiment(document=document).document_sentiment
			sentiment_score_dict[user].append(sentiment.score)
			sentiment_mag_dict[user].append(sentiment.magnitude)
			x_vals.append(tweet.created_at.hour + (1/60)*tweet.created_at.minute) #Scale time tweet was created for easier plotting

		#Plot sentiment of tweets over time
		#x_vals = range(len(sentiment_score_dict[user]))
		plt.scatter(x_vals, sentiment_score_dict[user], s=10, linewidth=0)
		plt.plot(x_vals, sentiment_score_dict[user], c=color_list[color_index])
		plt.ylim((-1,1))
		#col = np.where(np.array(sentiment_mag_dict[user])<0.5,'r', 'k')
		ax1 = fig.add_subplot(111)
		ax1.scatter(x_vals, sentiment_score_dict[user], c = color_list[color_index], label=user)
		ax1.set_xlabel('Hour')
		ax1.set_ylabel('Sentiment Score')
		ax1.set_title('Sentiment of Top Smasher Tweets on %s'%(stringdate))
		color_index += 1

	plt.legend(bbox_to_anchor=(1, 1), loc='upper left',fontsize='xx-small');
	plt.show()


	

if __name__ == '__main__':
	warnings.filterwarnings("ignore", category=UserWarning)
	smash_sentiment()
