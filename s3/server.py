#import essential libraries
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import re 
from pymongo import MongoClient


#create an instance of Flask class
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# use this part to enable mongo db connection 
client = MongoClient("mongodb://localhost:27017")
db = client['fyp']




data = {}

f = db.googleChart.find({}, {'_id':0})

for line in f:
	tag = line
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