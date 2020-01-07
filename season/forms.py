from django import forms

class Test_pageForm(forms.Form):
	post = forms.IntegerField(max_value = 10, min_value = 0, initial = 0)

class MatchForm(forms.Form):
	GameRound = forms.IntegerField(max_value = 10, min_value = 0, initial = 0)

class HomeForm(forms.Form):
	pass
	#GamesToPlay = forms.IntegerField(max_value = 10, min_value = 0, initial = 0)
		