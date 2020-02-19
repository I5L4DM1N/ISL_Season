from django.views import generic
from .models import *
from season.forms import Test_pageForm, MatchForm, HomeForm
from django.shortcuts import render, get_object_or_404, redirect
from season.MatchGenerator import Matchgenerator, Fitness_recovery, Motivation_update, Day_loop, update_cup_schedule, update_division_table
from season.MatchGenerator.DatabaseChanges import Reset_Database
from season.MatchGenerator.DatabaseChanges import Save_and_load_progress
from django.db.models import Avg, Max, Q
from collections import defaultdict
from math import *
import pandas as pd
import numpy as np
import os
 

connection_string = {
    'host': os.environ.get('DB_HOST'),
    'database':'isl',
    'user': os.environ.get('DB_USER'),
    'password':os.environ.get('DB_PASS'),
    'ssl_ca': os.environ.get('SSL_CA_DIR'),
    'ssl_cert': os.environ.get('SSL_CERT_DIR'),
    'ssl_key': os.environ.get('SSL_KEY_DIR')
    }


class StartView(generic.list.ListView):
    template_name = "season/start.html"

    def get(self,request):
        # all_matches = GeneralSchedule.objects.all()
        # days = DayTable.objects.all().filter(Status='Future')
        # current_day = DayTable.objects.get(Status='Current')
        # if current_day ==None:
        #     current_day = DayTable.objects.all().filter(Status='Past').last()
        # weeks = DayTable.objects.all().filter(Status='Future').last()
        # no_of_days = len(days)
        # next_game = GeneralSchedule.objects.filter(Played=False).first()
        context = {}
        return render(request,self.template_name,context)

    def post(self,request):
        if "PlayFullSeason" in request.POST:
            start_day = DayTable.objects.get(Status='Current')
            end_week = DayTable.objects.all().filter(Status='Future').last()
            start_week = start_day.Week
            end_week = end_week.Week + 1

            for week in range(start_week,end_week):
                first_day = DayTable.objects.all().filter(Week=week).first()
                last_day = DayTable.objects.all().filter(Week=week).last()
                
                for day in range(first_day.Day,last_day.Day+1):
                    no_of_matches = len(GeneralSchedule.objects.all().filter(Day = day,Played =False))
                    
                    if no_of_matches > 0:
                        for game in range(0,no_of_matches):
                            Matchgenerator.Full_game(connection_string)

                    Motivation_update.Motivation_update(connection_string, day)
                    Fitness_recovery.Recovery(connection_string, day)
                    
                    Day_loop.Change_of_Day(connection_string, day)

                #update division table
                update_division_table.weekly_update(connection_string,week)
                #update cup schedule
                update_cup_schedule.cup_update(connection_string)

        elif "ReSetGames" in request.POST:
            Reset_Database.ReSetAll()



        return redirect("season:start")


class CalendarView(generic.list.ListView):
    template_name = "season/calendar.html"
    # context_object_name = "all_matches" 
 
    def get(self,request):
        form = HomeForm()
        try:
            current_day = DayTable.objects.get(Status='Current')
        except DayTable.DoesNotExist:
            current_day = DayTable.objects.all().filter(Status='Past').last()
        last_day = current_day.Day-1
        all_matches = GeneralSchedule.objects.filter(Day = current_day.Day)

        Tournaments = Tournament.objects.all().order_by("-id")

        #doesn't work until page is reloaded
        if not all_matches:
            Day_loop.Set_End_of_Day(connection_string, current_day.Day)
            TypeOfDay = "Not Match Day"
            Division_table = None

        last_game = GeneralSchedule.objects.filter(Played=True).last()
        next_game = GeneralSchedule.objects.filter(Played=False).first()

        if all_matches:
            if not next_game:
                if last_game.TournamentName == "Cup":
                    TypeOfDay ="Cup Day"
                    Division_table = None
                else:
                    TypeOfDay ="Division Day"
                    Division_table = TeamDivisionData.objects.all().filter(Tournament_id = next_game.Tournament.id).order_by("Place")
            elif next_game.TournamentName == "Cup":
                TypeOfDay ="Cup Day"
                Division_table = None
            else:
                TypeOfDay ="Division Day"
                Division_table = TeamDivisionData.objects.all().filter(Tournament_id = next_game.Tournament.id).order_by("Place")

        all_players_fitness = PlayerFitnessLog.objects.all().filter(Day= last_day, TypeOfUpdate = "Dayly").order_by("-FitnessChange")[:10]

        Current_week = current_day.Week
        Current_week_days = [Current_week*7-6,Current_week*7-5,Current_week*7-4,Current_week*7-3,Current_week*7-2,Current_week*7-1,Current_week*7]
        
        context = {
                'form':form,
                'all_matches':all_matches,
                'next_game':next_game,
                'last_game':last_game,
                'current_day':current_day,
                "Current_week_days":Current_week_days,
                "all_players_fitness":all_players_fitness,
                "last_day":last_day,
                "Tournaments":Tournaments,
                'Division_table':Division_table,
                "TypeOfDay":TypeOfDay
                }
        return render(request,self.template_name,context)

    def post(self,request):
        form = HomeForm(request.POST)
        current_day = DayTable.objects.get(Status='Current')
        next_day = DayTable.objects.get(Status='Next')
        next_game = GeneralSchedule.objects.filter(Played=False).first()

        if "ReSetGames" in request.POST:
            Reset_Database.ReSetAll()

        elif "PlayNextGame" in request.POST:
            #Check if next game is on a new day in that case show end of day form
            if next_game.Day > current_day.Day:
                Day_loop.Set_End_of_Day(current_day.Day)
            else:
                Matchgenerator.Full_game(connection_string)
                Tournaments = Tournament.objects.all()

                for T in Tournaments:
                    T.collapse()
                    # T.calendar_class = "btn btn-link collapsed"
                    # T.calendar_expanded = "false"
                    # T.calendar_div_class = "collapse"

                next_game.Tournament.expand()



        elif "PlayFullDay" in request.POST:
            #Check if next game is on a new day in that case show end of day form
            if next_game.Day > current_day.Day:
                Day_loop.Set_End_of_Day(connection_string,current_day.Day)
            else:
                no_of_matches = len(GeneralSchedule.objects.all().filter(Day = current_day.Day,Played =False))
                for x in range(0,no_of_matches):
                    Matchgenerator.Full_game(connection_string)

        elif "Endday" in request.POST:
            Motivation_update.Motivation_update(connection_string, current_day.Day)
            Fitness_recovery.Recovery(connection_string, current_day.Day)
            #check if it's the end of the week
            if next_day.Week > current_day.Week:
                Day_loop.Set_End_of_Week(connection_string, current_day.Day)
                Day_loop.Remove_End_of_Day(connection_string, current_day.Day)
            else:
                Day_loop.Remove_End_of_Day(connection_string, current_day.Day)
                Day_loop.Change_of_Day(connection_string, current_day.Day)

        elif "EndWeek" in request.POST:
            #update division table
            update_division_table.weekly_update(connection_string, current_day.Week)
            #update cup schedule
            update_cup_schedule.cup_update(connection_string)

            #update next week
            Day_loop.Remove_End_of_Week(connection_string, current_day.Day)
            #update day
            Day_loop.Remove_End_of_Day(connection_string, current_day.Day)
            Day_loop.Change_of_Day(connection_string, current_day.Day)
            Tournaments = Tournament.objects.all()

            for T in Tournaments:
                T.collapse()
                # T.calendar_class = "btn btn-link collapsed"
                # T.calendar_expanded = "false"
                # T.calendar_div_class = "collapse"

            next_game.Tournament.expand()

        # elif "UntilDay" in request.POST:
        #     #End day
        #     #if same day - stop

        #     #For day
        #     #play remaining games
        #     #end day procedure
        #     #if new week
        #     #end week procedure
        #     #Change day
        #     #stop when End day = current day


        return redirect("season:calendar")
       

class MatchView(generic.TemplateView):
    template_name = "season/match.html"

    def get(self,request,GameID,GameRound):
        form = MatchForm()
        schedule = GeneralSchedule.objects.get(GameID = GameID)
        Home_team_name = schedule.Home
        Away_team_name = schedule.Away
        Home_team = Team.objects.get(Name = Home_team_name)
        Away_team = Team.objects.get(Name = Away_team_name)
        Home_team_background = TeamInfo.objects.get(Name = Home_team_name)
        Away_team_background = TeamInfo.objects.get(Name = Away_team_name)
        NextRound = GameRound + 1
        CurrentPage ="Match"
        Played = schedule.Played
        if Played == True:
            all_rounds_so_far = GameTeamLog.objects.all().filter(GameID = GameID, GameRound__lte=GameRound) 
            if GameRound > 0:
                current_round = GameTeamLog.objects.all().filter(GameID = GameID, GameRound=GameRound).first
                context = {'Played':Played,
                'form':form,
                'all_rounds_so_far':all_rounds_so_far,
                'GameID':GameID, 'GameRound':GameRound, 
                'current_round':current_round,
                'Home_team':Home_team,'Away_team':Away_team,
                'Home_team_background':Home_team_background,'Away_team_background':Away_team_background,
                'NextRound':NextRound,
                'CurrentPage':CurrentPage}
            else:
                context = {'Played':Played,
                'form':form,
                'all_rounds_so_far':all_rounds_so_far,
                'GameID':GameID, 'GameRound':GameRound, 
                'Home_team':Home_team,'Away_team':Away_team,
                'Home_team_background':Home_team_background,'Away_team_background':Away_team_background,
                'NextRound':NextRound,
                'CurrentPage':CurrentPage}
        else:
            context = {'Played':Played,
            'form':form,
            'GameID':GameID, 'GameRound':GameRound, 
            'Home_team':Home_team,'Away_team':Away_team,
            'Home_team_background':Home_team_background,'Away_team_background':Away_team_background,
            'NextRound':NextRound,
            'CurrentPage':CurrentPage}
        return render(request, self.template_name, context)

    def post(self,request,GameID,GameRound):
        form = MatchForm(request.POST)
        if form.is_valid():
            GameRound = form.cleaned_data['GameRound']
        return redirect("season:match",GameID =GameID, GameRound = GameRound)

class MatchSquadsView(MatchView):
    template_name = "season/match_squads.html"
    def get(self,request,GameID,GameRound):
        form = MatchForm()
        schedule = GeneralSchedule.objects.get(GameID = GameID)
        Home_team_name = schedule.Home
        Away_team_name = schedule.Away
        Home_team = Team.objects.get(Name = Home_team_name)
        Away_team = Team.objects.get(Name = Away_team_name)
        Home_team_players_start = Player.objects.all().filter(Team = Home_team_name)
        Away_team_players_start = Player.objects.all().filter(Team = Away_team_name)
        NextRound = GameRound + 1
        CurrentPage ="Squad"
        Played = schedule.Played
        if Played == True:
            all_rounds_so_far = GameTeamLog.objects.all().filter(GameID = GameID, GameRound__lte=GameRound)
            current_round = GameTeamLog.objects.all().filter(GameID = GameID, GameRound=GameRound) 
            Home_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)
            Away_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)

            if GameRound > 0:
                #current_round = GameTeamLog.objects.all().filter(GameID = GameID, GameRound=GameRound).first

                #PLayers = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)| GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)
                #HomePlayers = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)
                #AwayPlayers = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)
                #ContainerDict = {1:["Empty",None], 2:["LM","Home"],3:["Empty",None],4:["GK","Home"],5:["Empty",None],6:["ST","Home"],7:["Empty",None],8:["RM","Home"],9:["Empty",None],10:["Empty",None], 11:["RM","AWay"],12:["Empty",None],13:["ST","AWay"],14:["Empty",None],15:["GK","AWay"],16:["Empty",None],17:["LM","AWay"],18:["Empty",None]}
                #TestDict = {1:["Empty","Home"], 2:["LM","Away"]}
                HomeContainerDict = {1:"Empty", 2:"LM",3:"Empty",4:"GK",5:"Empty",6:"ST",7:"Empty",8:"RM",9:"Empty"}
                AwayContainerDict = {1:"Empty", 2:"RM",3:"Empty",4:"ST",5:"Empty",6:"GK",7:"Empty",8:"LM",9:"Empty"}
                #ContainerDicts = [HomeContainerDict,AwayContainerDict]
                context = {'Played':Played,
                'form':form,
                'all_rounds_so_far':all_rounds_so_far,
                'current_round':current_round,
                'Home_team_players_start':Home_team_players_start,
                #'ContainerDict':ContainerDict,
                'HomeContainerDict':HomeContainerDict,
                'AwayContainerDict':AwayContainerDict,
                #'TestDict':TestDict,
                #'HomePlayers':HomePlayers,
                #'AwayPlayers':AwayPlayers,
                #'PLayers':PLayers,
                'Away_team_players_start':Away_team_players_start,
                'Home_team_players':Home_team_players,
                'Away_team_players':Away_team_players,
                'GameID':GameID, 'GameRound':GameRound, 
                'Home_team':Home_team,'Away_team':Away_team,
                'NextRound':NextRound,
                'CurrentPage':CurrentPage}
            else:
                context = {'Played':Played,
                'form':form,
                'all_rounds_so_far':all_rounds_so_far,
                'Home_team_players_start':Home_team_players_start,
                'Away_team_players_start':Away_team_players_start,
                'GameID':GameID, 'GameRound':GameRound, 
                'Home_team':Home_team,'Away_team':Away_team,
                'NextRound':NextRound,
                'CurrentPage':CurrentPage}
        else:
            context = {'Played':Played,
            'Home_team_players_start':Home_team_players_start,
            'Away_team_players_start':Away_team_players_start,
            'form':form,
            'GameID':GameID, 'GameRound':GameRound, 
            'Home_team':Home_team,'Away_team':Away_team,
            'NextRound':NextRound,
            'CurrentPage':CurrentPage}
        return render(request, self.template_name, context)

    def post(self,request,GameID,GameRound):
        form = MatchForm(request.POST)
        if form.is_valid():
            GameRound = form.cleaned_data['GameRound']
        return redirect("season:Squad",GameID =GameID, GameRound = GameRound)

    #     form = MatchForm()
    #     schedule = GeneralSchedule.objects.get(GameID = GameID)
    #     all_rounds_home = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Home")
    #     all_rounds_away = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Away")
    #     current_round_home = all_rounds_home[GameRound]
    #     current_round_away = all_rounds_away[GameRound]
    #     Home_team_name = schedule.Home
    #     Away_team_name = schedule.Away
    #     Home_team = Team.objects.get(Name = Home_team_name)
    #     Away_team = Team.objects.get(Name = Away_team_name)
    #     Home_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)
    #     Away_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)
    #     Home_team_players_start = Player.objects.all().filter(Team = Home_team_name)
    #     Away_team_players_start = Player.objects.all().filter(Team = Away_team_name)
    #     NextRound = GameRound + 1
    #     context = {'form':form,
    #     'all_rounds_home':all_rounds_home,'all_rounds_away':all_rounds_away,
    #     'GameID':GameID, 'GameRound':GameRound, 
    #     'current_round_home':current_round_home,'current_round_away':current_round_away,
    #     'Home_team':Home_team,'Away_team':Away_team, 
    #     'Home_team_players':Home_team_players,'Away_team_players':Away_team_players,
    #     'Home_team_players_start':Home_team_players_start, 'Away_team_players_start':Away_team_players_start,
    #     'NextRound':NextRound,
    #     'CurrentPage':"Squad"}
    #     return render(request, self.template_name, context)

    # def post(self,request,GameID,GameRound):
    #     form = MatchForm(request.POST)
    #     if form.is_valid():
    #         GameRound = form.cleaned_data['GameRound']
    #     return MatchView.get(self,request,GameID,GameRound)

class MatchStatsView(MatchView):
    template_name = "season/match_stats.html"
    def get(self,request,GameID,GameRound):
        form = MatchForm()
        schedule = GeneralSchedule.objects.get(GameID = GameID)
        Played = schedule.Played
        all_rounds_home = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Home")
        all_rounds_away = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Away")
        current_round_home = all_rounds_home[GameRound]
        current_round_away = all_rounds_away[GameRound]
        Home_team_name = schedule.Home
        Away_team_name = schedule.Away
        All_players = Player.objects.filter(Q(Team = Home_team_name)|Q(Team = Away_team_name))
        Home_team = Team.objects.get(Name = Home_team_name)
        Away_team = Team.objects.get(Name = Away_team_name)
        Home_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)
        Away_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)
        Home_team_players_start = Player.objects.all().filter(Team = Home_team_name)
        Away_team_players_start = Player.objects.all().filter(Team = Away_team_name)
        Home_team_players_aggregated = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Home_team_name).annotate(Avg("Name"))
        Away_team_players_aggregated = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Away_team_name).annotate(Avg("Name"))
        current_round = GameTeamLog.objects.all().filter(GameID = GameID, GameRound=GameRound).first

        if GameRound == 0:
            df = ""
            df2 = ""
            df3 = ""
            keys = ""
        else:
            keys = [player.Name for player in Home_team_players_start ]

            df = pd.DataFrame(list(GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Home_team_name).values('Name', 'OffensiveAbilityChange','DefensiveAbilityChange')))
            df2 = df.pivot_table(index = 'Name', values = ['OffensiveAbilityChange','DefensiveAbilityChange'], aggfunc = 'sum')
            df3 = df2.T.to_dict('list')
        #https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary
        #df3 = np.array(df2[['PlayerName','OffensiveAbilityChange']])

        NextRound = GameRound + 1
        context = {'Played':Played,
        'current_round':current_round,
        'form':form,
        'keys':keys,'df':df,'df2':df2,'df3':df3,
        #'df3':df3,
        'all_rounds_home':all_rounds_home,'all_rounds_away':all_rounds_away,
        'GameID':GameID, 'GameRound':GameRound, 
        'current_round_home':current_round_home,'current_round_away':current_round_away,
        'Home_team':Home_team,'Away_team':Away_team, 
        'Home_team_players':Home_team_players,'Away_team_players':Away_team_players,
        'Home_team_players_start':Home_team_players_start, 'Away_team_players_start':Away_team_players_start,
        'Home_team_players_aggregated':Home_team_players_aggregated,'Away_team_players_aggregated':Away_team_players_aggregated,
        'NextRound':NextRound,
        'All_players':All_players,
        'CurrentPage':"Stats"}
        return render(request, self.template_name, context)

class MatchTableView(MatchView):
    template_name = "season/match_table.html"
    def get(self,request,GameID,GameRound):
        form = MatchForm()
        schdule_data = GeneralSchedule.objects.get(GameID = GameID)
        Played = schdule_data.Played
        all_rounds_home = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Home")
        all_rounds_away = GameTeamLog.objects.all().filter(GameID = GameID, HomeOrAway = "Away")
        current_round_home = all_rounds_home[GameRound]
        current_round_away = all_rounds_away[GameRound]
        Home_team_name = schdule_data.Home
        Away_team_name = schdule_data.Away
        Home_team = Team.objects.get(Name = Home_team_name)
        Away_team = Team.objects.get(Name = Away_team_name)
        Home_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Home_team_name)
        Away_team_players = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound = GameRound, Team = Away_team_name)
        Home_team_players_start = Player.objects.all().filter(Team = Home_team_name)
        Away_team_players_start = Player.objects.all().filter(Team = Away_team_name)
        Home_team_players_aggregated = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Home_team_name).annotate(Avg("Name"))
        Away_team_players_aggregated = GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Away_team_name).annotate(Avg("Name"))
        
        if GameRound == 0:
            df = ""
            df2 = ""
            df3 = ""
            keys = ""
        else:
            keys = [player.Name for player in Home_team_players_start ]

            df = pd.DataFrame(list(GamePlayerLog.objects.all().filter(GameID = GameID, GameRound__lte = GameRound, Team = Home_team_name).values('Name', 'OffensiveAbilityChange','DefensiveAbilityChange')))
            df2 = df.pivot_table(index = 'Name', values = ['OffensiveAbilityChange','DefensiveAbilityChange'], aggfunc = 'sum')
            df3 = df2.T.to_dict('list')
        #https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary
        #df3 = np.array(df2[['PlayerName','OffensiveAbilityChange']])

        NextRound = GameRound + 1
        context = {'form':form,
        'keys':keys,'df':df,'df2':df2,'df3':df3,
        #'df3':df3,
        'all_rounds_home':all_rounds_home,'all_rounds_away':all_rounds_away,
        'GameID':GameID, 'GameRound':GameRound, 
        'current_round_home':current_round_home,'current_round_away':current_round_away,
        'Home_team':Home_team,'Away_team':Away_team, 
        'Home_team_players':Home_team_players,'Away_team_players':Away_team_players,
        'Home_team_players_start':Home_team_players_start, 'Away_team_players_start':Away_team_players_start,
        'Home_team_players_aggregated':Home_team_players_aggregated,'Away_team_players_aggregated':Away_team_players_aggregated,
        'NextRound':NextRound,
        'CurrentPage':"Table"}
        return render(request, self.template_name, context)

    def post(self,request,GameID,GameRound):
        form = MatchForm(request.POST)
        if form.is_valid():
            GameRound = form.cleaned_data['GameRound']
        return MatchView.get(self,request,GameID,GameRound)

class LeagueView(generic.list.ListView):
    template_name = "season/league.html"

    def get(self,request):
        Div1 = TeamDivisionData.objects.all().filter(Division="Div 1").order_by("Place")
        Div2 = TeamDivisionData.objects.all().filter(Division="Div 2").order_by("Place")
        Div3 = TeamDivisionData.objects.all().filter(Division="Div 3").order_by("Place")
        Div4 = TeamDivisionData.objects.all().filter(Division="Div 4").order_by("Place")
        Div5 = TeamDivisionData.objects.all().filter(Division="Div 5").order_by("Place")
        Div6 = TeamDivisionData.objects.all().filter(Division="Div 6").order_by("Place")
        context = {"Div1":Div1,"Div2":Div2, "Div3":Div3,
                    "Div4":Div4, "Div5":Div5,"Div6":Div6}
        return render(request,self.template_name,context)

class CupView(generic.list.ListView):
    template_name = "season/cup.html"

    def get(self,request):
        Qualification = GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Qualification")
        RoundOf32 = GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Round of 32")
        RoundOf16 = GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Round of 16")
        QuarterFinals = GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Quarter Final")
        SemiFinals= GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Semi Final")
        Final = GeneralSchedule.objects.all().filter(Tournament="Cup",TournamnetRound = "Final")
        context = {"Qualification":Qualification,"RoundOf32":RoundOf32, "RoundOf16":RoundOf16,"QuarterFinals":QuarterFinals,
                    "SemiFinals":SemiFinals, "Final":Final}
        return render(request,self.template_name,context)

class PlayersList(generic.list.ListView):
    template_name = "season/players.html"
    context_object_name = "all_players"

    def get_queryset(self):
        return Player.objects.all()

class PlayerDeatail(generic.list.ListView):
    template_name = "season/player.html"
    context_object_name = "player"

    def get(self,request,Name):
        player = Player.objects.all().filter(Name = Name)
        context ={'player':player}
        return render(request, self.template_name, context)

class TeamsList(generic.list.ListView):
    template_name = "season/teamlist.html"
    context_object_name = "all_teams"

    def get_queryset(self):
        return Team.objects.all()

class TeamDetail(generic.detail.DetailView):
    template_name = "season/teamdetail.html"
    context_object_name = "team"

    def get(self,request,pk):
        team = Team.objects.get(id = pk)
        teaminfo = team.teaminfo_set.get()
        context ={'team':team,
                    'teaminfo':teaminfo}
        return render(request, self.template_name, context)


class TestPageView(generic.TemplateView):
    template_name = "season/test_page.html"

    def get(self,request):
        last_day = 1
        all_players_fitness = PlayerFitnessLog.objects.all().filter(Day= last_day, TypeOfUpdate = "Dayly").order_by("-FitnessChange")[:10]
        Players = GamePlayerLog.objects.filter(Player__Nation = "Sverige")
        context ={'Players':Players,"all_players_fitness":all_players_fitness}
        return render(request, self.template_name, context)


class TeamUpdate(generic.edit.UpdateView):
    model = Team
    fields = ['Name', 'FullName']