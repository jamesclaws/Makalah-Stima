from random import randint

class target(object):
	"""docstring for target"""
	def __init__(self, x,y,Map):
		self.x = x
		self.y = y
		self.pos = (self.x, self.y)
		self.map = Map

	def mapTile(self,x,y):
		return self.map[y][x]

	def move(self):
		randomNumber = randint(0,len(self.mapTile(self.x, self.y).adj)-1)
		self.x = self.mapTile(self.x, self.y).adj[randomNumber][0]
		self.y = self.mapTile(self.x, self.y).adj[randomNumber][1]
		self.pos = (self.x, self.y)
