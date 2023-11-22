# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wcmIxV6HkHo6LoBIKhQJHiIXFPSYfSQO
"""

import pandas as pd
import re

text = pd.read_csv('https://raw.githubusercontent.com/shrutib55/hw3/main/usnewshealth.txt', sep = "|", header=None)

text = text[2]

text.replace( { r"#" : '' }, inplace= True, regex = True)

text.replace({r"@\w+" : ''}, inplace = True, regex = True)

text.replace({r'http\S+': ''}, inplace = True, regex = True)

text = text.str.lower()

"""K means"""

def jaccarddistance(p1, p2):
  point1 = set(p1.split())
  point2 = set(p2.split())
  intersection = len(point1 & point2)
  union = len(point1 | point2)
  return 1 - (intersection / union)

# Set the desired number of clusters (k)
k = 2

centroids = text.sample(n = k, replace = False).to_list()

print("Initial Centroids:")
print(centroids)

# Initialize old_centroids as an empty list
old_centroids = [None] * k

# Iterate until centroids converge
while old_centroids != centroids:
    #print("1")
    distances = text.apply(lambda x: [jaccarddistance(x, centroid) for centroid in centroids])
    dist = pd.DataFrame(distances.to_list())
    #print("2")

    # Assign each data point to the cluster with the nearest centroid
    labels = dist.idxmin(axis=1)
    labels.columns = ["Label"]
    #print("3")

    # Update old_centroids
    old_centroids = centroids.copy()
    SSE = 0
    for i in range(k):
      cluster_points = text.loc[labels == i]
      print("Cluster", i+1, ":", len(cluster_points))

      if not cluster_points.empty:
        centroid_new = cluster_points.apply(lambda x: sum([jaccarddistance(x, cp) for cp in cluster_points]))
        SSE = SSE + sum(cluster_points.apply(lambda x: sum([jaccarddistance(x, cp)**2 for cp in cluster_points])))

        centroid_index = centroid_new.idxmin()
        centroids[i] = text.loc[centroid_index]
print("SSE: ")
print(SSE)

print("Final Centroids:")
print(centroids)