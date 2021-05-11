class tile(object):
	"""docstring for tile"""
	def __init__(self, x, y, path):
		self.x = x # x dihitung dari kiri ke kanan dimuali dari 0
		self.y = y # y di hitiung dari atas ke bawah, dimulai dengan 0
		self.path = path # Boolean, menyatakan apakah path true atau false
		self.adj = [] # Adjacent tiles, filled with tuples node coordinates
	# 	self.target = False # Boolean, menyatakan goal node
	# 	self.unit = None # Entitas yang mencari object


	# def getCharacter(self):
	# 	if (self.target == True):
	# 		return "T"
	# 	elif (self.path == True):
	# 		return "o"
	# 	elif(self.path == False):
	# 		return "x"



