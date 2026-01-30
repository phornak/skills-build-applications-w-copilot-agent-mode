from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models


from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Teams
        marvel_team = {'name': 'Team Marvel', 'description': 'Marvel superheroes'}
        dc_team = {'name': 'Team DC', 'description': 'DC superheroes'}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Users
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team_id': dc_team_id},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user_id': user_ids[0], 'type': 'Run', 'duration': 30, 'distance': 5},
            {'user_id': user_ids[1], 'type': 'Swim', 'duration': 45, 'distance': 2},
            {'user_id': user_ids[2], 'type': 'Bike', 'duration': 60, 'distance': 20},
            {'user_id': user_ids[3], 'type': 'Yoga', 'duration': 50, 'distance': 0},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 110},
            {'user_id': user_ids[3], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Morning Cardio', 'description': 'Cardio for all'},
            {'name': 'Strength Training', 'description': 'Strength for all'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
