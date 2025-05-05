#performance evaluation metrics

# commonly used evaluation metrics in machine learning:
# ● Accuracy
# ● Precision
# ● Recall
# ● R2 Score
# ● ROC AUC Curve

#for classification:
# accuracy score
# f1score
# precision 
# recall 
# ROC_AUC Score 
# Balanced Accuracy Score
# confusion matrix

#for regression: 
# Mean Absolute Error 
# Mean Square Error 
# Max Error 
# R2 Score 
# Explained Variance Score 
# D2 Absolute Score

#CONFUSION MATRIX

# True Positive (TP): The number of times our model correctly predicts positive values.
# You predicted a positive value, and it is actually positive.
# ● False Positive (FP): The number of times our model wrongly predicts positive values when they are actually negative.
# You predicted a positive value, but it is actually negative.
# ● True Negative (TN): The number of times our model correctly predicts negative values.
# You predicted a negative value, and it is actually negative.
# ● False Negative (FN): The number of times our model wrongly predicts negative values when they are actually positive.
# You predicted a negative value, but it is actually positive.


#ROC Curve - Receiver Operating Characteristic

#common used tool for evaluating performance of binary classification algos

# An ROC curve is a plot of the true positive rate (TPR) against the false positive rate (FPR) for a binary classifier at different classification thresholds.
# The TPR is the proportion of true positives (correctly predicted positive cases) out of all actual positives, while the FPR is the 
# proportion of false positives (incorrectlypredicted positive cases) out of all actual Negatives.

from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# Assuming the model has been trained and 'PredictionDT' holds class predictions
# To compute ROC, we need the probability estimates, not just the predicted class.
# For binary classification, use the probabilities of the positive class.

#get probabilities for the positive class
probabilities = DT.predict_proba(X_test)[:, 1] #get probability for class '1'

#calculate ROC curve 
fpr, tpr, thresholds = roc_curve(Y_test, probabilities)

#calculate ROC_AUC score
roc_auc = roc_auc_score (Y_test, probabilities)

#plot ROC curve with shaded area under the curve
plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.fill_between(fpr, tpr, color='skyblue', alpha=0.4)
plt.plot([0,1],[0,1], color='gray', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve with AUC Area')
plt.legend(loc='lower right')
plt.show()

