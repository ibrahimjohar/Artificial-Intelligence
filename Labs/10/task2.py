import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

def plot_elbow(X, k_range, title):
    wcss = []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", random_state=42)
        km.fit(X)
        wcss.append(km.inertia_)
    plt.figure(figsize=(8, 4))
    plt.plot(k_range, wcss, 'o-')
    plt.title(title)
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("WCSS")
    plt.show()

def plot_clusters(X, labels, x_col, y_col, title, cmap=None):
    plt.figure(figsize=(8, 5))
    if cmap:
        sc = plt.scatter(X[x_col], X[y_col], c=labels, cmap=cmap, s=100)
        plt.colorbar(sc, label="Cluster")
    else:
        # categorical coloring
        unique = np.unique(labels)
        colors = plt.cm.tab10.colors
        for i in unique:
            mask = (labels == i)
            plt.scatter(
                X.loc[mask, x_col],
                X.loc[mask, y_col],
                s=100,
                color=colors[i % len(colors)],
                label=f"Cluster {i+1}"
            )
        plt.legend()
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def prepare_features(df, scale_cols, leave_cols):
    """scale only scale_cols; leave leave_cols untouched."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[scale_cols])
    df_scaled = pd.DataFrame(scaled, columns=scale_cols, index=df.index)
    return pd.concat([df_scaled, df[leave_cols]], axis=1)

def main():
    # 1. Load & encode
    data = {
        'vehicle_serial_no': [5,3,8,2,4,7,6,10,1,9],
        'mileage': [150000,120000,250000,80000,100000,220000,180000,300000,75000,280000],
        'fuel_efficiency': [15,18,10,22,20,12,16,8,24,9],
        'maintenance_cost': [5000,4000,7000,2000,3000,6500,5500,8000,1500,7500],
        'vehicle_type': ['SUV','Sedan','Truck','Hatchback','Sedan','Truck','SUV','Truck','Hatchback','SUV']
    }
    df = pd.DataFrame(data).drop(columns=['vehicle_serial_no'])
    df['vehicle_type'] = LabelEncoder().fit_transform(df['vehicle_type'])

    # Features for clustering
    X = df[['mileage','fuel_efficiency','maintenance_cost','vehicle_type']]

    # 2. Elbow (no scaling)
    plot_elbow(X, range(2, 11), "Elbow Method (No Scaling)")

    # 3. K-Means without scaling
    labels_ns = KMeans(n_clusters=3, init="k-means++", random_state=42).fit_predict(X)
    plot_clusters(df, labels_ns, "mileage", "fuel_efficiency",
                  "Vehicle Clusters (No Scaling)")

    # 4. Prepare scaled data (scale all numeric)
    X_scaled = prepare_features(df, 
                                ['mileage','fuel_efficiency','maintenance_cost','vehicle_type'],
                                leave_cols=[])
    labels_s = KMeans(n_clusters=3, random_state=42).fit_predict(X_scaled)
    plot_clusters(X_scaled, labels_s, "mileage", "fuel_efficiency",
                  "Vehicle Clusters (All Features Scaled)", cmap='viridis')

    # 5. Attach & show final DataFrame
    df['cluster_no_scale'] = labels_ns
    df['cluster_scaled'] = labels_s
    print("Final DataFrame with cluster labels:\n", df)

if __name__ == "__main__":
    main()
