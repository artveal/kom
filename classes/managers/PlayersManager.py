from django.db import models
from django.db.models import Q
from classes.models import Player

class PlayersManager(models.Manager):
    def PlayerbyId(self, playerId):
        querySet = models.query.QuerySet(model=Player, using=self._db)
        conditions = (
            Q(id__exact=playerId)
        )
        result = querySet.filter(conditions).distinct()
        return result[0]

    def PlayersbyName(self, playerName):
        querySet = models.query.QuerySet(model=Player, using=self._db)
        conditions = (
            Q(full_name__icontains=playerName)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getPlayersofNationalTeam(self, teamAbbr):
        querySet = models.query.QuerySet(model=Player, using=self._db)
        conditions = (
            Q(nationality__abbr__exact=teamAbbr) &
            Q(n_shirt_number__gt=0)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getAllPlayersbyTeamId(self, teamId):
        querySet = models.query.QuerySet(model=Player, using=self._db)
        conditions = (
            Q(team__id__exact=teamId)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getPlayersbyTeamId(self, teamId):
        conditions = (
            Q(youth_team__exact=False)
        )
        return self.getAllPlayersbyTeamId(teamId).filter(conditions)

    def getYouthPlayersbyTeamId(self, teamId):
        conditions = (
            Q(youth_team__exact=True)
        )
        return self.getAllPlayersbyTeamId(teamId).filter(conditions)