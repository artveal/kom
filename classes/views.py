from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponse
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, ListView
from django.contrib import messages

from .models import Competition

from .forms import LoginForm, RegisterForm, RoundInlineFormSet
from classes.managers.TeamsManager import TeamsManager
from classes.managers.PlayersManager import PlayersManager
from classes.managers.OthersManager import NationsManager, NewsManager
from classes.managers.CompetitionsManager import CompetitionsManager

# AJAX
from django.core import serializers
import json

def index(request):
    return render(request, 'index.html')

def cssexample(request):
    return render(request, 'cssexample.html')

def news(request, newsId):
    news, previous_news, next_news = NewsManager().getNewsbyId(newsId)
    return render(
        request=request,
        template_name = "news.html",
        context = {
            "news": news,
            "previous_news": previous_news,
            "next_news": next_news,
        }
    )

def competitionview(request, competitionId):
    competition_info = CompetitionsManager().CompetitionbyId(competitionId=competitionId)
    competition_rounds = CompetitionsManager().RoundsOfCompetition(competitionId=competitionId)
    competition_seasons = CompetitionsManager().getCompetitionSeasons(competitionId=competitionId)
    for season in competition_seasons:
        season.rounds = CompetitionsManager().RoundsOfCompetitionSeason(competitionSeasonId=season.id)

        for season_round in season.rounds:
            season_round.teams = CompetitionsManager().getTeamPerformances(competitionSeasonRoundId=season_round.id)
    return render(
        request=request,
        template_name = "competitionview.html",
        context = {
            "competition": competition_info,
            "rounds": competition_rounds,
            "seasons": competition_seasons,
        }
    )

def teamview(request, teamId):
    try:
        team = TeamsManager().TeambyId(teamId=int(teamId))
        if team.national_team:
            return redirect('team', teamId=team.abbr)
        else:
            players = PlayersManager().getPlayersbyTeamId(team.id)
            youth_players = PlayersManager().getYouthPlayersbyTeamId(team.id)
    except ValueError:
        team = TeamsManager().getNationalTeam(teamAbbr=teamId.upper())
        players = PlayersManager().getPlayersofNationalTeam(team.abbr)
        youth_players = False

    return render(
        request=request,
        template_name = "teamview.html",
        context = {
            "team": team,
            "players": players,
            "youth_players": youth_players
        }
    )

def playerview(request, playerId):
    player = PlayersManager().PlayerbyId(playerId=playerId)
    nation_team = TeamsManager().getNationalTeam(teamAbbr=player.nationality.abbr)
    return render(
        request=request,
        template_name = "playerview.html",
        context = {
            "player": player,
            "nation_team": nation_team,
        }
    )

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        messages.error(request, 'Wrong password.')
        return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

class SearchPlayerView(ListView):
    template_name = "searchview.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchPlayerView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        if query is not None:
            search_results = {
                "teams": TeamsManager().TeamsbyName(teamName=query),
                "players": PlayersManager().PlayersbyName(playerName=query),
                "nations": TeamsManager().NationsbyName(nationName=query),
            }
            return search_results
        return None

def ajax(request, ajaxAction):
    if ajaxAction == "select_season":
        seasonId = request.GET.get("season")

        rounds_query_set = CompetitionsManager().RoundsOfCompetitionSeason(competitionSeasonId=seasonId)
        rounds = []
        for season_round in rounds_query_set:
            season_round.teams = CompetitionsManager().getTeamPerformances(competitionSeasonRoundId=season_round.id)
            rounds.append(season_round)

        return render(
            request=request,
            template_name = "blocks/seasonview.html",
            context = {
                "rounds": rounds,
            }
    )

        


