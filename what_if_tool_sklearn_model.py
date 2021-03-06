# -*- coding: utf-8 -*-
"""what-if-tool-Sklearn_model.ipynb

Automatically generated by Colaboratory.

"""

try:
  import google.colab
  !pip install --upgrade witwidget
except:
  pass

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor

import pandas as pd

# Set the path to the CSV containing the dataset to train on.
csv_path = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'

# Set the column names for the columns in the CSV. If the CSV's first line is a header line containing
# the column names, then set this to None.
csv_columns = [
  "Age", "Workclass", "fnlwgt", "Education", "Education-Num", "Marital-Status",
  "Occupation", "Relationship", "Race", "Sex", "Capital-Gain", "Capital-Loss",
  "Hours-per-week", "Country", "Over-50K"]

# Read the dataset from the provided CSV and print out information about it.
df = pd.read_csv(csv_path, names=csv_columns, skipinitialspace=True)

df

import numpy as np

# Set the column in the dataset you wish for the model to predict
label_column = 'Age'

# Set list of all columns from the dataset we will use for model input.
input_features = [
  'Over-50K', 'Workclass', 'Education', 'Marital-Status', 'Occupation',
  'Relationship', 'Race', 'Sex', 'Capital-Gain', 'Capital-Loss',
  'Hours-per-week', 'Country']

data=df.drop('Age',axis=1)
label=df[["Age"]]

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.33, random_state=42)

class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)

categorical=['Workclass', 'Education',
       'Marital-Status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Country',
       'Over-50K']

X_train=MultiColumnLabelEncoder(columns=categorical).fit_transform(X_train)
X_train.shape

params = {'n_estimators': 200, 'max_depth': 10,
          'learning_rate': 0.1, 'loss': 'ls','random_state':0}
reg = GradientBoostingRegressor(**params)
reg.fit(X_train, y_train)

def adjust_prediction(z):
 testing_data = pd.DataFrame(z, columns=X_test.columns.tolist())
 testing_data=MultiColumnLabelEncoder(columns=categorical).transform(testing_data)
 #scaling
 #cleaning
 return reg.predict(testing_data)

num_datapoints = 2000  
tool_height_in_px = 1000 
test_examples = np.hstack((X_test[:num_wit_examples].values,y_test[:num_wit_examples]))

from witwidget.notebook.visualization import WitConfigBuilder
from witwidget.notebook.visualization import WitWidget

config_builder = (WitConfigBuilder(test_examples.tolist(), X_test.columns.tolist() + ["age"])
  .set_custom_predict_fn(adjust_prediction)
  .set_target_feature('age')
  .set_model_type('regression'))
WitWidget(config_builder, height=tool_height_in_px)
