#Leave-One-Out Cross Validation (LOOCV)

#extreme case of K-fold where K = total num of samples
#model is trained on all data except one sample & the process repeats for each sample

from sklearn.model_selection import LeaveOneOut

#initialize LOOCV
loo = LeaveOneOut()

#store accuracy scores
loo_scores = []

#perform LOOCV
for train_index, test_index in loo.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]
    
    #train the model
    model.fit(X_train, Y_train)
    
    #predict and evaluate
    Y_pred = model.predict(X_test)
    loo_scores.append(accuracy_score(Y_test, Y_pred))
    
print(f"LOOCV avg accuracy: {np.mean(loo_scores):.4f}")
