from sklearn.cluater import OPTICS
import numpy as np

def find_clusters():
    data = 
    
    cluster = OPTICS(min_samples=20, xi=0.05, min_cluster_size=0.05)
    cluster.fit(data)

    labels = clustering.labels_

    print("labels: ", labels)

if __name__ == '__main__':
    find_clusters()
