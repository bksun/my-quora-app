import pytest
from django import urls


@pytest.mark.django_db
def test_update_answer_success(create_an_answer, client):
    """creating a answer"""
    answer = create_an_answer
    url = urls.reverse('answer-update', kwargs={'pk': answer.id})
    updated_answer = {'answer_text': "Modified"}
    resp = client.post(url, updated_answer, follow=True)
    ans = updated_answer['answer_text']
    ans = bytes(ans, 'utf-8')
    assert ans in resp.content
    assert b'Answer this question' in resp.content
    que = 'Que: {0}'.format(str(answer.question.question_text))
    que = bytes(que, 'utf-8')
    assert que in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_add_answer_form_success(create_a_question, client):
    """Verify we redirect to the login page when a user
       tries to add a new answer
     """
    question = create_a_question
    url = urls.reverse('answer-add', kwargs={'pk': question.id})
    resp = client.get(url)
    assert b'Write your answer' in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_add_answer_success(create_a_question, create_an_answer, client):
    """Verify we redirect to the login page when a user
       tries to add a new answer
     """
    question = create_a_question
    answer = create_an_answer
    url = urls.reverse('answer-add', kwargs={'pk': question.id})
    answer_object = {
        'author': answer.author, 'question': answer.question, 'answer_text': "new answer"
        }
    resp = client.post(url, answer_object, follow=True)
    assert b'Answer this question' in resp.content
    que = 'Que: {0}'.format(str(answer.question.question_text))
    que = bytes(que, 'utf-8')
    assert que in resp.content
    ans = answer_object['answer_text']
    ans = bytes(ans, 'utf-8')
    assert ans in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_redirect_to_login_when_add_answer(create_a_question, client):
    """Verify we redirect to the login page when a user
       tries to add a new answer
     """
    question = create_a_question
    url = urls.reverse('answer-add', kwargs={'pk': question.id})
    client.logout()
    resp = client.get(url)
    assert '/accounts/login/?next=/myquora/question/1/answer/' in resp.url
    assert resp.status_code == 302
    resp = client.get(url, follow=True)
    assert b'Username:' in resp.content
    assert b'Password:' in resp.content
    assert resp.status_code == 200


@pytest.mark.django_db
def test_upvote_answer(create_an_answer, client):
    answer = create_an_answer
    url = urls.reverse('answer-upvote', kwargs={'pk': answer.id})
    resp = client.post(url, follow=True)
    upvote1 = list(filter(lambda ans: (ans == answer), resp.context['answer_list']))[0].upvote
    resp = client.post(url, follow=True)
    assert b'Answer this question' in resp.content
    upvote2 = list(filter(lambda ans: (ans == answer), resp.context['answer_list']))[0].upvote
    assert upvote2 > upvote1
    assert resp.status_code == 200


@pytest.mark.django_db
def test_downvote_answer(create_an_answer, client):
    answer = create_an_answer
    url = urls.reverse('answer-downvote', kwargs={'pk': answer.id})
    resp = client.post(url, follow=True)
    downvote1 = list(filter(lambda ans: (ans == answer), resp.context['answer_list']))[0].downvote
    resp = client.post(url, follow=True)
    assert b'Answer this question' in resp.content
    downvote2 = list(filter(lambda ans: (ans == answer), resp.context['answer_list']))[0].downvote
    assert downvote2 > downvote1
    assert resp.status_code == 200


@pytest.mark.django_db
def test_comment(create_an_answer, client):
    answer = create_an_answer
    url = urls.reverse('comment-add', kwargs={'pk': answer.id})
    comment = {'comment_text': 'hgyc'}
    resp = client.post(url, comment, follow=True)
    resp = client.post(url, comment, follow=True)
    comment = comment['comment_text']
    assert resp.status_code == 200
    assert bytes(comment, 'utf-8') in resp.content
    assert b'Answer this question' in resp.content
    assert comment in resp.context['comment_dictionary'][answer.id].last().comment_text
