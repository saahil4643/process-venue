"""
URL configuration for the profiles app.
"""

from django.urls import path
from .views import (
    ProfileView,
    ProjectListView,
    TopSkillsView,
    SearchView,
)

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('projects', ProjectListView.as_view(), name='projects'),
    path('skills/top', TopSkillsView.as_view(), name='top-skills'),
    path('search', SearchView.as_view(), name='search'),
]
