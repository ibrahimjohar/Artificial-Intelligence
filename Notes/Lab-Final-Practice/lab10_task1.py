import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

# Load the dataset (assuming it's the Mall_Customers.csv)
# For demonstration, I'll create a sample dataset with similar features
data = {
    'CustomerID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'Gender': ['Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Male', 'Female',
              'Male', 'Female', 'Female', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female'],
    'Age': [19, 21, 20, 23, 31, 22, 35, 23, 64, 30, 67, 35, 58, 24, 37, 22, 35, 20, 52, 35],
    'Annual Income (k$)': [15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 19, 20, 23, 24, 25, 28, 28, 29, 30, 33],
    'Spending Score (1-100)': [39, 81, 6, 77, 40, 76, 6, 94, 3, 72, 14, 99, 15, 77, 35, 86, 92, 79, 36, 85]
}

df = pd.DataFrame(data)

# Prepare data - use all features except CustomerID
X = df.drop('CustomerID', axis=1)

# Encode categorical variable (Gender)
le = LabelEncoder()
X['Gender'] = le.fit_transform(X['Gender'])

# Function to perform clustering and visualize results
def perform_clustering(X, title, scale_features=True, exclude_age=False):
    if scale_features:
        if exclude_age:
            # Scale all features except Age
            scaler = StandardScaler()
            cols_to_scale = [col for col in X.columns if col != 'Age']
            X_scaled = X.copy()
            X_scaled[cols_to_scale] = scaler.fit_transform(X_scaled[cols_to_scale])
        else:
            # Scale all features
            scaler = StandardScaler()
            X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    else:
        X_scaled = X.copy()
    
    # Find optimal K using Elbow method
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), wcss, marker='o')
    plt.title(f'Elbow Method ({title})')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    
    # Based on elbow method, let's choose 5 clusters
    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add clusters to original dataframe
    df_clustered = df.copy()
    df_clustered['Cluster'] = clusters
    
    # Visualize clusters using two most important features
    plt.figure(figsize=(10, 6))
    plt.scatter(df_clustered['Annual Income (k$)'], 
                df_clustered['Spending Score (1-100)'], 
                c=df_clustered['Cluster'], cmap='viridis')
    plt.title(f'Customer Clusters ({title})')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.colorbar(label='Cluster')
    plt.show()
    
    return df_clustered

# Perform clustering without scaling
print("Clustering without feature scaling:")
df_no_scale = perform_clustering(X, "No Scaling", scale_features=False)

# Perform clustering with scaling (all features)
print("Clustering with all features scaled:")
df_scaled_all = perform_clustering(X, "All Features Scaled", scale_features=True, exclude_age=False)

# Perform clustering with scaling (all features except Age)
print("Clustering with all features scaled except Age:")
df_scaled_except_age = perform_clustering(X, "All Features Scaled Except Age", scale_features=True, exclude_age=True)

# Compare cluster distributions
print("\nCluster distribution without scaling:")
print(df_no_scale['Cluster'].value_counts())

print("\nCluster distribution with all features scaled:")
print(df_scaled_all['Cluster'].value_counts())

print("\nCluster distribution with all features scaled except Age:")
print(df_scaled_except_age['Cluster'].value_counts())

# In the example code above, customer segmentation was performed using only two
# features. Now, use all available features except customer_id to implement K-Means
# clustering. Perform the clustering twice — once without feature scaling, and once with
# scaling applied to all features except age. Compare the results and comment on the
# differences and insights observed from these changes.
