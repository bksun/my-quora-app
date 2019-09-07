import pytest
from django import urls


@pytest.mark.django_db
def test_question_update_success(authenticated_user, create_a_question):
    """creating a question"""
    client, author = authenticated_user
    question = create_a_question
    url = urls.reverse('question-update', kwargs={'pk': question.id})
    updated_question = {'question_text': "Newdfdf"}
    response = client.post(url, updated_question, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_to_login_when_logged_out_from_update_question(
  authenticated_user, create_a_question):
    """Verify we redirect to the login page when a user is logged out"""
    client, author = authenticated_user
    question = create_a_question
    url = urls.reverse('question-update', kwargs={'pk': question.id})
    client.logout()
    resp = client.get(url)
    assert '/accounts/login/?next=/myquora/question/{0}/update/'.format(str(question.id)) in resp.url
    assert resp.status_code == 302
    resp = client.get(url, follow=True)
    assert b'Username:' in resp.content
    assert b'Password:' in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_redirect_to_login_when_update_question(create_a_question, client, django_user_model):
    """Verify we redirect to the login page when a user
       tries to update a new question
     """
    question = create_a_question
    url = urls.reverse('question-update', kwargs={'pk': question.id})
    client.logout()
    # since question is by autheenticated author
    resp = client.get(url)
    assert '/accounts/login/?next=/myquora/question/{0}/update/'.format(str(question.id)) in resp.url
    assert resp.status_code == 302
    resp = client.get(url, follow=True)
    assert b'Username:' in resp.content
    assert b'Password:' in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_redirect_to_login_when_add_question(client):
    """Verify we redirect to the login page when a user
       tries to add a new question
     """
    url = urls.reverse('question-add')
    resp = client.get(url)
    # pprint.pprint(resp.__dict__)
    assert '/accounts/login/?next=/myquora/question/add/' in resp.url
    assert resp.status_code == 302
    resp = client.get(url, follow=True)
    assert b'Username:' in resp.content
    assert b'Password:' in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_question_detail_login_not_required(create_a_question, client):
    question = create_a_question
    url = urls.reverse('question-detail', kwargs={'pk': question.id})
    response = client.get(url)
    assert b'Answer this question' in response.content
    assert response.context['question'].question_text == question.question_text
