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

cluster1 = {}

with open('clusterfyp_raw_plus_preprocessed_multiple_3.txt') as f:
	for line in f:
		tag = json.loads(line)
		cluster_id = tag['cluster_id']
		ts_start = tag['ts_start']
		tag_name = cluster_id + '-' + ts_start
		tag_name = re.sub('#','_',tag_name)
		cluster1[tag_name] = tag
		
def get_list_of_clusters1():
	l = {}
	for k,v in cluster1.items():
		tag_name = v['cluster_id'] + '-' + v['ts_start']
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



@app.route('/isTrendPredict/<algo_tag_name>')
def render_trend(algo_tag_name):
	classifierAlgor = {'mlp': ['Multi-layer Perceptron Nerual Network Model (with 11 hidden layers)', 0.94, 'Max_MLP_predict'], 'gnb':['Gaussian Naive Bayes', 0.93, 'Max_GaussianNB_predict'], 'gbc':['Gradient Boosting Classifer', 0.91, 'Max_GradientBoosting_predict'], 'dtc':['Decision Tree Classifier', 0.91, 'Max_DecisionTree_predict'], 'rlm':['Regularized linear models with Stochastic Gradient Descent(SGD)', 0.89, 'Max_SGD_predict'], 'tca':['Two-Class AdaBoost boosting algorithm using AdaBoost-SAMME with decision trees', 0.89, 'Max_AdaBoostDecisionTree_predict'], 'lrs':['Logistic Regression', 0.89, 'Max_LogisticRegression_predict'], 'rfc': ['Random Forest Classifier - max depth = 15', 0.88, 'Max_RandomForest_predict'], 'lsv':['Linear Support Vector Classifier', 0.86, 'Max_LinearSVC_predict'], 'pac': ['Passive Aggressive Classifier', 0.84, 'Max_PassiveAgressive_predict'], 'knc': ['K-neighbors classifier', 0.82, 'Max_KNeighbors_predict'], 'etc': ['Extra-trees classifier', 0.79, 'Max_ExtraTree_predict'], 'bkn':['Bagging + k-neighbors classifier', 0.77, 'Max_BaggingAndKNeighbours_predict'], 'gpc':['Gaussian process classifier', 0.75, 'Max_GaussianProcess_predict'], 'ncc': ['Nearest centroid Classifier', 0.63, 'Max_NearestCentroid_predict'], 'rcf' : ['Ridge Classifier', 0.52, 'Max_Ridge_predict'], 'bnb':['Bernoulli Navies Bayes', '0.44', 'Max_BernoulliNB_predict'], 'lpc':['Label Propagation classifier', 0.30, 'Max_LabelPropagation_predict'] }
	algo = algo_tag_name[:3]
	tag_name = algo_tag_name[3:]

	algo_name = classifierAlgor[algo][0]
	algo_tpr = classifierAlgor[algo][1]

	ht_rmse = 0
	actual = ''
	predicte = 999

	tag = data[tag_name]

	with open('Trend_hashtag_json_key_value') as f:
		lines = f.readlines()
		for line in lines:
			entry = json.loads(line)
			if (entry['Topic'] == tag['ht_name'] and entry['Time'] == tag['ts_start']):
				actual = entry['Trend']
				predicted = entry[classifierAlgor[algo][2]]
				if (predicted == '1000'):
					predicted = '1000 (used as training set)'
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

	return render_template('isTrendPredict.html',**locals())

@app.route('/isTrendPredict')
def render_tredDefault():
	return render_trend('mlp_crypto-20180206-145600')

@app.route('/clusterValuePredict/<tag_name>')
def render_clusterValue(tag_name):
	list_of_samples = get_list_of_clusters1()

	tag = cluster1[tag_name]
	ht_name = tag['cluster_id']
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

	return render_template('clusterValuePredict.html',**locals())


@app.route('/clusterValuePredict')
def render_clusterValueDefault():
	return render_clusterValue('_hiphoprapmusichiphopmusic-20180201-073200')

@app.route('/clusterValueInput')
def render_clusterValueMenu():
	return render_template('clusterValueInput.html')

@app.route('/clusterValueInput/<algo_hashtag>')
def render_clusterValueMenu2(algo_hashtag):
	algo = algo_hashtag[:2]
	hashtag = ' ' + algo_hashtag[3:].strip()

	
	list_of_samples = {}

	for k,v in cluster1.items():
		print(v['cluster_words'])
		if(hashtag in v['cluster_words']):
			tag_name = v['cluster_id'] + '-' + v['ts_start']
			list_of_samples[k] = {}
			list_of_samples[k]['tag_name'] = tag_name
			list_of_samples[k]['isTrend'] = v['isTrend']
	print(hashtag)
	print(list_of_samples)


	return render_template('clusterValueInput2.html', **locals())


@app.route('/clusterIsTrendInput')
def render_clusterIsTrendMenu():
	return render_template('clusterIsTrendInput.html')

@app.route('/clusterIsTrendInput/<algo_hashtag>')
def render_clusterIsTrendMenu2(algo_hashtag):
	algo = algo_hashtag[:3]
	hashtag = ' ' + algo_hashtag[4:].strip()


	
	list_of_samples = {}
	for k,v in cluster1.items():
		print(v['cluster_words'])
		if(hashtag in v['cluster_words']):
			tag_name = v['cluster_id'] + '-' + v['ts_start']
			list_of_samples[k] = {}
			list_of_samples[k]['tag_name'] = tag_name
			list_of_samples[k]['isTrend'] = v['isTrend']
	print(hashtag)
	print(list_of_samples)


	return render_template('clusterIsTrendInput2.html', **locals())


@app.route('/clusterIsTrendPredict/<tag_name>')
def render_clusterIsTrned(tag_name):
	list_of_samples = get_list_of_clusters1()

	tag = cluster1[tag_name]
	ht_name = tag['cluster_id']
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

	return render_template('clusterIsTrendPredict.html',**locals())




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
