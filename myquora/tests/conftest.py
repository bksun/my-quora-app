from __future__ import print_function
from django.contrib.auth.models import User
from myquora.models import Question, Answer, Comment, Author
import pytest


@pytest.fixture
@pytest.mark.django_db
def authenticated_user(client, django_user_model):
    """Create an authenticated user for test"""
    user = django_user_model.objects.create_user(username='test', password='test123')
    author = Author.objects.create(user=user)
    client.login(username='test', password='test123')
    return (client, author)


@pytest.fixture
@pytest.mark.django_db
def create_a_question(client, django_user_model):
    user = django_user_model.objects.create_user(username='test1', password='test1123')
    author = Author.objects.create(user=user)
    question = Question.objects.create(author=author, question_text="some question")
    return question
