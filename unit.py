from copy import deepcopy

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([(str(i[0])+":"+str(i[1])) for i in self.queue])
  
    def isEmpty(self):
    	if (len(self.queue) == 0):
    		return True
    	else:
    		return False


    def insert(self, nodeTuple):
    	#nodeTuple = (namaNode,h(x), [ListOfPassedNodes] )
        self.queue.append(nodeTuple)
  
    def dequeue(self):
    	if (self.isEmpty()):
    		print("Queue is Empty")
    	else:
            min = 0
            for i in range(len(self.queue)):
                if (self.queue[i][1] < self.queue[min][1]):
                    min = i
            node = self.queue[min]
            del self.queue[min]
            return node

    def clear(self, minCost):
    	#Used to remove every nodeTuple whose heurstik value is higher than minCost
        idx = 0
        while(idx < len(self.queue)):
            if (self.queue[idx][1] > minCost):
                del self.queue[idx]
                idx = 0
            else:
                idx = idx+1

class unit(object):
	"""docstring for unit"""
	def __init__(self, x,y,Map,pathMethod = "astar"):
		self.x = x
		self.y = y
		self.map = Map
		self.alive = True
		self.moveCount = 0
		self.processedNodesCount = 0
		if (pathMethod == "astar" or pathMethod == "greedy" or pathMethod == "UCS"):
			self.pathMethod = pathMethod
		else:
			self.pathMethod = "astar"

	def mapTile(self,x,y):
		return self.map[y][x]

	def euclideanNode(self, node1Coor, node2Coor):
		node1X = node1Coor[0]
		node1Y = node1Coor[1]
		node2X = node2Coor[0]
		node2Y = node2Coor[1]
		return (( (node1X - node2X)**2 + (node1Y - node2Y)**2 )**0.5)

	def astar(self,startNode,goalNode):
		#Startnode and goalNode is a tuple of coordinates

		if (startNode == goalNode):
			return []

		startNodeTile = None
		goalNodeTile = None

		try:
			startNodeTile = self.mapTile(startNode[0],startNode[1])
			goalNodeTile = self.mapTile(goalNode[0],goalNode[1])
		except Exception:
			raise Exception("Start node or goal Node out of bounds")		

		if (startNodeTile == None or goalNodeTile == None):
			raise Exception("Start node or goal Node doesn't exist")


		PQ = PriorityQueue()

		PQ.insert((startNode, self.fungsiHeuristik(startNode, goalNode, []), []))
		# minCost = self.fungsiHeuristik(startNode, goalNode, [])
		minCost = None

		goalPath = []

		while(not PQ.isEmpty()):
			currentNode = PQ.dequeue()
			# print("Expanding: ("+ str(currentNode[0]) +","+ str(currentNode[1]) +") ...")
			# print(minCost)
			currentNodeName = currentNode[0]

			currentNodecost = currentNode[1]
			nextNodeHistory = currentNode[2]
			nextNodeHistory.append(currentNodeName)

			if (self.pathMethod == "greedy"):
				PQ.clear(currentNodecost)


			TuplesToBeProcessed = self.mapTile(currentNodeName[0],currentNodeName[1]).adj # List of Coordinates of tiles
			nodesToBeProcessed = [] # Coordinates of tiles
			for nodeTuples in TuplesToBeProcessed:
				if nodeTuples not in nextNodeHistory:
					nodesToBeProcessed.append(nodeTuples)


			for i in nodesToBeProcessed:				
				# print("Processing: "+str(i))
				self.processedNodesCount = self.processedNodesCount + 1
				if (i == goalNode):
					nextNodeHistory.append(goalNode)
					
					if (not goalPath):
						goalPath = nextNodeHistory
						minCost = self.findPathValue(nextNodeHistory)
					elif (self.findPathValue(nextNodeHistory) < self.findPathValue(goalPath)):
						goalPath = nextNodeHistory
						minCost = self.findPathValue(nextNodeHistory)
					
					PQ.clear(minCost)
				else:
					if (self.fungsiHeuristik(i, goalNode, nextNodeHistory) != 0):
						newHistory = deepcopy(nextNodeHistory)
						if (minCost == None):
							PQ.insert((i, self.fungsiHeuristik(i, goalNode, newHistory), newHistory))
						elif (minCost >= self.fungsiHeuristik(i, goalNode, newHistory)):
							PQ.insert((i, self.fungsiHeuristik(i, goalNode, newHistory), newHistory))
			nextNodeHistory = []
			

		return(goalPath)


	def fungsiHeuristik(self,nodeName1,nodeName2,ListOfPassedNodes):
		#ListOfPassedNodes is a list of string		
		costSoFar = len(ListOfPassedNodes)
		estimatedCostToGoal = self.euclideanNode(nodeName1,nodeName2)
		if (self.pathMethod == "greedy"):
			# print("greedy")
			return estimatedCostToGoal
		if (self.pathMethod	 == "UCS"):
			# print("UCS")
			return	costSoFar
		return (costSoFar+estimatedCostToGoal)

	def findPathValue(self,path):
		#path merupakan list of nodeName, yang sudah pasti ada
		return len(path)


	def move(self,goalNode):
		if (self.alive):
			path = self.astar( (self.x, self.y), goalNode )
			if (len(path) == 0):
				self.alive = False
				return []
			if (len(path) > 1):
				self.moveCount = self.moveCount + 1
				self.x = path[1][0]
				self.y = path[1][1]
				path = path[1:]
				self.showPath(path)
				if (len(path) == 1): #Sudah ketemu target
					self.alive = False
			
			return path
		return []

	def showMap(self, goalNode):
		for baris in self.map:
			for tile in baris:
				if (tile.x == self.x and tile.y == self.y):
					print("U", end= " ")
				elif ( (tile.x, tile.y) == goalNode):
					print("T", end= " ")
				elif (tile.path):
					print("o", end=" ")
				else:
					print("x", end=" ")
			print()

	def showPath(self,path):
		if (self.alive):
			for baris in self.map:
				for tile in baris:
					if (tile.x == self.x and tile.y == self.y):
						print("U", end= " ")
					elif ( (tile.x, tile.y) == path[-1] ):
						print("T", end= " ")
					elif ( (tile.x,tile.y) in path):
						print("P", end=" ")
					elif (tile.path):
						print("o", end=" ")
					else:
						print("x", end=" ")
				print()