import csv
import time
import os
import json
from datetime import datetime, timedelta
import progressbar
import re

debug = True
input_path_trends_tags = './timestamp-interval-analysis-trend-source.csv'
source_folder_for_analysis = './data-before-2017-07-30/tweets/'
frequent_words_500 = ['#', 'the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','s','that','at','with','me','do','have','just','this','be','nt','so','are','m','not','was','but','out','up','what','now','new','from','your','like','good','no','get','all','about','we','if','time','as','day','will','one','twitter','how','can','some','an','am','by','going','they','go','or','has','rt','know','today','there','love','more','work','=','too','got','he','back','think','did','lol','when','see','really','had','great','off','would','need','here','thanks','been','blog','still','people','who','night','ll','want','why','bit.ly','home','re','should','well','oh','much','u','ve','then','right','make','last','over','way','cant','does','getting','watching','its','only','her','post','his','morning','very','she','them','could','first','than','better','after','tonight','our','again','down','twitpic.com','news','man','im','looking','us','tomorrow','best','into','any','hope','week','nice','show','yes','where','take','check','come','trying','fun','say','working','next','happy','were','even','live','watch','feel','thing','life','little','never','something','bad','free','doing','world','ff.im','video','sure','yeah','bed','let','use','their','look','being','long','done','sleep','before','year','find','awesome','big','un','+','things','ok','another','d','him','cool','old','ever','help','anyone','made','ready','days','die','other','read','because','two','playing','though','is.gd','house','always','also','listening','maybe','please','wow','haha','having','thank','pretty','game','someone','school','those','snow','twurl.nl','gonna','hey','many','start','wait','while','google','finally','everyone','para','try','god','weekend','most','iphone','stuff','around','music','looks','may','thought','keep','yet','reading','must','which','same','real','follow','bit','hours','might','actually','online','job','friends','said','obama','coffee','hate','hard','soon','tweet','por','making','wish','call','movie','tell','thinking','via','site','facebook','few','found','these','tv','sorry','through','already','lot','makes','give','put','waiting','stop','play','says','away','coming','early','dinner','phone','cold','using','times','book','kids','went','nothing','every','years','top','office','friend','talk','feeling','hour','head','web','food','amazing','car','lost','end','girl','since','guess','lunch','hot','sounds','b','funny','idea','glad','saw','hear','mean','name','damn','myself','guy','song','yay','least','business','run','place','friday','buy','enough','anything','late','photo','party','link','interesting','used','shit','tired','internet','following','left','guys','money','far','own','seems','media','baby','class','x','social','seen','miss','forward','part','until','open','win','hi','almost']

def find_bigrams(input_list):
	bigram_list = []
	for i in range(len(input_list)-1):
		bigram_list.append((input_list[i], input_list[i+1]))
	return bigram_list


def main(look_behind_hours=20, look_forward_hours=20):
	list_of_tweets = [ source_folder_for_analysis + x.decode('ascii') for x in os.listdir(os.fsencode(source_folder_for_analysis)) ] 

	with open( input_path_trends_tags , 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		trends_raw = list(reader)

	trends_gram12_filtered = []
	datetime_first = datetime.strptime(trends_raw[0][1], '%Y%m%d-%H%M%S')
	datetime_pivot = datetime_first + timedelta(hours=look_behind_hours)
	datetime_last = datetime_pivot +  timedelta(hours=look_forward_hours)
	

	for t in trends_raw:
		#2017-07-21T10:06:38Z
		trend_datetime = datetime.strptime(t[1], '%Y%m%d-%H%M%S')	
		if trend_datetime > datetime_pivot and trend_datetime < datetime_last:
			gram1_raw = re.findall('[#a-z0-9][a-z0-9]+',t[0].lower())
			gram1 = []
			for g in gram1_raw:
				if g not in frequent_words_500:
					gram1.append(g)
			gram12 = gram1 + find_bigrams(gram1)
			for g in gram12:
				trends_gram12_filtered.append(g)
	
	
	grams_in_hour = [None]*(look_behind_hours)
	
	file_count = 1

	for f_name in list_of_tweets:
		f = open(f_name,'r')
		#print(file_count)
		file_count += 1
		for line in f:
			tweet = json.loads(line)
			#Fri Jul 21 11:09:32 +0000 2017
			datetime_tweet = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			if datetime_tweet < datetime_first or datetime_tweet > datetime_pivot:
				continue
			index_grams_in_hour = 0
			while index_grams_in_hour < look_behind_hours:
				if (datetime_tweet - datetime_first) > timedelta(hours=(index_grams_in_hour + 1) ):
					index_grams_in_hour += 1
				else:
					break
			

			s = tweet['text'].lower()
			
			gram1_raw = re.findall('[#a-z0-9][a-z0-9]+',s)
			gram1 = []
			#stopwords removal
			for g in gram1_raw:
				if g not in frequent_words_500:
					gram1.append(g)
			gram12 = gram1 + find_bigrams(gram1)
			if not grams_in_hour[index_grams_in_hour]:
				grams_in_hour[index_grams_in_hour] = {}
			for g in gram12:
				if g in grams_in_hour[index_grams_in_hour]:
					grams_in_hour[index_grams_in_hour][g]['count'] += 1
				else:
					grams_in_hour[index_grams_in_hour][g] = {}
					grams_in_hour[index_grams_in_hour][g]['count'] = 1
			#print(grams_in_hour[index_grams_in_hour])
	#print(grams_in_hour[0],grams_in_hour[1],grams_in_hour[2],grams_in_hour[3])
	
	grams_combined = grams_in_hour[0]
	for key, value in grams_combined.items():
		grams_combined[key]['first_count'] = grams_combined[key]['count']

	for i in range( 1, look_behind_hours):
		for key, value in grams_in_hour[i].items():
			if key in grams_combined:
				hourly_chg_of_count = ( value['count'] + grams_combined[key]['count'] ) / grams_combined[key]['count'] - 1
				if not 'avg_of_hourly_chg_of_count' in grams_combined[key]:
					grams_combined[key]['avg_of_hourly_chg_of_count'] = hourly_chg_of_count
					grams_combined[key]['index_to_calc_avg'] = 1
				else:
					index_to_calc_avg = grams_combined[key]['index_to_calc_avg'] 
					grams_combined[key]['avg_of_hourly_chg_of_count'] = ( hourly_chg_of_count + grams_combined[key]['avg_of_hourly_chg_of_count'] * index_to_calc_avg ) / ( index_to_calc_avg + 1)
					grams_combined[key]['index_to_calc_avg'] += 1
				grams_combined[key]['count'] += value['count']
			else:
				grams_combined[key] = value
				grams_combined[key]['first_count'] = value['count']
	
	for key, value in grams_combined.items():
		grams_combined[key]['chg_of_final_to_first_count'] = grams_combined[key]['count'] / grams_combined[key]['first_count'] - 1

	#clean useless data
	useless_key = []
	for key, value in grams_combined.items():
		if grams_combined[key]['count'] < 10:
			useless_key.append(key)
	for key in useless_key:
		del grams_combined[key]

	#print(trends_gram12_filtered)
	row = ''
	for x in trends_gram12_filtered:
		try:
			row += x + ','
		except:
			continue
	print(row)
	for key, value in grams_combined.items():
		try:
			row = key + ',' + str(value['chg_of_final_to_first_count']) + ',' + str(value['avg_of_hourly_chg_of_count']) + ',' + str(value['first_count']) + ',' + str(value['count'])
		except:
			continue
		print(row)

	return

if __name__ == '__main__':
	main()
