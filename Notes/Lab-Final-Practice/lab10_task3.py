import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Sample student data
data = {
    'student_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 
                   111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
    'GPA': [3.2, 3.8, 2.9, 3.5, 3.1, 3.9, 2.5, 3.7, 2.8, 3.6, 
            3.0, 3.4, 2.7, 3.3, 2.6, 3.5, 3.1, 3.8, 2.9, 3.7],
    'study_hours': [12, 18, 8, 15, 10, 20, 6, 16, 7, 17, 
                    9, 14, 5, 13, 4, 15, 11, 19, 8, 16],
    'attendance_rate': [75, 95, 65, 85, 70, 98, 60, 90, 62, 88, 
                        68, 82, 58, 80, 55, 87, 72, 96, 66, 92]
}

df = pd.DataFrame(data)

# Prepare data - use GPA, study_hours, and attendance_rate
X = df[['GPA', 'study_hours', 'attendance_rate']]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal K using Elbow method
wcss = []
for i in range(2, 7):  # Testing K from 2 to 6
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(2, 7), wcss, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Based on elbow method, let's choose 3 clusters
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add clusters to original dataframe
df_clustered = df.copy()
df_clustered['Cluster'] = clusters

# Visualize clusters using study_hours and GPA
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df_clustered['study_hours'], 
                     df_clustered['GPA'], 
                     c=df_clustered['Cluster'], 
                     cmap='viridis',
                     s=100)
plt.title('Student Clusters by Study Hours and GPA')
plt.xlabel('Weekly Study Hours')
plt.ylabel('GPA')
plt.colorbar(scatter, label='Cluster')
plt.grid(True)

# Add cluster centers to the plot
centers = kmeans.cluster_centers_
# Inverse transform to get back to original scale
centers_original = scaler.inverse_transform(centers)
plt.scatter(centers_original[:, 1],  # study_hours
            centers_original[:, 0],  # GPA
            s=200, marker='X', c='red', label='Cluster Centers')
plt.legend()
plt.show()

# Print cluster characteristics
print("\nCluster Characteristics:")
for cluster in sorted(df_clustered['Cluster'].unique()):
    cluster_data = df_clustered[df_clustered['Cluster'] == cluster]
    print(f"\nCluster {cluster}:")
    print(f"Number of students: {len(cluster_data)}")
    print(f"Average GPA: {cluster_data['GPA'].mean():.2f}")
    print(f"Average study hours: {cluster_data['study_hours'].mean():.1f}")
    print(f"Average attendance rate: {cluster_data['attendance_rate'].mean():.1f}%")

# Display final dataset with cluster assignments
print("\nStudent Cluster Assignments:")
print(df_clustered[['student_id', 'Cluster']].sort_values('student_id'))


# The academic affairs department at FAST NUCES Karachi is looking to identify distinct
# groups of students based on their academic engagement and performance. 
# The department has access to anonymized student data containing the attributes student_id,
# GPA, study_hours (average weekly study hours), and attendance_rate (percentage of
# classes attended).
# The goal is to group students into meaningful clusters that can help tailor academic
# support programs, such as extra tutoring, mentoring sessions, or motivation workshops.
# You are required to perform unsupervised learning using K-Means clustering on
# the student dataset. Do following :
# ● Feature Selection and Scaling: Use the following features for clustering: GPA,
# study_hours, and attendance_rate.
# ● Apply appropriate feature scaling before clustering.
# ● Determine Optimal Number of Clusters (K): Use the ELbow method to determine
# the optimal number of clusters (K) in the range of 2 to 6.
# ● Perform Clustering: Apply K-Means using the optimal K and assign a cluster label
# to each student.
# ● Visualization: Create a scatter plot to visualize the clusters using study_hours
# and GPA as the axes.
# ● Color each point based on its cluster.
# ● Add an informative title and labels for clarity.
# ● Deliverables: Display the final dataset showing student IDs along with their
# assigned cluster.
# ● Present the scatter plot that illustrates the clustering result.
