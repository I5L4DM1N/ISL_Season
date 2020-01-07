
from django.contrib import admin
from .models import GamePlayerLog, GameTeamLog, Player, GeneralSchedule, Team, PlayerFitnessLog, PlayerInfo, PlayerMotivationLog, PlayerTransfer, TeamDivisionData, TeamInfo, TeamPrevDiv, GamePenaltiesLog, Tournament


admin.site.register(GamePlayerLog)
admin.site.register(GameTeamLog)
admin.site.register(Player)
admin.site.register(GeneralSchedule)
admin.site.register(Team)
admin.site.register(PlayerFitnessLog)
admin.site.register(PlayerInfo)
admin.site.register(PlayerMotivationLog)
admin.site.register(PlayerTransfer)
admin.site.register(TeamDivisionData)
admin.site.register(TeamInfo)
admin.site.register(TeamPrevDiv)
admin.site.register(GamePenaltiesLog)
admin.site.register(Tournament)

