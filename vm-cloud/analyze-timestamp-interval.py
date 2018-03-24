import csv
import time
import os
import json
from datetime import datetime
import progressbar

debug = False
input_path_trends_tags = './trends-20170926-20171115.csv'
output_path = './output-timestamp-interval-{time}.csv'.format(time=time.strftime("%Y%m%d-%H%M%S"))
source_folder_for_analysis = './data/tweets/'
input_list = []
def main():
	list_of_tweets = [ source_folder_for_analysis + x.decode('ascii') for x in os.listdir(os.fsencode(source_folder_for_analysis)) ] 
	
	if not debug:
		os.makedirs(os.path.dirname(output_path), exist_ok=True)
		output_file = open(output_path,'w')
		#output_file.write('trend_name,ts,count_before,count_after,tweet_volume,query\n')


	with open( input_path_trends_tags , 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		input_list = list(reader)

	#init progress ProgressBar
	pbar = None
	pbar = progressbar.ProgressBar(max_value=(len(input_list) * len(list_of_tweets)))
	pbar_count = 0 	
	
	block = 0
	for trend in input_list:
		block += 1
		#print(trend[0])
		#2017-07-21T10:06:38Z
		#time_tag = datetime.strptime(trend[1], '%Y%m%d-%H%M%S')
		try:
			time_tag = datetime.strptime(trend[1], '%Y-%m-%dT%H:%M:%SZ')
		except:
			pbar_count += len(list_of_tweets)
			pbar.update(pbar_count)
			continue
			
		string_time_diff = ''

		flag_eof = False
		no_volume = False
		if str(trend[2]) == '0':
			no_volume = True
			flag_eof = True

		for f_name in list_of_tweets:
			pbar_count += 1
			pbar.update(pbar_count)
			if flag_eof:
				continue
			f = open(f_name,'r')
			for line in f:
				tweet = json.loads(line)
				#Fri Jul 21 11:09:32 +0000 2017
				time_tweet = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
				time_tag_ts = time.mktime(time_tag.timetuple())
				time_tweet_ts = time.mktime(time_tweet.timetuple())
				if trend[0] in tweet['text']:
					time_diff = int(time_tweet_ts - time_tag_ts) / 60
					time_diff = int(time_diff)
					if time_diff > 0:
						flag_eof = True
						break
					string_time_diff += str(time_diff) + ','
		#print('before: ',count_before, ' after: ', count_after)
		data = trend[0] + ',' + str(trend[2]) + ',' + time_tag.strftime("%Y%m%d-%H%M%S")  + ',' + string_time_diff
		data += '\n'
		if not debug:
			if not no_volume:
				output_file.write(data)

	if not debug:
		output_file.close()
	pass


if __name__ == '__main__':
	main()
