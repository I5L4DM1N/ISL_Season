class Favorite_status(object):
	"""docstring for Favorite_status"""
	def __init__(self, name):
		super(Favorite_status, self).__init__()
		self.name = name

	def __str__(self):
		return "{}".format(self.name)
		
Normal = Favorite_status("Normal")
Favorite = Favorite_status("Favorite")
Underdog = Favorite_status("Underdog")
Big_favorite = Favorite_status("Big_favorite")
Big_underdog = Favorite_status("Big_underdog")

class Status(object):
	"""docstring for Status"""
	def __init__(self,name):
		super(Status, self).__init__()
		self.name = name

	def __str__(self):
		return "{}".format(self.name)



Big_lead = Status("Big_lead")
Lead = Status("Lead")
Equal = Status("Equal")
Losing = Status("Losing")
Losing_big = Status("Losing_big")

def Status_determination(team1_score,team2_score):
	if team1_score - team2_score > 1 :
		return Big_lead
	elif team1_score - team2_score > 0 :
		return Lead
	elif team1_score - team2_score == 0:
		return Equal
	elif team1_score - team2_score < - 1 :
		return Losing_big
	elif team1_score - team2_score < 0 :
		return Losing
	


class Status_change(object):
	"""docstring for Status_change"""
	def __init__(self,name):
		super(Status_change, self).__init__()
		self.name = name
		

	def __str__(self):
		return "{}".format(self.name)
			

keeping_lead = Status_change("keeping_lead")
increased_lead = Status_change("increased_lead")
decreased_lead = Status_change("decreased_lead")
lost_lead = Status_change("lost_lead")
new_lead = Status_change("new_lead")
even = Status_change("even")
new_losing = Status_change("new_losing")
equalization = Status_change("equalization")
keep_losing = Status_change("keep_losing")
increased_losing = Status_change("increased_losing")
reduced_losing = Status_change("reduced_losing")

def Change_determination(score_difference,previous_score_difference):
	if score_difference > 0 and previous_score_difference > 0 and score_difference == previous_score_difference:
		return keeping_lead
	elif score_difference > 0 and previous_score_difference > 0 and score_difference > previous_score_difference:
		return increased_lead
	elif score_difference > 0 and previous_score_difference > 0 and score_difference < previous_score_difference:
		return decreased_lead
	elif score_difference == 0 and previous_score_difference > 0:
		return lost_lead
	elif score_difference > 0 and previous_score_difference == 0:
		return new_lead
	elif score_difference == 0 and previous_score_difference == 0:
		return even
	if score_difference < 0 and previous_score_difference == 0:
		return new_losing
	elif score_difference == 0 and previous_score_difference < 0:
		return equalization
	elif score_difference < 0 and previous_score_difference < 0 and score_difference == previous_score_difference:
		return keep_losing
	elif score_difference < 0 and previous_score_difference < 0 and score_difference < previous_score_difference:
		return increased_losing
	elif score_difference < 0 and previous_score_difference < 0 and score_difference > previous_score_difference:
		return reduced_losing
	
		
class Status_and_change(object):
	"""docstring for Status_and_change"""
	def __init__(self, name,Big_favorite,Favorite,Normal,Underdog,Big_underdog):
		super(Status_and_change, self).__init__()
		self.name = name
		self.test = "test successful"
		self.Big_favorite = Big_favorite
		self.Favorite = Favorite
		self.Normal = Normal
		self.Underdog = Underdog
		self.Big_underdog = Big_underdog

	def __str__(self):
		return "{}".format(self.name)

	def value_determination(self, favorite_status):
		if favorite_status == Big_favorite:
			return self.Big_favorite
		if favorite_status == Favorite:
			return self.Favorite
		if favorite_status == Normal:
			return self.Normal
		if favorite_status == Underdog:
			return self.Underdog
		if favorite_status == Big_underdog:
			return self.Big_underdog

Losing_big_keep_losing = Status_and_change("Losing_big_keep_losing",-0.02,-0.01,0,0,0)
Losing_big_increased_losing = Status_and_change("Losing_big_increased_losing",-0.02,-0.02,-0.01,-0.01,-0.01)
Losing_big_reduced_losing = Status_and_change("Losing_big_reduced_losing",0,0,0.01,0.01,0.02)
Losing_keep_losing = Status_and_change("Losing_keep_losing",-0.02,-0.02,-0.01,0,0.01)
Losing_reduced_losing = Status_and_change("Losing_reduced_losing",0,0,0.01,0.01,0.02)
Losing_new_losing = Status_and_change("Losing_new_losing",0.01,0.01,0.01,0.01,0.01)
Equal_even = Status_and_change("Equal_even",-0.02,-0.01,0,0.01,0.02)
Equal_lost_lead = Status_and_change("Equal_lost_lead",-0.02,-0.01,-0.01,0,0)
Equal_equalization = Status_and_change("Equal_equalization",0,0.01,0.01,0.02,0.02)
Lead_keeping_lead = Status_and_change("Lead_keeping_lead",-0.01,0,0,0.01,0.02)
Lead_new_lead = Status_and_change("Lead_new_lead",0,0,0.01,0.02,0.02)
Lead_decreased_lead = Status_and_change("Lead_decreased_lead",-0.02,-0.01,-0.01,-0.01,0)
Big_lead_keeping_lead = Status_and_change("Big_lead_keeping_lead",-0.01,-0.01,-0.01,0,0.01)
Big_lead_increased_lead = Status_and_change("Big_lead_increased_lead",0.01,0.01,0.01,0.02,0.02)
Big_lead_decreased_lead = Status_and_change("Big_lead_decreased_lead",-0.02,-0.02,-0.01,-0.01,0)


def Status_and_change_determination(Status,change):
	if Status == Losing_big and change == keep_losing:
		return Losing_big_keep_losing
	elif Status == Losing_big and change == increased_losing:
		return Losing_big_increased_losing
	elif Status == Losing_big and change == reduced_losing:
		return Losing_big_reduced_losing
	elif Status == Losing and change == keep_losing:
		return Losing_keep_losing
	elif Status == Losing and change == reduced_losing:
		return Losing_reduced_losing
	elif Status == Losing and change == new_losing:
		return Losing_new_losing
	elif Status == Equal and change == even:
		return Equal_even
	elif Status == Equal and change == lost_lead:
		return Equal_lost_lead
	elif Status == Equal and change == equalization:
		return Equal_equalization
	elif Status == Lead and change == keeping_lead:
		return Lead_keeping_lead
	elif Status == Lead and change == new_lead:
		return Lead_new_lead
	elif Status == Lead and change == decreased_lead:
		return Lead_decreased_lead
	elif Status == Big_lead and change == keeping_lead:
		return Big_lead_keeping_lead
	elif Status == Big_lead and change == increased_lead:
		return Big_lead_increased_lead
	elif Status == Big_lead and change == decreased_lead:
		return Big_lead_decreased_lead


