from tile import tile
from copy import deepcopy
from unit import unit
from time import sleep
from target import target	

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

class gamemap(object):
	"""docstring for gamemap"""
	def __init__(self, *args):
		self.map = []
		if (len(args) == 1): #Argumen berupa filename
			filename = args[0]
			f = open(filename)
			firstLine = f.readline().replace("\n","").split(" ")
			self.length = int(firstLine[0])
			self.width = int(firstLine[1])

			for i in range(self.width):
				baris = []
				listFromRead = f.readline().replace("\n","").split(" ")
				for j in range(self.length):
					if (listFromRead[j] == "x"):
						baris.append(tile(j,i,False))
					else:
						baris.append(tile(j,i,True))
				self.map.append(baris)
			print("Hi")
			self.linkPath()

		elif (len(args) == 2): #Argunem berupa length, width
			self.length = args[0]
			self.width = args[1]
			for i in range(self.width):
				baris = []
				for j in range(self.length):
					baris.append(tile(j,i,True))
				self.map.append(baris)
			# self.map[self.width//2][self.length//2].path = False
			# self.map[0][self.length//2].path = False
			# self.map[1][self.length//2].path = False
			# self.map[3][self.length//2].path = False
			# self.map[0][3].path = False
			# self.map[2][1].path = False
			# self.map[2][2].path = False
			# self.map[1][3].path = False
			# self.map[2][0].path = False

		# self.map[4][length//2].path = False
			self.linkPath()

		else:
			print("Error")
			raise Exception("constructor harus berisi length dan width atau nama file")

	def euclideanNode(self, node1Coor, node2Coor):
		node1X = node1Coor[0]
		node1Y = node1Coor[1]
		node2X = node2Coor[0]
		node2Y = node2Coor[1]
		return (( (node1X - node2X)**2 + (node1Y - node2Y)**2 )**0.5)

	def mapTile(self,x,y):
		return self.map[y][x]

	def linkPath(self):
		for baris in self.map:
			for tile in baris:
				if (tile.path):
					# print(tile.x, end=" ")
					# print(tile.y)
					if (tile.x > 0):
						if (self.mapTile(tile.x-1,tile.y).path == True):
							tile.adj.append((tile.x-1, tile.y))

					if (tile.x < self.length-1):
						if (self.mapTile(tile.x+1,tile.y).path == True):
							tile.adj.append((tile.x+1, tile.y))
					if (tile.y > 0 ):
						if (self.mapTile(tile.x,tile.y-1).path == True):
							tile.adj.append((tile.x, tile.y-1))

					if (tile.y < self.width-1 ):
						if (self.mapTile(tile.x,tile.y+1).path == True):
							tile.adj.append((tile.x, tile.y+1))

	def showMap(self):
		for baris in self.map:
			for tile in baris:
				if (tile.path):
					print("o", end=" ")
				else:
					print("x", end=" ")
			print()

	def showPath(self,path):
		for baris in self.map:
			for tile in baris:
				if ( (tile.x,tile.y) in path):
					print("P", end=" ")
				elif (tile.path):
					print("o", end=" ")
				else:
					print("x", end=" ")
			print()

	def astar(self,startNode,goalNode):
		#Startnode and goalNode is a tuple of coordinates
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
			currentNodeName = currentNode[0]

			currentNodecost = currentNode[1]
			nextNodeHistory = currentNode[2]
			nextNodeHistory.append(currentNodeName)



			TuplesToBeProcessed = self.mapTile(currentNodeName[0],currentNodeName[1]).adj # List of Coordinates of tiles
			nodesToBeProcessed = [] # Coordinates of tiles
			for nodeTuples in TuplesToBeProcessed:
				if nodeTuples not in nextNodeHistory:
					nodesToBeProcessed.append(nodeTuples)


			for i in nodesToBeProcessed:				
				# print("Processing: "+str(i))
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
		return (costSoFar+estimatedCostToGoal)

	def findPathValue(self,path):
		#path merupakan list of nodeName, yang sudah pasti ada
		return len(path)


# g = gamemap(10,5)


# g.mapTile(5,2).path = False
# print(g.mapTile(1,0).adj)
# g.showMap()

# print(g.fungsiHeuristik((8,4),(8,5),[]))
# print(g.astar((8,4),(8,5)))

# g = gamemap("map.txt")
# u1 = unit(5,4,g.map, "UCS")
# t = target(5,7,g.map)
# u1.showMap(t.pos)

# g = gamemap(12,9)
# u1 = unit(2,4,g.map, "UCS")
# t = target(9,4,g.map)
# u1.showMap(t.pos)

g = gamemap("map2.txt")
u1 = unit(0,0,g.map, "greedy")
t = target(8,0,g.map)
u1.showMap(t.pos)

print()

print("Press any key to continue")
targetMove = 2
userInput = input()
while(userInput != 0 and u1.alive):
	path = u1.move(t.pos)

	targetMove = targetMove + 1
	if (targetMove >= 2):
		targetMove = 0
		t.move()
	print()
	# sleep(0.5)

print(u1.processedNodesCount)
print(u1.moveCount)
print("Rata-rata node yang di process per move:")
print(u1.processedNodesCount/u1.moveCount)
# u1.showPath(path)

# g.mapTile(2,0).path = False
# g.mapTile(1,1).path = False
# g.mapTile(2,1).path = False
# g.mapTile(3,1).path = False

# print(g.astar((0,0), (1,0)))
# path = g.astar((4,2), (3,4))
# path = g.astar((0,0), (9,3))
# g.showPath(path)