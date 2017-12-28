%matplotlib inline
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
import script.stats as stats
import matplotlib.pyplot as plt
import sklearn

inf = open('stream_tweets-20171116-012802.txt','r')
dict_from_file = eval(inf.read())
inf.close()
 
Y = df[‘user_followers_count’]
X = df[‘lang’]
 
X=X.reshape(len(X),1)
Y=Y.reshape(len(Y),1)
 
# Split the data into training/testing sets
X_train = X[:-250]
X_test = X[-250:]
 
# Split the targets into training/testing sets
Y_train = Y[:-250]
Y_test = Y[-250:]
 
# Plot outputs
plt.scatter(X_test, Y_test,  color='black')
plt.title('Test Data')
plt.xlabel('lang')
plt.ylabel('user_followers_count)
plt.xticks(())
plt.yticks(())
 
plt.show()
