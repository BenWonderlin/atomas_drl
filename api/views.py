from django.http import HttpResponse
from django.http import Http404

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from .models import Game, Score
from .serializers import UserSerializer, GameSerializer, ScoreSerializer


# users ---------------------------

@api_view(["GET"])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def get_user(request, name):
    users = User.objects.get(username = name)
    serializer = UserSerializer(users, many = False)
    return Response(serializer.data)



# games ---------------------------

@api_view(["GET"])
def get_all_games(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def get_new_game(request):
    pass

@api_view(["POST"])
def update_game(request, game):
    pass





# scores ---------------------------

@api_view(["GET"])
def get_all_scores(request):
    scores = Score.objects.all()
    serializer = UserSerializer(scores, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def get_user_scores(request, name):
    tmp_user = User.objects.get(username = name)
    scores = Score.objects.get(user = tmp_user.id)
    serializer = ScoreSerializer(scores, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def get_leaderboard(request):
    return HttpResponse("TODO")
