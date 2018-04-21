import tweepy
import time
import json
import progressbar
import os
import sys
#'woeid': 44418, 'name': 'London', 

debug = False
limit_of_tweets_per_file = 10000
number_of_tweets = 0
auth_key = 'xseeWdXDxAMbsHsJLM58wdQxf'
auth_secret = '9EF3pE1tNHU6veXT8s9tj5KE92bJ4h1bixLtpnTRwMTFmsfQze'
access_token = '2839650654-ukODpcbvQBq17c25GMhfSEDpgRw6fH1moG0TEh3'
access_secret = 'I3zj8jUJAscBIWLjM9ZecXcZXPBzXxKDjy8g9D44z9M39'
#this word list is produced on 2008 tweet data, so may selectively capture trending words in 2008 (eg facebook)
#frequent_words_500 = ['#', 'the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','s','that','at','with','me','do','have','just','this','be','nt','so','are','m','not','was','but','out','up','what','now','new','from','your','like','good','no','get','all','about','we','if','time','as','day','will','one','twitter','how','can','some','an','am','by','going','they','go','or','has','rt','know','today','there','love','more','work','=','too','got','he','back','think','did','lol','when','see','really','had','great','off','would','need','here','thanks','been','blog','still','people','who','night','ll','want','why','bit.ly','home','re','should','well','oh','much','u','ve','then','right','make','last','over','way','cant','does','getting','watching','its','only','her','post','his','morning','very','she','them','could','first','than','better','after','tonight','our','again','down','twitpic.com','news','man','im','looking','us','tomorrow','best','into','any','hope','week','nice','show','yes','where','take','check','come','trying','fun','say','working','next','happy','were','even','live','watch','feel','thing','life','little','never','something','bad','free','doing','world','ff.im','video','sure','yeah','bed','let','use','their','look','being','long','done','sleep','before','year','find','awesome','big','un','+','things','ok','another','d','him','cool','old','ever','help','anyone','made','ready','days','die','other','read','because','two','playing','though','is.gd','house','always','also','listening','maybe','please','wow','haha','having','thank','pretty','game','someone','school','those','snow','twurl.nl','gonna','hey','many','start','wait','while','google','finally','everyone','para','try','god','weekend','most','iphone','stuff','around','music','looks','may','thought','keep','yet','reading','must','which','same','real','follow','bit','hours','might','actually','online','job','friends','said','obama','coffee','hate','hard','soon','tweet','por','making','wish','call','movie','tell','thinking','via','site','facebook','few','found','these','tv','sorry','through','already','lot','makes','give','put','waiting','stop','play','says','away','coming','early','dinner','phone','cold','using','times','book','kids','went','nothing','every','years','top','office','friend','talk','feeling','hour','head','web','food','amazing','car','lost','end','girl','since','guess','lunch','hot','sounds','b','funny','idea','glad','saw','hear','mean','name','damn','myself','guy','song','yay','least','business','run','place','friday','buy','enough','anything','late','photo','party','link','interesting','used','shit','tired','internet','following','left','guys','money','far','own','seems','media','baby','class','x','social','seen','miss','forward','part','until','open','win','hi','almost']
stream_filter_words = ['#']

auth = tweepy.OAuthHandler(auth_key, auth_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

output_file = None


def change_file():
	global output_file
	if output_file is not None:
		output_file.close()
	filename = './data_london/stream_tweets-{time}.txt'.format(time=time.strftime("%Y%m%d-%H%M%S"))
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	output_file = open(filename,'w')

def feed_to_file(json_dumps):
	if debug:
		print(json_dumps)
		return
	global	output_file, number_of_tweets
	number_of_tweets += 1
	if number_of_tweets % limit_of_tweets_per_file == 0 :
		change_file()
	s = json_dumps + '\n'
	output_file.write(s)
	print(number_of_tweets)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

	def __init__(self):
		self.api = api
		print('init StreamListener')
		
	def on_data(self, data):
		try:	
			newData = json.loads(data)
			#dont need retweeted because they are duplicates
			if 'retweeted_status' in newData:
				pass
				#return True
			if 'lang' not in newData or str(newData['lang']) != 'en':
				return True

			newDict = {	'created_at':str(newData['created_at']),	
				'hashtags':newData['entities']['hashtags'],
				'hashtags_count':len(newData['entities']['hashtags']),
				'favorite_count':newData['favorite_count'] if 'favorite_count' in newData else 0,
				'id_str':str(newData['id_str']),	
				'in_reply_to_status_id_str':str(newData['in_reply_to_status_id_str']) if 'in_reply_to_status_id_str' in newData else '',	
				'lang':str(newData['lang']) if 'lang' in newData else '',
				'retweet_count':newData['retweet_count'],	
				'text':str(newData['text']),	
				'user_created_at':str(newData['user']['created_at']),
				'user_favourites_count':newData['user']['favorite_count'] if 'favorite_count' in newData['user'] else 0,	
				'user_followers_count':newData['user']['followers_count'],
				'user_friends_count':newData['user']['friends_count'],	
				'user_id_str':str(newData['user']['id_str']),
				'user_statuses_count':newData['user']['statuses_count'],	
				'user_verified':newData['user']['verified'],
				'retweeted_status_id_str':str(newData['retweeted_status']['id_str']) if 'retweeted_status' in newData else ''
				}
			s = json.dumps(newDict) 
			feed_to_file(s)
			#print(s)

		except Exception as  e:
			print('exception: ',str(e))
			

		return True

	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			#returning False in on_error disconnects the stream
			return False

		# returning non-False reconnects the stream, with backoff.

#LONDON 
#[51.27, -0.54, 51.7, 0.3]
def stream_tweets():
	if not debug:
		change_file()
	while True:
		try:
			myStreamListener = MyStreamListener()
			myStream = tweepy.Stream(auth = auth, listener=myStreamListener)
			myStream.filter(track=stream_filter_words, locations=[51.27, -0.54, 51.7, 0.3])	
			#myStream.filter(track=frequent_words_500)	
		except:
			print('error reconnecting stream')
			continue

def main():
	#print('main()')
	stream_tweets()
	
if __name__ == '__main__':
	main()
