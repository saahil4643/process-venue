"""
Models for the Me-API Playground.

Defines Profile, Skill, and Project models with their relationships.
"""

from django.db import models


class Skill(models.Model):
    """
    Represents a skill that can be associated with profiles and projects.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Represents a project with associated skills.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    links = models.JSONField(default=dict, blank=True, help_text="JSON object with link names as keys and URLs as values")
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Profile(models.Model):
    """
    Single-user profile containing personal and professional information.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    education = models.TextField(blank=True)
    work = models.TextField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    
    # Relationships
    skills = models.ManyToManyField(Skill, related_name='profiles', blank=True)
    projects = models.ManyToManyField(Project, related_name='profiles', blank=True)

    def __str__(self):
        return self.name
