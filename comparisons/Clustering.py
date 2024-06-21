from sklearn.cluster import KMeans
import numpy as np

def kmeans_clustering(data, n_clusters, n_init=10):
    best_kmeans = None
    best_inertia = np.inf

    for seed in range(n_init):
        kmeans = KMeans(n_clusters=n_clusters, random_state=seed)
        kmeans.fit(data)
        
        if kmeans.inertia_ < best_inertia:
            best_inertia = kmeans.inertia_
            best_kmeans = kmeans

    return best_kmeans