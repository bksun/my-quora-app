from django.contrib.auth.models import User
from myquora.models import Question, Answer, Comment, Author
import pytest


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user for a test"""
    user = User.objects.create(username='test4', password='Test1pass')
    user.save()
    author = Author.objects.create(user=user, email='sun@gm.in')
    author.save()
    client.login(username='bksun', password='Sunil@123')
    return author


@pytest.fixture
def question_created(authenticated_user):
    """creating a question"""
    question = Question.objects.create(author=auth)