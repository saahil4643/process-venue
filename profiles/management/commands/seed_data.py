"""
Management command to seed the database with sample data.

Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from profiles.models import Profile, Skill, Project


class Command(BaseCommand):
    help = 'Seeds the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create skills
        skills_data = [
            'Python', 'Django', 'Django REST Framework', 'JavaScript',
            'React', 'PostgreSQL', 'Docker', 'Git', 'AWS', 'HTML/CSS'
        ]
        skills = {}
        for name in skills_data:
            skill, created = Skill.objects.get_or_create(name=name)
            skills[name] = skill
            if created:
                self.stdout.write(f'  Created skill: {name}')

        # Create projects
        projects_data = [
            {
                'title': 'E-Commerce API',
                'description': 'A RESTful API for an e-commerce platform with product management, cart, and checkout functionality.',
                'links': {
                    'github': 'https://github.com/example/ecommerce-api',
                    'demo': 'https://api.example.com'
                },
                'skills': ['Python', 'Django', 'Django REST Framework', 'PostgreSQL']
            },
            {
                'title': 'Task Manager App',
                'description': 'A full-stack task management application with real-time updates and team collaboration features.',
                'links': {
                    'github': 'https://github.com/example/task-manager',
                    'live': 'https://tasks.example.com'
                },
                'skills': ['React', 'JavaScript', 'Django', 'Docker']
            },
            {
                'title': 'Portfolio Website',
                'description': 'Personal portfolio website showcasing projects and skills with a modern, responsive design.',
                'links': {
                    'github': 'https://github.com/example/portfolio',
                    'live': 'https://portfolio.example.com'
                },
                'skills': ['HTML/CSS', 'JavaScript', 'React']
            },
            {
                'title': 'DevOps Pipeline',
                'description': 'CI/CD pipeline setup with automated testing, containerization, and cloud deployment.',
                'links': {
                    'github': 'https://github.com/example/devops-pipeline'
                },
                'skills': ['Docker', 'AWS', 'Git', 'Python']
            },
        ]

        projects = []
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=proj_data['title'],
                defaults={
                    'description': proj_data['description'],
                    'links': proj_data['links']
                }
            )
            if created:
                project.skills.set([skills[s] for s in proj_data['skills']])
                self.stdout.write(f'  Created project: {proj_data["title"]}')
            projects.append(project)

        # Create profile
        profile, created = Profile.objects.get_or_create(
            email='john.doe@example.com',
            defaults={
                'name': 'John Doe',
                'education': 'B.S. Computer Science, Example University (2020-2024)',
                'work': 'Software Engineering Intern at Tech Corp (Summer 2023)\nFreelance Web Developer (2022-Present)',
                'github': 'https://github.com/johndoe',
                'linkedin': 'https://linkedin.com/in/johndoe',
                'portfolio': 'https://johndoe.dev',
            }
        )
        
        if created:
            # Associate skills and projects with profile
            profile.skills.set([
                skills['Python'], skills['Django'], skills['JavaScript'],
                skills['React'], skills['Git'], skills['Docker']
            ])
            profile.projects.set(projects)
            self.stdout.write(f'  Created profile: {profile.name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
