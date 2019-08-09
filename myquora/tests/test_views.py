from django import urls
import pytest
import pprint
from django.contrib.sessions.models import Session
from myquora.models import Question, Author


@pytest.mark.django_db
def test_question_update_success(authenticated_user, create_a_question):
    """creating a question"""
    client, author = authenticated_user
    question = create_a_question
    url = urls.reverse('question-update', kwargs={'pk': question.id})
    response = client.get(url)
    updated_question = {'question_text': "Newdfdf"}
    response = client.post(url, updated_question, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_to_login_when_update_question(create_a_question, client, django_user_model):
    """Verify we redirect to the login page when a user
       tries to update a new question
     """
    question = create_a_question
    url = urls.reverse('question-update', kwargs={'pk': question.id})
    resp = client.get(url)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_redirect_to_login_when_add_question(client, django_user_model):
    """Verify we redirect to the login page when a user
       tries to add a new question
     """
    url = urls.reverse('question-add')
    resp = client.get(url)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_redirect_to_login(create_a_question, client, django_user_model):
    question = create_a_question
    url = urls.reverse('question-detail', kwargs={'pk': question.id})
    response = client.get(url, follow=True)
    assert b'myquora/author/add/?next=/myquora/question/1' in response.content
    assert response.context['question'].question_text == question.question_text


# @pytest.mark.django_db
# def test_redirect_to_login_when_logged_out_from_update_question(client):
#     """Verify we redirect to the marketing page when a user is not logged in"""
#     question = Question(fill waith)
#     question.save()


#     url = urls.reverse('answer-update', kwargs={'pk': 2})
#     resp = client.get(url)
#     print('*************************************')
#     # pprint.pprint(resp.__dict__, indent=5)
#     assert resp.status_code == 302
#     # assert b'answer List' in resp.content
