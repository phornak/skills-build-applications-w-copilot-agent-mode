from django.test import TestCase
from .models import User, Team, Activity, Leaderboard, Workout

class BasicModelTest(TestCase):
    def test_team_creation(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        self.assertEqual(str(team), 'Test Team')

    def test_user_creation(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        self.assertEqual(str(user), 'Test User')

    def test_activity_creation(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        activity = Activity.objects.create(user=user, type='Run', duration=30, distance=5.0)
        self.assertEqual(str(activity), 'Test User - Run')

    def test_leaderboard_creation(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        leaderboard = Leaderboard.objects.create(user=user, points=100)
        self.assertEqual(str(leaderboard), 'Test User - 100')

    def test_workout_creation(self):
        workout = Workout.objects.create(name='Morning Cardio', description='Cardio for all')
        self.assertEqual(str(workout), 'Morning Cardio')
