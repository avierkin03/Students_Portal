from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Voting, Option, Vote

class VotingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.moderator = User.objects.create_user(username='moderator', password='12345')
        group = Group.objects.create(name='Moderators')
        self.moderator.groups.add(group)
        self.voting = Voting.objects.create(
            title="Test Voting",
            description="Test Description",
            start_date="2023-01-01T00:00:00Z",
            end_date="2023-12-31T23:59:59Z",
            created_by=self.moderator
        )
        self.option1 = Option.objects.create(voting=self.voting, text="Option 1")
        self.option2 = Option.objects.create(voting=self.voting, text="Option 2")

    def test_voting_creation(self):
        self.assertEqual(self.voting.title, "Test Voting")
        self.assertEqual(self.voting.options.count(), 2)

    def test_vote_unique(self):
        Vote.objects.create(user=self.user, voting=self.voting, option=self.option1)
        with self.assertRaises(Exception):
            Vote.objects.create(user=self.user, voting=self.voting, option=self.option2)