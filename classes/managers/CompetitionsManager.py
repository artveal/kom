from django.db import models
from django.db.models import Q
from classes.models import Competition, CompetitionRound, CompetitionSeason, CompetitionSeasonRound, QualifyingRelation, TeamPerformance

from classes.managers.MatchesManager import MatchesManager

class CompetitionsManager(models.Manager):
    def CompetitionbyId(self, competitionId):
        querySet = models.query.QuerySet(model=Competition, using=self._db)
        conditions = (
            Q(id__exact=competitionId)
        )
        result = querySet.filter(conditions).distinct()
        return result[0]

    def RoundsOfCompetition(self, competitionId):
        querySet = models.query.QuerySet(model=CompetitionRound, using=self._db)
        conditions = (
            Q(competition__id__exact=competitionId)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getCompetitionSeasons(self, competitionId):
        querySet = models.query.QuerySet(model=CompetitionSeason, using=self._db)
        conditions = (
            Q(competition__id__exact=competitionId)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def RoundsOfCompetitionSeason(self, competitionSeasonId):
        querySet = models.query.QuerySet(model=CompetitionSeasonRound, using=self._db)
        conditions = (
            Q(competition_season__id__exact=competitionSeasonId)
        )
        result = querySet.filter(conditions).distinct()
        return result

    def getTeamPerformances(self, competitionSeasonRoundId):
        querySet = models.query.QuerySet(model=TeamPerformance, using=self._db)
        conditions = (
            Q(competition__id__exact=competitionSeasonRoundId)
        )
        result = querySet.filter(conditions).order_by('-points').distinct()
        return result

    def getLeagueTable(self, competitionSeasonRoundId):
        teams = self.getTeamPerformances(competitionSeasonRoundId)
        competitionSeason = self.RoundsOfCompetitionSeason(competitionSeasonRoundId)

        point_groups = dict()
        for team in teams:
            if point_groups.get(str(team.points), False):
                point_groups[str(team.points)].append(team)
            else:
                point_groups.update({str(team.points): [team, ]})

        if competitionSeason.untie_rule == "local":
            pass
            # SORT TEAMS INSIDE EACH POINT GROUP

        # return league_table
        league_table = []
        for group in point_groups.values():
            for team in group:
                league_table.append(team)

        return league_table


