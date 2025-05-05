#K-fold cross validation 

#K-fold cross validation divides the dataset into K equal parts (folds)
#model is trained K times, 
# each time using K-1 folds for training
# 1 fold for validation

#avg performance across all K folds is used as the final evaluation metric 

from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import seaborn as sns

#load dataset
df = sns.load_dataset("titanic")

#select features and target, handling missing values
X = df[['age', 'fare']].fillna(df[['age', 'fare']].mean())
Y = df['survived']

#convert to dataframe to use .iloc[]
X = pd.DataFrame(X)
Y = pd.Series(Y)

#define k-folds (5 splits)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

#initialize the model 
model = LogisticRegression()

#store the accuracy scores
accuracy_scores = []

#perform K-Fold Cross Validation
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index] #now X is a Dataframe
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index] #now Y is a series
    
    #train model 
    model.fit(X_train, Y_train)
    
    #predict and evaluate
    Y_pred = model.predict(X_test)
    acc = accuracy_score(Y_test, Y_pred)
    accuracy_scores.append(acc)


#print avg accuracy
print(f"k-fold avg accuracy: {np.mean(accuracy_scores):.4f}")
