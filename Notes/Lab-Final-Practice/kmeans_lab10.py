#UNSUPERVISED LEARNING

# Unsupervised Learning is a type of machine learning where the model is not given any labeled data.
# Instead of being told what the correct output is, the model tries to find
# patterns or structure in the data on its own. The algorithm learns from the data itself —
# without guidance or answers.

# Unsupervised learning cannot be directly applied to a regression or classification
# problem because unlike supervised learning, we have the input data but no
# corresponding output data.

# The goal of unsupervised learning is to find the underlying structure of dataset, group that data according to similarities, and represent that dataset
# in a compressed format.

# Why use Unsupervised Learning?
# Below are some main reasons which describe the importance of Unsupervised
# Learning:
# ● Unsupervised learning is helpful for finding useful insights from the data.
# ● Unsupervised learning is much similar as a human learns to think by their own
# experiences, which makes it closer to the real AI.
# ● Unsupervised learning works on unlabeled and uncategorized data which make
# unsupervised learning more important.
# ● In real-world, we do not always have input data with the corresponding output
# so to solve such cases, we need unsupervised learning.

# Types of Unsupervised Learning
# 1. Clustering: Clustering is a way of grouping similar things together. In machine
# learning and data science, clustering is used to group similar data points into
# clusters, so that items in the same cluster are more alike than those in other clusters.

# 2. Association: An association rule is an unsupervised learning method which is
# used for finding the relationships between variables in the large database. It
# determines the set of items that occur together in the dataset. Association rule
# makes marketing strategy more effective. Such as people who buy X item
# (suppose a bread) are also tend to purchase Y (Butter/Jam) item.

# 3. Dimensionality Reduction: Dimensionality Reduction is the process of
# reducing the number of features (columns) in your dataset while keeping the
# important information. It helps simplify complex data, makes it easier to
# visualize, and often speeds up machine learning algorithms.

# K-Means clustering
# groups the unlabeled dataset into different clusters. Here K defines the number of pre-defined clusters that
# need to be created in the process, as if K=2, there will be two clusters, and for K=3, there
# will be three clusters, and so on.

# k-means clustering algorithm mainly performs two tasks:
# ● Determines the best value for K center points or centroids by an iterative
# process.
# ● Assigns each data point to its closest k-center. Those data points which are near
# to the particular k-center, create a cluster.

# How does the K-means algorithm works
# Step-1: Select the number K to decide the number of clusters.
# Step-2: Select random K points or centroids. (It can be other from the input
# dataset).
# Step-3: Assign each data point to their closest centroid, which will form the
# predefined K clusters.
# Step-4: Calculate the variance and place a new centroid of each cluster.
# Step-5: Repeat the third steps, which means reassign each datapoint to the new
# closest centroid of each cluster.
# Step-6: If any reassignment occurs, then go to step-4 else go to FINISH.
# Step-7: The model is ready.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#import dataset
df = pd.read_csv('mall_customers.csv')
df.head()

#extract variables
x = df.iloc[:, [3,4]].values

#finding optimal num of clusters using the elbow method
wcss_list = [] #Initializing the list for the values of WCSS

#using loop for iterations from 1 to 10
for i in range(1,11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss_list.append(kmeans.inertia_)
    
plt.plot(range(1, 11), wcss_list)
plt.title('The Elobw Method Graph')
plt.xlabel('Number of clusters(k)')
plt.ylabel('wcss_list')
plt.show()

#normalize the features for better clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

#training the k-means model on a dataset
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_predict = kmeans.fit_predict(X_scaled)

#visulaizing the clusters
plt.scatter(x[y_predict == 0, 0], x[y_predict == 0, 1], s = 100, c ='blue', label = 'Cluster 1') #for first cluster
plt.scatter(x[y_predict == 1, 0], x[y_predict == 1, 1], s = 100, c ='green', label = 'Cluster 2') #for second cluster
plt.scatter(x[y_predict== 2, 0], x[y_predict == 2, 1], s = 100, c ='red', label = 'Cluster 3') #for third cluster
plt.scatter(x[y_predict == 3, 0], x[y_predict == 3, 1], s = 100, c ='black', label = 'Cluster 4') #for fourth cluster
plt.scatter(x[y_predict == 4, 0], x[y_predict == 4, 1], s = 100, c ='purple', label = 'Cluster 5') #for fifth cluster
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s = 300, c = 'yellow', label = 'Centroid')
plt.title('Clusters of customers')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()
