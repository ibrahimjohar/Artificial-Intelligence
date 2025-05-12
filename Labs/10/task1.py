import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

def prepare_features(df, scale_cols, leave_cols):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[scale_cols])
    df_scaled = pd.DataFrame(scaled, columns=scale_cols, index=df.index)
    return pd.concat([df_scaled, df[leave_cols]], axis=1)

def plot_elbow(X, k_range, title):
    wcss = [KMeans(n_clusters=k, init="k-means++", random_state=42)
            .fit(X).inertia_ for k in k_range]
    plt.figure(figsize=(8,4))
    plt.plot(k_range, wcss, 'o-')
    plt.title(title)
    plt.xlabel("k")
    plt.ylabel("WCSS")
    plt.show()

def plot_clusters(X, labels, title):
    colors = ['blue','green','red','black','purple']
    plt.figure(figsize=(8,5))
    for i, color in enumerate(colors[:labels.max()+1]):
        mask = (labels == i)
        plt.scatter(
            X.loc[mask, "Annual Income (k$)"],
            X.loc[mask, "Spending Score (1-100)"],
            s=100, c=color, label=f"Cluster {i+1}"
        )
    plt.title(title)
    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.legend()
    plt.show()

df = pd.read_csv('Mall_Customers.csv')
x = df.drop(columns=["CustomerID"])
x["Gender"] = LabelEncoder().fit_transform(x["Gender"])

# Elbow (no scaling)
plot_elbow(x, range(2,11), "Elbow Method (No Scaling)")

# K-Means without scaling
labels_ns = KMeans(n_clusters=5, random_state=42).fit_predict(x)
plot_clusters(x, labels_ns, "Clusters (No Scaling)")

# Prepare scaled data (except Age)
X_scaled = prepare_features(x, ['Annual Income (k$)','Spending Score (1-100)','Gender'], ['Age'])
labels_s = KMeans(n_clusters=5, random_state=42).fit_predict(X_scaled)
plot_clusters(X_scaled.join(df[[]]), labels_s, "Clusters (Scaling Except Age)")

