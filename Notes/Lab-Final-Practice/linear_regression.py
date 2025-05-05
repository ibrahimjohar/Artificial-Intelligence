#REGRESSION 

#linear regression
#used for predictive analysis in machine learning.

# Linear regression shows the linear relationship between the independent(predictor) variable i.e. X-axis and the
# dependent(output) variable i.e. Y-axis, called linear regression. If there is a single input
# variable X (independent variable), such linear regression is called simple linear regression.

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#create & train the linear regression model
LR = LinearRegression()
ModelLR = LR.fit(X_train, y_train)

#predict on the test data
PredictionLR = ModelLR.predict(X_test)

#print predictions
print("predictions: ", PredictionLR)
