from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import re 

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

data = {}
with open('raw_plus_preprocessed_multiple_3') as f:
	for line in f:
		tag = json.loads(line)
		ht_name = tag['ht_name']
		ts_start = tag['ts_start']
		tag_name = ht_name + '-' + ts_start
		tag_name = re.sub('#','_',tag_name)
		data[tag_name] = tag
		
#<a href=""></a>
def get_list_of_samples():
	l = {}
	for k,v in data.items():
		tag_name = v['ht_name'] + '-' + v['ts_start']
		l[k] = {}
		l[k]['tag_name'] = tag_name
		l[k]['isTrend'] = v['isTrend']
	return l

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

	return render_template('test.html',**locals())

@app.route("/")
def index():
	return render_tag('_crypto-20180206-145600')
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
 
if __name__ == "__main__":
    app.run()