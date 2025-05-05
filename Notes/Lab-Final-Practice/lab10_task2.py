import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Sample vehicle data
data = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000, 75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck', 'Hatchback', 'SUV']
}

df = pd.DataFrame(data)

# Prepare data - use all features except vehicle_serial_no
X = df.drop('vehicle_serial_no', axis=1)

# One-hot encode categorical variable (vehicle_type)
encoder = OneHotEncoder(sparse=False)
vehicle_type_encoded = encoder.fit_transform(X[['vehicle_type']])
encoded_cols = encoder.get_feature_names_out(['vehicle_type'])
X_encoded = pd.concat([
    X.drop('vehicle_type', axis=1),
    pd.DataFrame(vehicle_type_encoded, columns=encoded_cols)
], axis=1)

# Function to perform clustering and visualize results
def perform_vehicle_clustering(X, title, scale_features=True):
    if scale_features:
        # Scale all features except vehicle_type (already encoded)
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
    
    # Based on elbow method, let's choose 3 clusters
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add clusters to original dataframe
    df_clustered = df.copy()
    df_clustered['Cluster'] = clusters
    
    # Visualize clusters using two most important features
    plt.figure(figsize=(10, 6))
    plt.scatter(df_clustered['mileage'], 
                df_clustered['maintenance_cost'], 
                c=df_clustered['Cluster'], cmap='viridis')
    plt.title(f'Vehicle Clusters ({title})')
    plt.xlabel('Mileage')
    plt.ylabel('Maintenance Cost')
    plt.colorbar(label='Cluster')
    plt.show()
    
    # Print cluster characteristics
    for cluster in sorted(df_clustered['Cluster'].unique()):
        cluster_data = df_clustered[df_clustered['Cluster'] == cluster]
        print(f"\nCluster {cluster} characteristics:")
        print(f"Average mileage: {cluster_data['mileage'].mean():.0f}")
        print(f"Average fuel efficiency: {cluster_data['fuel_efficiency'].mean():.1f}")
        print(f"Average maintenance cost: {cluster_data['maintenance_cost'].mean():.0f}")
        print("Vehicle types:", cluster_data['vehicle_type'].value_counts().to_dict())
    
    return df_clustered

# Perform clustering without scaling
print("Clustering without feature scaling:")
df_no_scale = perform_vehicle_clustering(X_encoded, "No Scaling", scale_features=False)

# Perform clustering with scaling
print("\nClustering with feature scaling:")
df_scaled = perform_vehicle_clustering(X_encoded, "All Features Scaled", scale_features=True)

# A transportation company wants to optimize its routes and fleet by categorizing
# different types of vehicles based on their usage patterns. The company has data on
# several features such as: vehicle_serial_no, mileage, fuel_efficiency, maintenance_cost,
# and vehicle_type. The goal is to create segments of vehicles based on these attributes to
# help with fleet management. Implement K-Means clustering to group vehicles using all
# the features. Perform the clustering twice: once without scaling the features and once
# with scaling applied to all features (except for vehicle_type, which is categorical).
# Analyze and compare the results, focusing on how the scaling affects the clustering
# output.
# Sample Data:
# # Example vehicle data
# data = {
# ‘vehicle_serial_no’: [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
# &#39;mileage&#39;: [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000,
# 75000, 280000],
# &#39;fuel_efficiency&#39;: [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
# &#39;maintenance_cost&#39;: [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
# &#39;vehicle_type&#39;: [&#39;SUV&#39;, &#39;Sedan&#39;, &#39;Truck&#39;, &#39;Hatchback&#39;, &#39;Sedan&#39;, &#39;Truck&#39;, &#39;SUV&#39;, &#39;Truck&#39;,
# &#39;Hatchback&#39;, &#39;SUV&#39;]
# }
# # Create a DataFrame
# df = pd.DataFrame(data)
