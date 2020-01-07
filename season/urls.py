from django.urls import path, re_path
from . import views
#import re

app_name = 'season'

urlpatterns = [
	#start page
	path('',views.StartView.as_view(), name ='start'),

	#match schedule
	path('calendar/',views.CalendarView.as_view(), name ='calendar'),

	#test_page
	path('test_page/',views.TestPageView.as_view(), name = 'test_page'),

	#individual match
	path('match/<int:GameID>/round/<int:GameRound>/',views.MatchView.as_view(), name = 'match'),

	#individual match - squads
	path('match/<int:GameID>/round/<int:GameRound>/squads',views.MatchSquadsView.as_view(), name = 'matchsquads'),

	#individual match - stats
	path('match/<int:GameID>/round/<int:GameRound>/stats',views.MatchStatsView.as_view(), name = 'matchstats'),

	#individual match - table
	path('match/<int:GameID>/round/<int:GameRound>/table',views.MatchTableView.as_view(), name = 'matchtable'),

	#league table
	path('league/',views.LeagueView.as_view(), name = 'league'),

	#cup_tree
	path('cup/',views.CupView.as_view(), name = 'cup'),

	#player_stat
	path('players/',views.PlayersList.as_view(), name = 'players'),
	
	# #individual player_stat
	re_path(r'^players/(?P<Name>[\w\W ]+?)/$',views.PlayerDeatail.as_view(), name = 'player'),

	#team_stat
	path('teams/',views.TeamsList.as_view(), name = 'teams_list'),
	
	# #individual team_stat
	#re_path(r'^teams/(?P<Name>[\w\W ]+?)/$',views.TeamDetail.as_view(), name = 'team_detail'),
	path('teams/<int:pk>/',views.TeamDetail.as_view(), name = 'team_detail'),

	# #update individual team_stat
	#re_path(r'^teams/(?P<Name>[\w\W ]+?)/update/$',views.TeamUpdate.as_view(), name = 'team_update'),
	path('teams/<int:pk>/update/',views.TeamUpdate.as_view(), name = 'team_update'),
	# #individual player_stat
	# path(r'players/<str:id>',views.PlayerView.as_view(), name = 'player'),

	] 