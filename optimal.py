
from sklearn.cluster import KMeans
from gap_statistic import OptimalK
import numpy as np
import matplotlib.pyplot as plt

# Elbow method, GAP Statistics
def findOptimal(reduced_data):
    ks = range(1, 25)
    inertias = []
    bp = reduced_data

    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters=k)

        # Fit model to samples
        model.fit(bp)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    # Plot ks vs inertias
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()

    # Gap Statistics
    optimalK = OptimalK(parallel_backend='joblib')
    n_clusters = optimalK(bp, cluster_array=np.arange(1, 26))

    print('Optimal clusters: ', n_clusters)

    plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df.gap_value, linewidth=3)
    plt.scatter(optimalK.gap_df[optimalK.gap_df.n_clusters == n_clusters].n_clusters,
                optimalK.gap_df[optimalK.gap_df.n_clusters == n_clusters].gap_value, s=1)
    plt.grid(True)
    plt.xlabel('Cluster Count')
    plt.ylabel('Gap Value')
    plt.title('Gap Values by Cluster Count')
    plt.show()
    return n_clusters
#
#
# # Gap Statistic for K means
# def optimalK(data, nrefs=3, maxClusters=15):
#     """
#     Calculates KMeans optimal K using Gap Statistic
#     Params:
#         data: ndarry of shape (n_samples, n_features)
#         nrefs: number of sample reference datasets to create
#         maxClusters: Maximum number of clusters to test for
#     Returns: (gaps, optimalK)
#     """
#     gaps = np.zeros((len(range(1, maxClusters)),))
#     resultsdf = pd.DataFrame({'clusterCount': [], 'gap': []})
#     for gap_index, k in enumerate(range(1, maxClusters)):
#         # Holder for reference dispersion results
#         refDisps = np.zeros(nrefs)
#         # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
#         for i in range(nrefs):
#             # Create new random reference set
#             randomReference = np.random.random_sample(size=data.shape)
#
#             # Fit to it
#             km = KMeans(k)
#             km.fit(randomReference)
#
#             refDisp = km.inertia_
#             refDisps[i] = refDisp
#         # Fit cluster to original data and create dispersion
#         km = KMeans(k)
#         km.fit(data)
#
#         origDisp = km.inertia_
#         # Calculate gap statistic
#         gap = np.log(np.mean(refDisps)) - np.log(origDisp)
#         # Assign this loop's gap statistic to gaps
#         gaps[gap_index] = gap
#
#         resultsdf = resultsdf.append({'clusterCount': k, 'gap': gap}, ignore_index=True)
#
# score_g, df = optimalK(cluster_df, nrefs=5, maxClusters=30)
# plt.plot(df['clusterCount'], df['gap'], linestyle='--', marker='o', color='b');
# plt.xlabel('K');
# plt.ylabel('Gap Statistic');
# plt.title('Gap Statistic vs. K');
