import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def plot_elbow(X, k_range, title):
    wcss = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X)
        wcss.append(km.inertia_)
    plt.figure(figsize=(8, 4))
    plt.plot(k_range, wcss, 'o-')
    plt.title(title)
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("WCSS")
    plt.show()

def plot_silhouette(X, k_range):
    scores = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42)
        labels = km.fit_predict(X)
        scores.append(silhouette_score(X, labels))
    plt.figure(figsize=(8, 4))
    plt.plot(k_range, scores, 'o-')
    plt.title("Silhouette Scores")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.show()

def plot_clusters(X, labels, x_col, y_col, title, cmap=None):
    plt.figure(figsize=(8, 5))
    if cmap:
        sc = plt.scatter(X[x_col], X[y_col], c=labels, cmap=cmap, s=50)
        plt.colorbar(sc, label="Cluster")
    else:
        colors = plt.cm.tab10.colors
        for i in np.unique(labels):
            mask = labels == i
            plt.scatter(X.loc[mask, x_col], X.loc[mask, y_col],
                        color=colors[i % len(colors)],
                        label=f"Cluster {i}")
        plt.legend()
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def main():
    # 1. Generate synthetic student data
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        'student_id': [f"S{1000+i}" for i in range(n)],
        'GPA': np.round(np.random.normal(3.0, 0.5, n).clip(1.0, 4.0), 2),
        'study_hours': np.round(np.random.normal(15, 5, n).clip(5, 30), 1),
        'attendance_rate': np.round(np.random.normal(80, 10, n).clip(50, 100), 1)
    })

    # 2. Feature scaling
    features = ['GPA', 'study_hours', 'attendance_rate']
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(df[features]),
                            columns=features, index=df.index)

    # 3. Elbow & Silhouette analyses
    ks = range(2, 11)
    plot_elbow(X_scaled, ks, "Elbow Method (Scaled Features)")
    plot_silhouette(X_scaled, ks)

    # 4. Choose k (e.g. silhouette peak or elbow): here k=4
    k_opt = 4
    km = KMeans(n_clusters=k_opt, random_state=42)
    df['cluster'] = km.fit_predict(X_scaled)

    # 5. Visualize clusters
    plot_clusters(df, df['cluster'], 'study_hours', 'GPA',
                  f"Student Clusters (k={k_opt})", cmap='viridis')

    # 6. Show final table
    print(df[['student_id', 'GPA', 'study_hours', 'attendance_rate', 'cluster']])

if __name__ == "__main__":
    main()
