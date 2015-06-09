
import sys
import math
import random
import subprocess
import matplotlib.pyplot as plt


def main():
	
	num_points = 1000
	dimensions = 2
	lower = 0
	upper = 200
	num_clusters = 4
	opt_cutoff = 1.0
	
	points = [makeRandomPoint(dimensions, lower, upper) for i in xrange(num_points)]
	
	clusters = kmedoid(points, num_clusters, opt_cutoff)
	
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
		self.medoid = self.calculateMedoid()

		
	def __repr__(self):
	
		return str(self.points)
	
	def update(self, points):
		
		
		old_medoid = self.medoid
		self.points = points
		self.medoid = self.calculateMedoid()
		shift = getDistance(old_medoid, self.medoid)
		return shift

	def cmp(a,b):
		dista =0.0
		distb = 0.0
		for i in range(a.n):
			dista +=a.coords[i]*a.coords[i]
			distb +=b.coords[i]*b.coords[i]
		if distb > dista:
			return 1
		else:
			return 0
	
	def calculateMedoid(self):
		min_medoid = self.points[0]
		min_dist = 0.0
		for j in self.points:
			min_dist += getDistance(j,min_medoid)
		for i in range(1,len(self.points)):
			dist = 0.0
			for j in self.points:
				dist += getDistance(j,self.points[i])
			if dist <min_dist:
				min_dist = dist
				min_medoid = self.points[i] 
		return min_medoid


def kmedoid(points, k, cutoff):
	
	initial = random.sample(points, k)
	clusters = [Cluster([p]) for p in initial]
	counter = 0
	
	while True:
		
		lists = [[] for c in clusters]
		clus_count = len(clusters)
		counter+=1
		for p in points:
			
			smallest_distance = getDistance(p, clusters[0].medoid)
			clusterIndex = 0
			
			for i in range(clus_count-1):
				
				distance = getDistance(p, clusters[i+1].medoid)
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
			new_dist=get_Cluster_distance(clusters[i],clusters[j])
			distance=min(distance, new_dist)

	for i in range(k):
		numPoints = len(clusters[i].points)
		dist2 = 0
		for j in clusters[i].points:
			for v in clusters[i].points:
				dist2=max(dist2, getDistance(j, v))

	dunn_index = distance/dist2		
	print str(dunn_index)


def get_cluster_Distance(a, b):

	dist = 0.0
	for i in a.points:

		for j in b.points:
			if getDistance(i,j) == 0:
				continue
			dist = min(dist, getDistance(i, j))


	return dist

def davies(k, clusters):
	db = 0.0
	for i in range(k):
		
		s_i = 0.0

		for p in clusters [i].points:
			
			s_i += getDistance(p, clusters[i].medoid)
		s_i = s_i/len(clusters[i].points)
		r_i = 0.0
		for j in range(i+1,k):

			d_ij=getDistance(clusters[i].medoid,clusters[j].medoid)
			s_j = 0.0

			for p in clusters[j].points:
				
				s_j += getDistance(p, clusters[j].medoid)
			s_j = s_j/len(clusters[j].points)

			r_i = max(r_i, ((s_i + s_j)/d_ij))

		db += r_i

	db = db/k

	print str(db)


			
	
if __name__=="__main__":
	main()
			
			
				
		
	
		
