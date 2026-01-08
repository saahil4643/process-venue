"""
Views for the Me-API Playground.

Implements REST API endpoints for profile, projects, skills, and search functionality.
"""

from django.db.models import Count, Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile, Skill, Project
from .serializers import (
    ProfileSerializer,
    ProjectSerializer,
    SkillWithCountSerializer,
)


class HealthCheckView(APIView):
    """
    Health check endpoint.
    
    GET /health -> {"status": "ok"}
    """
    
    def get(self, request):
        return Response({"status": "ok"})


class ProfileView(APIView):
    """
    Single-user profile endpoint.
    
    GET    /api/profile  -> Retrieve the profile
    POST   /api/profile  -> Create a new profile
    PUT    /api/profile  -> Update the existing profile
    """
    
    def get(self, request):
        """Retrieve the profile (assumes single-user, returns first profile)."""
        profile = Profile.objects.first()
        if not profile:
            return Response(
                {"detail": "No profile found. Create one first."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        """Create a new profile."""
        # Check if profile already exists (single-user constraint)
        if Profile.objects.exists():
            return Response(
                {"detail": "Profile already exists. Use PUT to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update the existing profile."""
        profile = Profile.objects.first()
        if not profile:
            return Response(
                {"detail": "No profile found. Create one first with POST."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(APIView):
    """
    Project list endpoint with optional skill filtering.
    
    GET /api/projects              -> List all projects
    GET /api/projects?skill=Python -> List projects with "Python" skill
    """
    
    def get(self, request):
        """List projects, optionally filtered by skill name."""
        skill_name = request.query_params.get('skill')
        
        if skill_name:
            # Filter projects by skill name (case-insensitive)
            projects = Project.objects.filter(
                skills__name__iexact=skill_name
            ).distinct()
        else:
            projects = Project.objects.all()
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TopSkillsView(APIView):
    """
    Top skills endpoint.
    
    GET /api/skills/top -> Skills ordered by number of associated projects
    """
    
    def get(self, request):
        """Return skills ordered by project count (descending)."""
        skills = Skill.objects.annotate(
            project_count=Count('projects')
        ).order_by('-project_count')
        
        serializer = SkillWithCountSerializer(skills, many=True)
        return Response(serializer.data)


class SearchView(APIView):
    """
    Search endpoint.
    
    GET /api/search?q=python -> Search across profile name, skills, and project titles
    """
    
    def get(self, request):
        """
        Search across multiple models.
        
        Returns matching results categorized by type:
        - profiles: Profiles where name matches
        - skills: Skills where name matches
        - projects: Projects where title matches
        """
        query = request.query_params.get('q', '').strip()
        
        if not query:
            return Response(
                {"detail": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search profiles by name
        profiles = Profile.objects.filter(name__icontains=query)
        
        # Search skills by name
        skills = Skill.objects.filter(name__icontains=query)
        
        # Search projects by title
        projects = Project.objects.filter(title__icontains=query)
        
        return Response({
            "query": query,
            "results": {
                "profiles": [
                    {"id": p.id, "name": p.name, "email": p.email}
                    for p in profiles
                ],
                "skills": [
                    {"id": s.id, "name": s.name}
                    for s in skills
                ],
                "projects": [
                    {"id": p.id, "title": p.title, "description": p.description[:100] + "..." if len(p.description) > 100 else p.description}
                    for p in projects
                ],
            }
        })
