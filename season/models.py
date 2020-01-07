from django.db import models
from django.urls import reverse

class Tournament(models.Model):
	"""docstring for Tournament"""
	Name = models.CharField(max_length=100)
	Value = models.CharField(max_length=10)
	calendar_class = models.CharField(max_length=100)
	calendar_datatarget = models.CharField(max_length=100)
	calendar_expanded = models.CharField(max_length=100)
	calendar_id = models.CharField(max_length=100)
	calendar_div_class = models.CharField(max_length=100)

	def __str__(self):
		return self.Name

	def collapse(self):
		self.calendar_class = "btn btn-link collapsed"
		self.calendar_expanded = "false"
		self.calendar_div_class = "collapse"
		super().save()

	def expand(self):
		self.calendar_class = "btn btn-link"
		self.calendar_expanded = "true"
		self.calendar_div_class = "collapse show"
		super().save()
		
class Nation(models.Model):
	Name = models.CharField(max_length=100)
	Flag = models.ImageField(blank=True, null=True)

#general tables
class Player(models.Model):
	Ability = models.FloatField()
	DefensiveAbility = models.FloatField()
	DivisionRank = models.IntegerField(blank=True,null=True)
	Fitness = models.FloatField()
	GKPosExperience = models.FloatField()
	LMPosExperience = models.FloatField()
	Nation = models.ForeignKey(Nation, on_delete=models.CASCADE,blank=True,null=True)
	OffensiveAbility = models.FloatField()
	PlayerChemistry = models.FloatField()
	PlayerMotivation = models.FloatField()
	Name = models.CharField(max_length=100)
	Position = models.CharField(max_length=100)
	RMPosExperience = models.FloatField()
	Routine = models.IntegerField()
	RoutineRank = models.FloatField()
	STPosExperience = models.FloatField()
	Team = models.CharField(max_length=100)
	TeamPlayerID = models.CharField(max_length=100,blank=True, null=True)
	Image = models.ImageField(blank=True, null=True)
	Age = models.IntegerField(blank=True,null=True)
	Personlighet = models.CharField(max_length=100, blank=True, null=True)
	Extrovert_Introvert = models.CharField(max_length=100, blank=True, null=True)
	E_I = models.CharField(max_length=100, blank=True, null=True)
	Sinnesfornimmelse_Intuition = models.CharField(max_length=100, blank=True, null=True)
	S_N = models.CharField(max_length=100, blank=True, null=True)
	Tanke_Kansla = models.CharField(max_length=100, blank=True, null=True)
	T_K = models.CharField(max_length=100, blank=True, null=True)
	Bedomning_Perception = models.CharField(max_length=100, blank=True, null=True)
	B_P = models.CharField(max_length=100, blank=True, null=True)
	Personlighetsgrupp = models.CharField(max_length=100, blank=True, null=True)
	Personlighetsbeskrivning = models.CharField(max_length=100, blank=True, null=True)
	langre_personlighetsbeskrivning = models.CharField(max_length=100, blank=True, null=True)


	def __str__(self):
		return self.Name

class Team(models.Model):
	AbilityRank = models.IntegerField()
	AbilityRankDivision = models.IntegerField()
	AverageAbility = models.FloatField()
	Division = models.CharField(max_length=100)
	DivisionID = models.CharField(max_length=100)
	Name = models.CharField(max_length=100)
	NoOfPlayers = models.IntegerField(blank=True, null=True)
	SeedingGroup = models.CharField(max_length=100)
	SeedingNumber = models.IntegerField(blank=True, null=True)
	Tactics = models.CharField(max_length=100)
	TacticsValue = models.FloatField()
	TotalAbility = models.FloatField()
	Logo = models.ImageField(blank=True, null=True)
	FullName = models.CharField(max_length=100, blank=True, null=True)

	def get_absolute_url(self):
		return reverse('season:team_detail',kwargs={'pk':self.pk})


	def __str__(self):
		return self.Name

	



class GeneralSchedule(models.Model):
	Day = models.IntegerField(blank=True, null=True)
	Week = models.IntegerField(blank=True, null=True)
	GameID = models.IntegerField(blank=True, null=True)
	GameNumber = models.IntegerField(blank=True, null=True)
	TypeOfGame = models.CharField(max_length=100,blank=True, null=True)
	TournamentName = models.CharField(max_length=100,blank=True, null=True)
	Home = models.CharField(max_length=100)
	HomeTeam = models.ForeignKey(Team,on_delete=models.CASCADE,related_name = "HomeTeam",blank=True,null=True)
	Away = models.CharField(max_length=100)
	AwayTeam = models.ForeignKey(Team,on_delete=models.CASCADE,related_name = "AwayTeam",blank=True,null=True)
	GoalsHome = models.IntegerField(blank=True, null=True)
	GoalsAway = models.IntegerField(blank=True, null=True)
	Played = models.BooleanField(default=False)
	AfterPenaltyHome = models.IntegerField(blank=True, null=True)
	AfterPenaltyAway = models.IntegerField(blank=True, null=True)
	DivisionHome = models.CharField(max_length=100, blank=True, null=True)
	DivisionAway = models.CharField(max_length=100, blank=True, null=True)
	DivisionPlaceHome = models.IntegerField(blank=True, null=True)
	DivisionPlaceAway = models.IntegerField(blank=True, null=True)
	DivisionPlaceDifference = models.IntegerField(blank=True, null=True)
	FavouriteStatusAway = models.CharField(max_length=100)
	FavouriteStatusHome = models.CharField(max_length=100)
	FocusedEvent = models.CharField(max_length=100, blank=True, null=True)
	PrestigeCupAway = models.FloatField(blank=True, null=True)
	PrestigeCupHome = models.FloatField(blank=True, null=True)
	PrestigePointsBasic = models.FloatField(blank=True, null=True)
	PrestigePointsDivisionBasic = models.FloatField(blank=True, null=True)
	PrestigePointsFocusedEvent = models.FloatField(blank=True, null=True)
	PrestigePointsRivalryAway = models.FloatField(blank=True, null=True)
	PrestigePointsRivalryHome = models.FloatField(blank=True, null=True)
	PrestigePointsTotalAway = models.FloatField(blank=True, null=True)
	PrestigePointsTotalHome = models.FloatField(blank=True, null=True)
	TournamnetRound = models.CharField(max_length=100)
	RoutinePoints = models.IntegerField(blank=True, null=True)
	SignAway = models.CharField(max_length=100)
	SignHome = models.CharField(max_length=100)
	TeamMotivationAway = models.FloatField(blank=True, null=True)
	TeamMotivationFavouriteStatusAway = models.FloatField(blank=True, null=True)
	TeamMotivationFavouriteStatusHome = models.FloatField(blank=True, null=True)
	TeamMotivationHome = models.FloatField(blank=True, null=True)
	TeamMotivationPreviousRoundAway = models.FloatField(blank=True, null=True)
	TeamMotivationPreviousRoundHome = models.FloatField(blank=True, null=True)
	TeamMotivationSituationAway = models.FloatField(blank=True, null=True)
	TeamMotivationSituationHome = models.FloatField(blank=True, null=True)
	TeamRankAway = models.IntegerField(blank=True, null=True)
	TeamRankDifference = models.IntegerField(blank=True, null=True)
	TeamRankDivisionAway = models.IntegerField(blank=True, null=True)
	TeamRankDivisionDifference = models.IntegerField(blank=True, null=True)
	TeamRankDivisionHome = models.IntegerField(blank=True, null=True)
	TeamRankHome = models.IntegerField(blank=True, null=True)
	TeamRivalryAway = models.FloatField(blank=True, null=True)
	TeamRivalryHome = models.FloatField(blank=True, null=True)
	TeamRivalryTotal = models.FloatField(blank=True, null=True)
	TeamTacticsAway = models.CharField(max_length=100,blank=True, null=True)
	TeamTacticsGameValueAway = models.FloatField(blank=True, null=True)
	TeamTacticsGameValueHome = models.FloatField(blank=True, null=True)
	TeamTacticsHome = models.CharField(max_length=100,blank=True, null=True)
	TeamTacticsValueAway = models.FloatField(blank=True, null=True)
	TeamTacticsValueHome = models.FloatField(blank=True, null=True)
	Winner = models.CharField(max_length=100,blank=True, null=True)
	QualificationHome = models.CharField(max_length=100,blank=True, null=True)
	QualificationAway = models.CharField(max_length=100,blank=True, null=True)
	SchedulingIdentifyerHome = models.CharField(max_length=100,blank=True, null=True)
	SchedulingIdentifyerAway = models.CharField(max_length=100,blank=True, null=True)
	Tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,blank=True,null=True)

	def __str__(self):
		return "MatchID " + str(self.id)

class TeamDivisionData(models.Model):
	Division = models.CharField(max_length=100)
	Tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,blank=True,null=True)
	DivisionID = models.CharField(max_length=100)
	Drawn = models.IntegerField()
	GoalDifference = models.IntegerField()
	GoalsConceded = models.IntegerField()
	GoalsScored = models.IntegerField()
	Lost = models.IntegerField()
	Name = models.CharField(max_length=100)
	Team = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True,null=True)
	Place = models.IntegerField()
	PlayedGames = models.IntegerField()
	Points = models.IntegerField()
	Won = models.IntegerField()

#game logs
class GamePlayerLog(models.Model):
	#Gneral info about game and round
	GameRound = models.IntegerField(blank=True,null=True)
	GameID = models.IntegerField(blank=True,null=True)
	AreaAttack = models.CharField(max_length=100,blank=True,null=True)
	AreaDefence = models.CharField(max_length=100,blank=True,null=True)
	#General info about player
	Player = models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True)
	Name = models.CharField(max_length=100,blank=True,null=True)
	Position = models.CharField(max_length=100,blank=True,null=True)
	#Team realated info
	Team = models.CharField(max_length=100,blank=True,null=True)
	TeamTactics = models.CharField(max_length=100,blank=True,null=True)
	Chemestry = models.FloatField(blank=True,null=True)
	#Ability
	Ability = models.FloatField(blank=True,null=True)
	OffensiveAbility = models.FloatField(blank=True,null=True)
	DefensiveAbility = models.FloatField(blank=True,null=True)
	AttackAbility = models.FloatField(blank=True,null=True)
	DefendAbility = models.FloatField(blank=True,null=True)
	OffensiveAbilityChange = models.FloatField(blank=True,null=True)
	GoalOffAbilityChange = models.FloatField(blank=True,null=True)
	DefensiveAbilityChange = models.FloatField(blank=True,null=True)
	SaveDefAbilityChange = models.FloatField(blank=True,null=True)
	SentOffOffAbilityChange = models.FloatField(blank=True,null=True)
	SentOffDefAbilityChange = models.FloatField(blank=True,null=True)
	PositionalExperience = models.FloatField(blank=True,null=True) #Experience with the current position
	AttackAbilityChangePerformance = models.FloatField(blank=True, null=True)
	DefeneceAbilityChangePerformance = models.FloatField(blank=True, null=True)
	AttackAbilityChangeEffect = models.FloatField(blank=True, null=True)
	DefenceAbilityChangeEffect = models.FloatField(blank=True, null=True)

	#Performance
	DefensivePerformance = models.FloatField(blank=True,null=True)
	OffensivePerformance = models.FloatField(blank=True,null=True)
	OffensiveValue = models.IntegerField(blank=True,null=True)
	DefensiveValue = models.IntegerField(blank=True,null=True)
	MotivationAdjustedDefensivePerformance = models.FloatField(blank=True,null=True)
	MotivationAdjustedOffensivePerformance = models.FloatField(blank=True,null=True)
	DefensiveRating = models.FloatField(blank=True,null=True) #round rating, chnages every round
	OffensiveRating = models.FloatField(blank=True,null=True) #round rating, chnages every round
	MatchRating = models.FloatField(blank=True,null=True) #accumulated rating for the whole game influenced by both offenisve and defensive rating
	#Other factors
	AttackingPostionalOffensiveFactor = models.FloatField(blank=True,null=True)
	AttackingPostionalDefensiveFactor = models.FloatField(blank=True,null=True)
	DefendingPostionalOffensiveFactor = models.FloatField(blank=True,null=True)
	DefendingPostionalDefensiveFactor = models.FloatField(blank=True,null=True)
	MaxAttackPerformance = models.IntegerField(blank=True,null=True)
	MaxDefencePerformance = models.IntegerField(blank=True,null=True)
	AttackAreaInfluence = models.FloatField(blank=True,null=True)
	DefenceAreaInfluence = models.FloatField(blank=True,null=True)

	#Eventws
	GoalPlayer = models.IntegerField(blank=True,null=True)
	SavePlayer = models.IntegerField(blank=True,null=True)
	SentOff = models.BooleanField()
	Substitute = models.BooleanField()

	#Fitness and motivation
	NewFitness = models.FloatField(blank=True,null=True)
	FitnessChange = models.FloatField(blank=True,null=True)
	NewMotivation = models.FloatField(blank=True,null=True)
	PersonalMotivation = models.FloatField(blank=True,null=True)
	TeamMotivation = models.FloatField(blank=True,null=True)
	MotivationChange = models.FloatField(blank=True,null=True)
	PersonalMotivationChange = models.FloatField(blank=True,null=True)
	TeamMotivationChange = models.FloatField(blank=True,null=True)
	AdjustedPersonalMotivation = models.FloatField(blank=True,null=True)
	TotalMotivationChange = models.FloatField(blank=True,null=True)
	AttackIntensity = models.FloatField(blank=True,null=True)
	DefenceIntensity = models.FloatField(blank=True,null=True)
	RoutineBonus = models.FloatField(blank=True,null=True)
	Nervosity = models.FloatField(blank=True,null=True)

class GameTeamLog(models.Model):
	GameID = models.IntegerField(blank=True,null=True)
	GameRound = models.IntegerField(blank=True,null=True)
	TeamName = models.CharField(max_length=100,blank=True,null=True)
	HomeOrAway = models.CharField(max_length=100,blank=True,null=True)
	AttckingArea = models.CharField(max_length=100,blank=True,null=True)
	DefendingArea = models.CharField(max_length=100,blank=True,null=True)
	AttackResult = models.CharField(max_length=100,blank=True,null=True)
	DefenceResult = models.CharField(max_length=100,blank=True,null=True)
	EventPlayerAttack = models.ForeignKey(Player,on_delete=models.CASCADE,related_name = "EventPlayerAttack",blank=True,null=True)
	EventPlayerDefence = models.ForeignKey(Player,on_delete=models.CASCADE,related_name = "EventPlayerDefence",blank=True,null=True)
	GoalsForwardAfterRound = models.IntegerField(blank=True,null=True)
	GoalsAgainstAfterRound = models.IntegerField(blank=True,null=True)
	TacticsValueChange = models.FloatField(blank=True,null=True)
	TacticsValue = models.FloatField(blank=True,null=True)
	Tactics = models.CharField(max_length=100,blank=True,null=True)
	Motivation = models.FloatField(blank=True,null=True)
	MotivationChange = models.FloatField(blank=True,null=True)
	Intensity = models.FloatField(blank=True,null=True)
	AttackValue = models.FloatField(blank=True,null=True)
	DefenseValue = models.FloatField(blank=True,null=True)
	Status = models.CharField(max_length=100,blank=True,null=True)
	StatusChange = models.CharField(max_length=100,blank=True,null=True)

class GamePenaltiesLog(models.Model):
	DefensiveAbility = models.FloatField()
	Event = models.CharField(max_length=100)
	GameID = models.IntegerField()
	GoalAway = models.IntegerField()
	GoalHome = models.IntegerField()
	Goalkeeper = models.CharField(max_length=100)
	OffensiveAbility = models.FloatField()
	PenaltyPlayer = models.CharField(max_length=100)
	PeneltyNumber = models.CharField(max_length=100)
	TeamName = models.CharField(max_length=100)
	TransactionID = models.IntegerField()

#spedfic logs
class PlayerMotivationLog(models.Model):
	OldMotivation = models.FloatField(default=0,blank=True, null=True)
	MotivationChange = models.FloatField(default=0,blank=True, null=True)
	NewMotivation = models.FloatField(blank=True, null=True)
	Player = models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, dayly, special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)

class PlayerFitnessLog(models.Model):
	OldFitness = models.FloatField(default=0,blank=True, null=True)
	FitnessChange = models.FloatField(default=0,blank=True, null=True)
	NewFitness = models.FloatField(blank=True, null=True)
	Player = models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, dayly, special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)

class PlayerAbilityLog(models.Model):
	OffensiveAbilityChange = models.FloatField(default=0,blank=True, null=True)
	OffensiveAbility = models.FloatField(blank=True, null=True)
	DefensiveAbilityChange = models.FloatField(default=0,blank=True, null=True)
	DefensiveAbility = models.FloatField(blank=True, null=True)
	Name = models.CharField(max_length=100,blank=True, null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, Dayly, Special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)

class TeamMotivationLog(models.Model):
	"""docstring for TeamMotivationLog"""
	MotivationChange = models.FloatField(blank=True, null=True)
	Motivation = models.FloatField(blank=True, null=True)
	Name = models.CharField(max_length=100,blank=True, null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, dayly, special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)


#imported tables not specific to ISL-Season
class PlayerInfo(models.Model):
	Name = models.CharField(max_length=100)
	PersonalityTrait = models.CharField(max_length=500)

class PlayerTransfer(models.Model):
	PlayerIn = models.CharField(max_length=100)
	PreviousTeam = models.CharField(max_length=100)
	TransactionID = models.IntegerField()

class TeamInfo(models.Model):
	Arena = models.CharField(max_length=100,blank=True,null=True)
	Background = models.CharField(max_length=1000,blank=True,null=True)
	FanClub = models.CharField(max_length=100,blank=True,null=True)
	FanClubDescription = models.CharField(max_length=1000,blank=True,null=True)
	FullName = models.CharField(max_length=100,blank=True,null=True)
	Name = models.CharField(max_length=99,blank=True,null=True)
	ArenaDescription = models.CharField(max_length=1000,blank=True,null=True)
	Team = models.ForeignKey(Team, on_delete = models.CASCADE, blank=True, null=True, default=None)

class TeamPrevDiv(models.Model):
	Division = models.CharField(max_length=100)
	DivisionPlace = models.IntegerField()
	Name = models.CharField(max_length=100)
	Season = models.CharField(max_length=100)

#Background tables
class DayTable(models.Model):
	Day = models.IntegerField(blank=True,null=True)
	Week= models.IntegerField(blank=True,null=True)
	Status = models.CharField(max_length=100)
	EndofDay = models.BooleanField(default=False)
	EndofWeek = models.BooleanField(default=False)

#temoporary tables
class TempFitnessLog(models.Model):
	"""docstring for TempFitnessLog"""
	OldFitness = models.FloatField(default=0,blank=True, null=True)
	FitnessChange = models.FloatField(default=0,blank=True, null=True)
	Player = models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True)
	NewFitness = models.FloatField(blank=True, null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, dayly, special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)

class TempMotivationLog(models.Model):
	OldMotivation = models.FloatField(default=0,blank=True, null=True)
	MotivationChange = models.FloatField(default=0,blank=True, null=True)
	NewMotivation = models.FloatField(blank=True, null=True)
	Player = models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True)
	# Name = models.CharField(max_length=100,blank=True, null=True)
	# Team = models.CharField(max_length=100,blank=True, null=True)
	Day = models.IntegerField(blank=True, null=True)
	#Type of update (Game, dayly, special event)
	TypeOfUpdate = models.CharField(max_length=100,blank=True, null=True)
	#GameID (only applicable for Game-updates)
	GameID = models.IntegerField(blank=True, null=True)
