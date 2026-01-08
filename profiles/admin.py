"""
Django admin configuration for Me-API models.
"""

from django.contrib import admin
from .models import Profile, Skill, Project


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_skills']
    search_fields = ['title', 'description']
    filter_horizontal = ['skills']
    
    def get_skills(self, obj):
        return ", ".join([s.name for s in obj.skills.all()])
    get_skills.short_description = 'Skills'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    search_fields = ['name', 'email']
    filter_horizontal = ['skills', 'projects']
