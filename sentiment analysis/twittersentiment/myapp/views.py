from asyncio import as_completed
from django.shortcuts import render
from django.http import *
from myapp.forms import *

from matplotlib import pyplot as plt
import io
import urllib,base64


# Create your views here.
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'xk42lFFyawVxdeUn4QSFY5g6f'
		consumer_secret = 'zN1tWQczobMymerJl4ImVHoGkIhPRHCVUcXSLFiGGpbnJdmUnI'
		access_token = '1533815356564746245-Tgajd8GzuhM0weTfMvzGVP2GgxAxfs'
		access_token_secret='QljwLpknD8xvO4O0lfmhlWfuZQu97JXktEQAsltvzCoJD'
		

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token,access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except AttributeError:
			# print error (if any)
			print("Error")

def show(request):
 form= TwitterForm()
 return render(request,'index.html',{'ff':form})

def prediction(request):
    arr_pred=[]
    if request.method == 'POST':
        # creating object of TwitterClient Class
        api=TwitterClient()
        t = request.POST['word']
        tweets = api.get_tweets(query =t, count = 200)
        # percentage of positive tweets
        ptweets= [tweet for tweet in tweets if tweet['sentiment'] == 'positive']        
        pos="Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))
        # percentage of negative tweets	
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        neg="Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))
        # percentage of neutral tweets      
        neu="Neutral tweets percentage: {} % ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))
        posper= 100*len(ptweets)/len(tweets)
        negper= 100*len(ntweets)/len(tweets)
        neuper=100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)
        maxper=[posper,negper,neuper]
        max=posper
        vibenum=0
        for i in range(0,3):
            if((maxper[i])>=max):
                max=maxper[i]
                vibenum=i
        if vibenum==2:
            vibe= 'Neutral'
        elif vibenum==1:
            vibe= 'Negative'
        else :
            vibe= 'Positive'
        max='The vibe of the word is: {}'.format(vibe)
        
        vibes=['Positive','Negative','Neutral']
        """plt.bar(vibes,maxper,color='blue',width=0.4)
        fig=plt.gcf()
        plt.ylabel('Percentage of tweets')
        
        buf=io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string=base64.b64encode(buf.read())
        uri=urllib.parse.quote(string)"""
        

        

        arr_pred.append(max)
        arr_pred.append(pos)
        arr_pred.append(neg)
        arr_pred.append(neu)
        return render(request,'prediction.html',{'arr_pred':arr_pred})


	# printing 
	#print("\n\nPositive tweets:")
	#for tweet in ptweets[:10]:
	#	print(tweet['text'])

	# printing first 5 negative tweets
	#print("\n\nNegative tweets:")
	#for tweet in ntweets[:10]:
	#	print(tweet['text'])

#if __name__ == "__main__":
	# calling main function
#	main()
