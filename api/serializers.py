from tkinter.tix import NoteBook

from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Game, Score


# this makes me sad

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"