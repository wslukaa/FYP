#import essential libraries
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import re 
#from pymongo import MongoClient



#create an instance of Flask class
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# use this part to enable mongo db connection 
#client = MongoClient("mongodb://localhost:27017")
#db = client['fyp']




data = {}

#f = db.googleChart.find({}, {'_id':0})
with open('raw_plus_preprocessed_multiple_3.txt') as f:
	for line in f:
		tag = json.loads(line)
		ht_name = tag['ht_name']
		ts_start = tag['ts_start']
		tag_name = ht_name + '-' + ts_start
		tag_name = re.sub('#','_',tag_name)
		data[tag_name] = tag
		
def get_list_of_samples():
	l = {}
	for k,v in data.items():
		tag_name = v['ht_name'] + '-' + v['ts_start']
		l[k] = {}
		l[k]['tag_name'] = tag_name
		l[k]['isTrend'] = v['isTrend']
	return l

def render_tag_list(tag_name):
	list_of_samples = get_list_of_samples()

	tag = data[tag_name]
	ht_name = tag['ht_name']
	ts_start = tag['ts_start']
	tag_name = ht_name + '-' + ts_start
	isTrend = tag['isTrend']
	df_raw = [['timestamp', 'value']]
	df_nor = [['timestamp', 'value']]
	df_em = [['timestamp', 'value']]
	df_smoothed = [['timestamp', 'value']]

	ts_full = tag['ts_full']
	_df_raw = tag['df_raw']
	_df_nor = tag['df_nor']
	_df_em = tag['df_em']
	_df_smoothed = tag['df_smoothed']

	for i in range(0,len(ts_full)):
		df_raw.append([ts_full[i],_df_raw[i]])
		df_nor.append([ts_full[i],_df_nor[i]])
		df_em.append([ts_full[i],_df_em[i]])
		df_smoothed.append([ts_full[i],_df_smoothed[i]])

	return render_template('listSearch.html',**locals())

@app.route('/tag/<tag_name>')
def render_tag(tag_name):
	list_of_samples = get_list_of_samples()

	tag = data[tag_name]
	ht_name = tag['ht_name']
	ts_start = tag['ts_start']
	tag_name = ht_name + '-' + ts_start
	isTrend = tag['isTrend']
	df_raw = [['timestamp', 'value']]
	df_nor = [['timestamp', 'value']]
	df_em = [['timestamp', 'value']]
	df_smoothed = [['timestamp', 'value']]

	ts_full = tag['ts_full']
	_df_raw = tag['df_raw']
	_df_nor = tag['df_nor']
	_df_em = tag['df_em']
	_df_smoothed = tag['df_smoothed']

	for i in range(0,len(ts_full)):
		df_raw.append([ts_full[i],_df_raw[i]])
		df_nor.append([ts_full[i],_df_nor[i]])
		df_em.append([ts_full[i],_df_em[i]])
		df_smoothed.append([ts_full[i],_df_smoothed[i]])

	return render_template('directSearch.html',**locals())


@app.route('/valuePredict/<algo_tag_name>')
def render_value(algo_tag_name):
	regressionAlgor = {'kr': ['Kernel Ridge Regression', 4.449910311, 7], 'dt':['Decision Tree Regression', 6.318584563, 8], 'kn':['KNN Regression', 6.084973799, 9], 'lp': ['MLP Regression', 6.192667041, 10], 'rf': ['Random Forest Regression',  6.128285151, 11], 'gp':['Gaussian process Regression', 344.3642791, 12], 'ls':['Linear Support Vector Regression', 4.459506737,13] }
	algo = algo_tag_name[:2]
	tag_name = algo_tag_name[2:]

	algo_name = regressionAlgor[algo][0]
	algo_rmse = regressionAlgor[algo][1]

	ht_rmse = 0

	tag = data[tag_name]

	with open('hashtagResult.json') as f:
		lines = f.readlines()
		for line in lines:
			entry = json.loads(line)
			if (entry['ht_name'] == tag['ht_name'] and entry['ts_start'] == tag['ts_start']):
				ht_rmse = entry[algo]
				break

	list_of_samples = get_list_of_samples()

	
	ht_name = tag['ht_name']
	ts_start = tag['ts_start']
	tag_name = ht_name + '-' + ts_start
	isTrend = tag['isTrend']
	df_raw = [['timestamp', 'value']]
	df_nor = [['timestamp', 'value']]
	df_em = [['timestamp', 'value']]
	df_smoothed = [['timestamp', 'value']]

	ts_full = tag['ts_full']
	_df_raw = tag['df_raw']
	_df_nor = tag['df_nor']
	_df_em = tag['df_em']
	_df_smoothed = tag['df_smoothed']

	for i in range(0,len(ts_full)):
		df_raw.append([ts_full[i],_df_raw[i]])
		df_nor.append([ts_full[i],_df_nor[i]])
		df_em.append([ts_full[i],_df_em[i]])
		df_smoothed.append([ts_full[i],_df_smoothed[i]])

	return render_template('valuePredict.html',**locals())

@app.route('/valuePredict')
def render_valueDefault():
	return render_value('kr_crypto-20180206-145600')



@app.route("/")
def index():
	return render_template('summary2.html')
 
"""@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/home")
def home():
	return home
"""
@app.route("/direct")
def directSearch():
	return render_tag('_crypto-20180206-145600')

@app.route("/select")
def selectSearch():
	return render_tag_list('_crypto-20180206-145600')

@app.route("/cluster")
def showCluster():
	return render_template('cluster2.html')

@app.route("/words")
def showWords():
	return render_template('words.html')

@app.route("/tsne")
def showTsne():
	return render_template('tsne.html')

@app.route("/bubble")
def showBubble():
	return render_template('bubble.html')


 
 
if __name__ == "__main__":
    app.run()
