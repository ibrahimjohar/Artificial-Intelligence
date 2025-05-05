#Supervised Learning Libraries
#Supervised learning is a type of machine learning where the model is trained on labeled data.

#libraries:

#Scikit Learn
## provides algorithms for classification, regression, clustering, and dimensionality reduction.
## includes tools for model selection, preprocessing, and evaluation.

from sklearn.linear_model import LinearRegression
import numpy as np

#Scikit-learn expects X to be a 2-D array of shape (n_samples, n_features),
#so we call .reshape(-1,1) to turn [1,2,3,4,5] into
# [[1],
#  [2],
#  [3],
#  [4],
#  [5]]

X = np.array([1,2,3,4,5]).reshape(-1,1)
Y = np.array([2,4,6,8,10])              #y is your “target” array (the output) of the same length.

#Creates a linear regression object with ordinary least squares by default
model = LinearRegression()

#Fitting/training
# Finds the best-fit line y = mx + b that minimizes squared errors on the provided data
# In this case the data are perfectly on y = 2x, so it estimates slope m≈2 and intercept b≈0.
model.fit(X,Y)

#Making predictions
#Computes y^ = mX + b for each input in X.
print("predictions (predict()): ", model.predict(X))    #predictions: [ 2.  4.  6.  8. 10.]
print("slope (coef_[]):", model.coef_[0])      # ~2.0
print("intercept (intercept_):", model.intercept_)  # ~0.0

#This confirms the fitted line is y=2x+0.



