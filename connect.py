from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import tweepy #used for ingesting the stream
from kafka import KafkaConsumer #used for a consumer
import urllib3

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        f = open('../kafka_2.11-1.1.0/test.txt', 'a+') 
        f.write(status.text)  # Python 3.x
    
    def on_error(self, status_code):
        print (status_code)
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
def main():
	# tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	# auth.secure=True
	auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.secure=True
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	print(auth.consumer_key)
	# create the api needed for the stream
	api = tweepy.API(auth)
	# Create the streamlistener object and init the stream using the api object
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	# Start the stream usin a filter word track uses a keyword and follow=["2211149702"] to track a user
	# keyword async allows teh stream to run on a new thread async=True
	myStream.filter(track=['trump'])
	return 0
if __name__ == "__main__":
    main()