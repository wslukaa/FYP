import tweepy
import time
import json
import progressbar
import os
import sys

#'woeid': 44418, 'name': 'London', 
debug = False
hours_to_stream = 7*24
auth_key = ''
auth_secret = ''
access_token = ''
access_secret = ''
#frequent_words_500 = ['#', 'the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','s','that','at','with','me','do','have','just','this','be','nt','so','are','m','not','was','but','out','up','what','now','new','from','your','like','good','no','get','all','about','we','if','time','as','day','will','one','twitter','how','can','some','an','am','by','going','they','go','or','has','rt','know','today','there','love','more','work','=','too','got','he','back','think','did','lol','when','see','really','had','great','off','would','need','here','thanks','been','blog','still','people','who','night','ll','want','why','bit.ly','home','re','should','well','oh','much','u','ve','then','right','make','last','over','way','cant','does','getting','watching','its','only','her','post','his','morning','very','she','them','could','first','than','better','after','tonight','our','again','down','twitpic.com','news','man','im','looking','us','tomorrow','best','into','any','hope','week','nice','show','yes','where','take','check','come','trying','fun','say','working','next','happy','were','even','live','watch','feel','thing','life','little','never','something','bad','free','doing','world','ff.im','video','sure','yeah','bed','let','use','their','look','being','long','done','sleep','before','year','find','awesome','big','un','+','things','ok','another','d','him','cool','old','ever','help','anyone','made','ready','days','die','other','read','because','two','playing','though','is.gd','house','always','also','listening','maybe','please','wow','haha','having','thank','pretty','game','someone','school','those','snow','twurl.nl','gonna','hey','many','start','wait','while','google','finally','everyone','para','try','god','weekend','most','iphone','stuff','around','music','looks','may','thought','keep','yet','reading','must','which','same','real','follow','bit','hours','might','actually','online','job','friends','said','obama','coffee','hate','hard','soon','tweet','por','making','wish','call','movie','tell','thinking','via','site','facebook','few','found','these','tv','sorry','through','already','lot','makes','give','put','waiting','stop','play','says','away','coming','early','dinner','phone','cold','using','times','book','kids','went','nothing','every','years','top','office','friend','talk','feeling','hour','head','web','food','amazing','car','lost','end','girl','since','guess','lunch','hot','sounds','b','funny','idea','glad','saw','hear','mean','name','damn','myself','guy','song','yay','least','business','run','place','friday','buy','enough','anything','late','photo','party','link','interesting','used','shit','tired','internet','following','left','guys','money','far','own','seems','media','baby','class','x','social','seen','miss','forward','part','until','open','win','hi','almost']

auth = tweepy.OAuthHandler(auth_key, auth_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#init progress bar
pbar = None
if debug is False:
	pbar = progressbar.ProgressBar(max_value=(hours_to_stream*6*600))	
	

def collect_trends():	
	progress_index = 0
	counter = 0 
	newTrends = []
	
	#Collect trends for x hours at 5 minute intervals
	while counter < (hours_to_stream * 6):
		#This information is cached for 5 minutes.

		if debug is False:
			#filename = './data2/trends-{time}.csv'.format(time=time.strftime("%Y%m%d-%H%M%S"))
			filename = './data2/trends.csv'
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			trends_csv = open(filename,'a')

		current_trends = api.trends_place(44418)
		for trend in current_trends[0]['trends']:
			try:
				#print(trend)
				if trend['name'] not in newTrends:
					#print(trend['name'],',',current_trends[0]['created_at'])
					tweet_volume = str(trend['tweet_volume']) if trend['tweet_volume'] is not None else '0'
					#print(tweet_volume)
					data = trend['name'] + ',' + current_trends[0]['created_at'] + ',' + tweet_volume + ',' + trend['query'] 
					#csv format
					data += '\n'
					if debug is False:
						trends_csv.write(data)
					else:
						print(data)
					newTrends.append(trend['name'])
			except:
				#print('error')
				continue
		trends_csv.close()
		counter += 1
		if debug is True:
			return
		for tmp in range(300):
			time.sleep(1)
			progress_index += 1
			if pbar is not None:
				pbar.update(progress_index)
		#time.sleep(600)
	


def main():
	#print('main()')
	collect_trends()

	return
	for x in api.trends_available():
		try:
			print(x)
		except:
			continue
	
if __name__ == '__main__':
	main()
