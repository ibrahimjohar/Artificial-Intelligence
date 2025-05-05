from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#sample dataset
data = {
    'spend_last6m': [1300, 750, 1600, 580, 2050, 920, 1750, 490, 2250, 800],
    'age_years':    [36, 27, 43, 24, 47, 31, 39, 23, 52, 29],
    'visit_count':  [9, 4, 11, 3, 13, 5, 8, 2, 14, 6],
    'purchases_per_month': [5, 1, 7, 1, 9, 2, 6, 1, 11, 2],
    'high_value':   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1=high-value, 0=low-value
}
df = pd.DataFrame(data)

#clean data
df = df.dropna()  # drop missing
for col in ['spend_last6m','age_years','visit_count','purchases_per_month']:
    low, high = df[col].quantile([0.01, 0.99])
    df[col] = df[col].clip(low, high)

#feature scaling
X = df.drop('high_value', axis=1)
y = df['high_value']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

#train decision tree
dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
dt_model.fit(X_train, y_train)

#evaluate
y_pred = dt_model.predict(X_test)
print(f"accuracy: {accuracy_score(y_test, y_pred):.2f}\n")
print("classification report:")
print(classification_report(y_test, y_pred))
print("confusion matrix:")
print(confusion_matrix(y_test, y_pred))

#visualize tree
plt.figure(figsize=(12, 8))
tree.plot_tree(
    dt_model,
    feature_names=X.columns,
    class_names=['LowValue','HighValue'],
    filled=True, rounded=True
)
plt.title("decision tree for customer classification")
plt.show()

#feature importance
importances = dt_model.feature_importances_
plt.barh(X.columns, importances)
plt.xlabel("feature importance")
plt.title("importance of features")
plt.show()

#classify a new customer
new_customer = np.array([[1900, 41, 9, 5]])  # spend_last6m, age_years, visit_count, purchases_per_month
new_scaled = scaler.transform(new_customer)
new_pred = dt_model.predict(new_scaled)[0]
print(f"\nnew customer is classified as: {'High-value' if new_pred == 1 else 'Low-value'}")
