#task 1 - lab 09

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#sample dataset with some missing entries (csv alternative)
data = {
    'square_footage': [1200, 1600, 2000, np.nan, 1850, 2250, 1400, 1750, np.nan, 2100, 1950, 2300],
    'bedrooms': [2, 3, 4, 3, np.nan, 5, 2, 4, 3, 4, 3, 5],
    'bathrooms': [1, 2, 2.5, 2, 1.5, np.nan, 1, 2.5, 2, 3, 2, 3],
    'age': [15, 10, 5, 8, 12, 3, np.nan, 7, 6, 4, 9, 2],
    'neighborhood': ['Downtown', 'Uptown', 'Suburb', 'Suburb', 'Downtown', 'Uptown', 'Suburb', 'Downtown', 'Uptown', 'Suburb', 'Downtown', 'Uptown'],
    'price': [220000, 310000, 415000, 360000, 295000, 480000, 250000, 380000, 340000, 500000, 330000, 510000]
}


df = pd.DataFrame(data)

#handle missing vals w/ median imputation for numeric features
numeric_features = ['square_footage', 'bedrooms', 'bathrooms', 'age']
numeric_imputer = SimpleImputer(strategy='median')

#encode categorical variable 'neighborhood' with OneHotEncoder
elect_transformer = OneHotEncoder(drop='first')

#preprocessing steps
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_imputer, numeric_features),
    ('cat', elect_transformer, ['neighborhood'])
], remainder='passthrough')

#preparing features and target
X = df.drop('price', axis=1)
y = df['price']

#apply preprocessing
X_processed = preprocessor.fit_transform(X)

#feature names after encoding
encoded_cat_names = preprocessor.named_transformers_['cat'].get_feature_names_out(['neighborhood'])
feature_names = numeric_features + list(encoded_cat_names)

#split into train/test
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

#train Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

#evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"mean squared error: {mse:.2f}")
print(f"root MSE: {rmse:.2f}")
print(f"r-squared: {r2:.2f}")

#identify feature importances (coefficients)
coefs = model.coef_
importance = pd.Series(coefs, index=feature_names).sort_values(key=abs, ascending=False)
print("\nfeature importance (by absolute coefficient):")
print(importance)

#predict a new house price
new_house = pd.DataFrame({
    'square_footage': [1900],
    'bedrooms': [4],
    'bathrooms': [2.5],
    'age': [6],
    'neighborhood': ['Downtown']
})
new_processed = preprocessor.transform(new_house)
predicted_price = model.predict(new_processed)
print(f"\npredicted price for new house: ${predicted_price[0]:,.2f}")

#visualization
plt.scatter(y_test, y_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("actual price")
plt.ylabel("predicted price")
plt.title("actual vs predicted house prices")
plt.show()

