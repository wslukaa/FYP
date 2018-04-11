
import flask
from flask import Flask, render_template, request
from sklearn.externals import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS, cross_origin


from scipy import misc

app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/index")

def index():
   return flask.render_template('index.html')




@cross_origin()
@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        file = request.files['csv']

        if not file:
            return render_template('index.html', label="No file")
        #img = misc.imread(file)
        #img = img[:,:,:3]
        #img = img.reshape(1, -1)
        dfff = pd.read_csv(file)
        prediction = model.predict(dfff)
        label = str(np.squeeze(prediction))
        #label=1
        #if label=='1':
        #    label='0'
        return render_template('index.html', label=label, file=file)

@cross_origin()
@app.route("/testing", methods=['GET'])
def okok():
    return str(123)

if __name__ == '__main__':
    model = joblib.load('/Users/lukwingsan/FYP/model.pkl')
    app.run(host='127.0.0.1', port=8080, debug=True)

