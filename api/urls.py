from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.get_all_users, name = "users"),
    path("users/<str:name>", views.get_user, name = "user"),
    path("scores/", views.get_all_scores, name = "scores"),
    path("scores/<str:name>", views.get_user_scores, name = "user_scores"),
    path("games/", views.get_all_games, name = "games"),
    path("leaderboard/", views.get_leaderboard, name = "leaderboard"),
]