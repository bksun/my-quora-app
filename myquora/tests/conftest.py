from __future__ import print_function
import pytest
from myquora.models import Answer, Author, Question


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
def create_a_question(authenticated_user, client):
    client, author = authenticated_user
    question = Question.objects.create(author=author, question_text="some question")
    return question


@pytest.fixture
@pytest.mark.django_db
def create_an_answer(authenticated_user, create_a_question, client):
    client, author = authenticated_user
    question = create_a_question
    answer = Answer.objects.create(author=author, question=question, answer_text="some answer")
    return answer
