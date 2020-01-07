
class Favorite_status(object):
	"""docstring for Favorite_status"""
	def __init__(self, name):
		super(Favorite_status, self).__init__()
		self.name = name
		
Normal = Favorite_status("Normal")
Favorite = Favorite_status("Favorite")
Underdog = Favorite_status("Underdog")
