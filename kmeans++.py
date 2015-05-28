import sys
import math
import random
import subprocess
import matplotlib.pyplot as plt


def main():
	
	num_points = 10000
	dimensions = 2
	lower = 0
	upper = 200
	num_clusters = 4
	opt_cutoff = 0.05
	
	points = [makeRandomPoint(dimensions, lower, upper) for i in xrange(num_points)]
	
	clusters = kmeans(points, num_clusters, opt_cutoff)
	
	for i,c in enumerate(clusters):
		for p in c.points:
			print " Cluster: ", i, "\t Point :", p
	davies(num_clusters, clusters)
	
class Point:
	
	def __init__(self, coords):
		
		self.coords = coords
		self.n = len(coords)
		
	
	def __repr__(self):
	
		return str(self.coords)
	

class Cluster:
	
	def __init__(self, points):
		
		self.points = points
		self.n = points[0].n
		self.centroid = self.calculateCentroid()
		
	def __repr__(self):
	
		return str(self.points)
	
	def update(self, points):
		
		
		old_centroid = self.centroid
		self.points = points
		self.centroid = self.calculateCentroid()
		shift = getDistance(old_centroid, self.centroid)
		return shift
	
	def calculateCentroid(self):
		
		numPoints = len(self.points)
		coords = [p.coords for p in self.points]
		unzipped = zip(*coords)
		centroid_coords = [math.fsum(x)/numPoints for x in unzipped]
		return Point(centroid_coords)
	

def kmeans(points, k, cutoff):
	
	initial = cluster_initialize(points, k)
	
	clusters = [Cluster([p]) for p in initial]
	counter = 0
	
	while True:
		
		lists = [[] for c in clusters]
		clus_count = len(clusters)
		counter+=1
		for p in points:
			
			smallest_distance = getDistance(p, clusters[0].centroid)
			clusterIndex = 0
			
			for i in range(clus_count-1):
				
				distance = getDistance(p, clusters[i+1].centroid)
				if distance < smallest_distance:
					
					smallest_distance = distance
					clusterIndex = i+1
				
			
			lists[clusterIndex].append(p)
		biggest_shift = 0.0
			
		for i in range(clus_count):
				
			shift = clusters[i].update(lists[i])
			if biggest_shift < shift:
					
				biggest_shift = shift
				
		if biggest_shift < cutoff:
				
			break
		
	return clusters
		
	
def getDistance(a, b):
	
		ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
		return math.sqrt(ret)

def makeRandomPoint(n, lower, upper):
	
	p = Point([random.uniform(lower, upper) for i in range(n)])
	return p

def dunn(k, clusters):

	distance = 200
	for i in range(k):
		for j in range(i+1,k):
			new_dist=getDistance(clusters[i].centroid,clusters[j].centroid)
			distance=min(distance, new_dist)

	for i in range(k):
		numPoints = len(clusters[i].points)
		dist2 = 0
		for j in clusters[i].points:
			for v in clusters[i].points:
				dist2=max(dist2, getDistance(j, v))

	dunn_index = distance/dist2		
	print str(dunn_index)
def davies(k, clusters):
	db = 0.0
	for i in range(k):
		
		s_i = 0.0

		for p in clusters [i].points:
			
			s_i += getDistance(p, clusters[i].centroid)
		s_i = s_i/len(clusters[i].points)
		r_i = 0.0
		for j in range(i+1,k):

			d_ij=getDistance(clusters[i].centroid,clusters[j].centroid)
			s_j = 0.0

			for p in clusters[j].points:
				
				s_j += getDistance(p, clusters[j].centroid)
			s_j = s_j/len(clusters[j].points)

			r_i = max(r_i, ((s_i + s_j)/d_ij))

		db += r_i

	db = db/k

	print str(db)

def cluster_initialize(points, k):

	initial = random.sample(points, 1)
	lists = []
	#print str(initial)
	lists.append(initial[0])
	#print str(lists[0].coords)
	for i in range(k-1):
		initial = random.sample(points, 1)
		maxp = initial[0]
		maxd = 0.0
		for p in points:
			
			dist = getDistance(lists[0], p)
			for j in range(len(lists)-1):
				
				dist = min(dist, getDistance(lists[j+1], p))

			if dist > maxd :

				maxd = dist
				maxp = p

		lists.append(maxp)

	return lists



	
	
if __name__=="__main__":
	main()
			
			
				
		
	
		
