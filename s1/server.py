from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
tags = []
with open('raw_plus_preprocessed_multiple_3') as f:
	for line in f:
		tag = json.loads(line)
		tags.append(tag)

def getExchangeRates():
    rates = [1.1,2.1,3.1,4.1]
    return rates
 
@app.route("/")
def index():
	ht_name = tags[0]['ht_name']
	ts_start = tags[0]['ts_start']
	tag_name = ht_name + '-' + ts_start
	isTrend = tags[0]['isTrend']
	df_raw = [['timestamp', 'value']]
	df_nor = [['timestamp', 'value']]
	df_em = [['timestamp', 'value']]
	df_smoothed = [['timestamp', 'value']]

	ts_full = tags[0]['ts_full']
	_df_raw = tags[0]['df_raw']
	_df_nor = tags[0]['df_nor']
	_df_em = tags[0]['df_em']
	_df_smoothed = tags[0]['df_smoothed']

	for i in range(0,len(ts_full)):
		df_raw.append([ts_full[i],_df_raw[i]])
		df_nor.append([ts_full[i],_df_nor[i]])
		df_em.append([ts_full[i],_df_em[i]])
		df_smoothed.append([ts_full[i],_df_smoothed[i]])

	return render_template('test.html',**locals())      
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
 
if __name__ == "__main__":
    app.run()