from django.db import models
from django.db.models import Q
from classes.models import Competition, CompetitionRound, CompetitionSeason, CompetitionSeasonRound, QualifyingRelation, TeamPerformance

class MatchesManager(models.Manager):
    def getmatchbyId(self, matchId):
        pass