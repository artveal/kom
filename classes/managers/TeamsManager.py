from django.db import models
from django.db.models import Q
from classes.models import Team

class TeamsManager(models.Manager):
    def TeambyId(self, teamId):
        querySet = models.query.QuerySet(model=Team, using=self._db)
        conditions = (
            Q(id__exact=teamId)
        )
        result = querySet.filter(conditions).distinct()
        return result[0]

    def TeamsbyName(self, teamName):
        querySet = models.query.QuerySet(model=Team, using=self._db)
        conditions = (
            Q(name__icontains=teamName) &
            Q(national_team=None)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def NationsbyName(self, nationName):
        querySet = models.query.QuerySet(model=Team, using=self._db)
        conditions = (
            Q(name__icontains=nationName) &
            Q(national_team=True)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getNationalTeam(self, teamAbbr):
        querySet = models.query.QuerySet(model=Team, using=self._db)
        conditions = (
            Q(abbr__exact=teamAbbr)
        )
        result = querySet.filter(conditions).exclude(national_team=False).distinct()
        if result:
            return result[0]
        else:
            return None