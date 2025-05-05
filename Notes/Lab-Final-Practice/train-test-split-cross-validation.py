#Train-Test Split & Cross Validation

#the train-test split technique used in machine learning to evaluate the performance of a model
#involves splitting the dataset into two subsets

## training set: used to train the model
## testing set: used to evaluate the model's performace on unseen data

# this helps in assesing how well the model generalizes to new data and prevents issues like overfitting

#underfitting: model is too simple, performs poorly on training & test data
#overfitting: model memorizes training data but performs poorly on unseen data

#solution: use train-test split and cross-validation to check generalization

#diff ways to split data:
#80-20 split (common):
## 80% TRAINING - 20% TESTING
## used in general ML problems

#70-30 split:
## more test data, useful when we need better validation

#60-20-20 split:
## 60% TRAINING - 20% VALIDATION - 20% TESTING
## used for hyperparameter tuning to avoid overfitting

#train-test split, with the Naïve Bayes Classifier:
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np

#generate dummy dataset
X = np.random.rand(100, 5) #100 samples, 5 features
Y = np.random.randint(0, 2, 100) #binary target variable (0 or 1)

#splitting the data into 80% training and 20% testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#create a naive bayes model
model = GaussianNB()

#train the model on training data
model.fit(X_train, Y_train)

#predict on test data
Y_pred = model.predict(X_test)

#evaluate the model
accuracy = accuracy_score(Y_test, Y_pred)
print(f"model accuracy: {accuracy:.2f}")
