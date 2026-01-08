"""
Serializers for the Me-API Playground.

Provides ModelSerializers with nested representations for Profile, Skill, and Project.
"""

from rest_framework import serializers
from .models import Profile, Skill, Project


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model."""
    
    class Meta:
        model = Skill
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model with nested skills."""
    skills = SkillSerializer(many=True, read_only=True)
    skill_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of skill names to associate with this project"
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'links', 'skills', 'skill_names']

    def create(self, validated_data):
        skill_names = validated_data.pop('skill_names', [])
        project = Project.objects.create(**validated_data)
        self._set_skills(project, skill_names)
        return project

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if skill_names is not None:
            self._set_skills(instance, skill_names)
        return instance

    def _set_skills(self, project, skill_names):
        """Create or get skills and associate them with the project."""
        skills = []
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip())
            skills.append(skill)
        project.skills.set(skills)


class ProjectMinimalSerializer(serializers.ModelSerializer):
    """Minimal project serializer for nested use in Profile."""
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'links', 'skills']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model with nested skills and projects.
    
    For write operations, accepts skill_names and project_ids.
    For read operations, returns full nested objects.
    """
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectMinimalSerializer(many=True, read_only=True)
    
    # Write-only fields for creating/updating relationships
    skill_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of skill names to associate with this profile"
    )
    project_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of project IDs to associate with this profile"
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'email', 'education', 'work',
            'github', 'linkedin', 'portfolio',
            'skills', 'projects',
            'skill_names', 'project_ids'
        ]

    def create(self, validated_data):
        skill_names = validated_data.pop('skill_names', [])
        project_ids = validated_data.pop('project_ids', [])
        
        profile = Profile.objects.create(**validated_data)
        self._set_skills(profile, skill_names)
        self._set_projects(profile, project_ids)
        return profile

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        project_ids = validated_data.pop('project_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if skill_names is not None:
            self._set_skills(instance, skill_names)
        if project_ids is not None:
            self._set_projects(instance, project_ids)
        return instance

    def _set_skills(self, profile, skill_names):
        """Create or get skills and associate them with the profile."""
        skills = []
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip())
            skills.append(skill)
        profile.skills.set(skills)

    def _set_projects(self, profile, project_ids):
        """Associate existing projects with the profile."""
        projects = Project.objects.filter(id__in=project_ids)
        profile.projects.set(projects)


class SkillWithCountSerializer(serializers.ModelSerializer):
    """Serializer for skills with project count."""
    project_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'project_count']
