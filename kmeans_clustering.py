import math
import random
from matplotlib import colors
from matplotlib.colors import cnames
import numpy as np
import matplotlib.pyplot as plt

def initializePoints(count):
    points = []
    for i in range(int(count/3)):
        points.append([random.gauss(0,10),random.gauss(100,10)])
    for i in range(int(count/3)):
        points.append([random.gauss(-30,20),random.gauss(10,10)])
    for i in range(int(count/3)):
        points.append([random.gauss(30,20),random.gauss(10,10)])

    return points

# function to experiment with different sigma and mean values
def initializePoints_random(count):
    points = []
    for i in range(int(count/3)):
        points.append([random.gauss(-25,20),random.gauss(0,20)])
    for i in range(int(count/3)):
        points.append([random.gauss(0,40),random.gauss(80,10)])
    for i in range(int(count/3)):
        points.append([random.gauss(20,20),random.gauss(150,20)])

    return points

# to calculate the eucledian distance
def euc_dist(point, centroid):
    return(math.sqrt((point[0] - centroid[0])**2 + (point[1] - centroid[1])**2 ))

# to check the currrent centroids are equal to prevoius centroids or not
def check(past,current):
    count=0
    t_keys=0
    for keys in past:
        t_keys+=1
        for t in current:
            # if distance is negligible, increment count
            if euc_dist(keys,t)<0.75:
                count+=1
                break
    # if all centroids are not changing, return false
    if count==t_keys:
        return False
    return True

# to cluster a given dataset
def cluster(points,K,visuals = True):
    clusters=[]
    #Your kmeans code will go here to cluster given points in K clsuters. If visuals = True, the code will also plot graphs to show the current state of clustering
    # plot iteration 0
    if(visuals):
        x, y = zip(*points)
        plt.scatter(x, y, color='black', marker="+")
        plt.title("Iteration 0")
        plt.show()
    
    centroids = dict()
    past_centroids = dict()
    
    # initializing random k centroids
    iterations = 0
    if (iterations == 0):
        for i in range(K):
            temp = points[random.randrange(0, len(points))]
            centroids[(temp[0], temp[1])] = []
    
    # setting past centroids with large values
    for keys in centroids:
        past_centroids[(random.randrange(10000, 200000), random.randrange(10000, 200000))] = []
    
    # for updating centroids of k-clusters untill no minimun change in distance is observed 
    while(check(past_centroids,centroids)==True):
        if (iterations != 0):
            past_centroids = centroids
            centroids = dict()
            # generating new centroids (cluster centers)
            for key in past_centroids:
                # get all x, y
                x = []
                y = []
                point_lst = past_centroids[key]
                for i in range(len(point_lst)):
                    x.append(point_lst[i][0])
                    y.append(point_lst[i][1])
                # avg cluster to get mean point(centroid)
                mean_x = sum(x) / len(x)
                mean_y = sum(y) / len(y)
                centroids[(mean_x, mean_y)] = []
        # calculating new clusters (assign points to the new clusters via min distance)
        for point in range(len(points)):
            min_dist = math.inf
            choosen_center = list(centroids.keys())[0] # initially choosing first centroid
            for each_centroid in centroids:
                curr_dist = euc_dist(points[point], each_centroid)
                if(curr_dist < min_dist):
                    choosen_center = each_centroid
                    min_dist = curr_dist
            centroids[choosen_center].append(points[point])

        iterations += 1

        # plotting the cluster dataset
        if(visuals):
            clr = ['red','green','blue', 'pink', 'yellow', 'purple', 'orange', 'grey', 'violet']
            i = 0
            for centroid in centroids:
                lst = centroids[centroid]
                # print("lst = ", lst)
                if(len(lst) != 0):
                    x, y = zip(*lst)
                    plt.scatter(x,y , color=clr[i], marker="+")
                    i += 1
                    if (i > len(clr) -1):
                        i = 0
                plt.scatter(centroid[0], centroid[1], color='black', marker="D")

            plt.title("Iteration "+str(iterations))
            plt.show()

    
    return centroids



def clusterQuality(clusters):
    score = -1 
    score_lst = []
    #Your code to compute the quality of cluster will go here.
    # calculate mean square error for each cluster
    for cluster in clusters:
        total_cluster_dist = 0
        num_points = 0 # get number of points for each clustering
        # for each point in the cluster, compute mse from its centroid
        for key in cluster.keys():
            each_key_dist = 0
            points = cluster[key]
            num_points += len(points)
            for point in points:
                each_key_dist += (euc_dist(point, key))**2
            total_cluster_dist += each_key_dist
        score_lst.append(total_cluster_dist/num_points)


    # best score is the one with least mse
    score = min(score_lst)
    print("Computing score for each clustering through mean square error")
    print("Score list is :", score_lst)
    return score
    
def keepClustering(points,K,N,visuals):
    clusters = []
    
    #Write you code to run clustering N times and return the formation having the best quality. 
    for n in range(N):
        clusters.append(cluster(points, K, visuals))
    
    return clusters

K = 3
N = 10

points = initializePoints(1000)

clusters = keepClustering(points,K,N,False)

print ("The score of best Kmeans clustering is:", clusterQuality(clusters))

