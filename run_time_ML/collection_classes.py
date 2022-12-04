# Python program to print DFS traversal for complete graph
from collections import defaultdict

# This class represents a directed graph using adjacency
# list representation
class Graph:

	# Constructor
	def __init__(self):

		# default dictionary to store graph
		self.graph = defaultdict(list)

	# function to add an edge to graph
	def addEdge(self,u,v):
		self.graph[u].append(v)

	# A function used by DFS
	def DFSUtil(self, v, visited):

		# Mark the current node as visited and print it
		visited[v]= True
		print(v)

		# Recur for all the vertices adjacent to
		# this vertex
		for i in self.graph[v]:
			if visited[i] == False:
				self.DFSUtil(i, visited)


	# The function to do DFS traversal. It uses
	# recursive DFSUtil()
	def DFS(self):
		V = len(self.graph) #total vertices

		# Mark all the vertices as not visited
		visited =[False]*(V)

		# Call the recursive helper function to print
		# DFS traversal starting from all vertices one
		# by one
		for i in range(V):
			if visited[i] == False:
				self.DFSUtil(i, visited)



class Tree:
	
	def __init__(self):
		self.root = None
		self.left = None
		self.right = None

	def children(self, tree):
		return [tree.left, tree.right]

	def addLeft(self, left):
		self.left = left

	def addRight(self, right):
		self.right = right	

	def search_tree(self, tree, node):
		if tree is None:
			return False
		if tree.root == node:
			return True
		return self.search_tree(tree.left, node) or self.search_tree(tree.right, node)


