from django import urls
import pytest
import pprint
from django.contrib.sessions.models import Session
from myquora.models import Question, Author



# @pytest.mark.django_db
# def test_redirect_to_memes_when_logged_in(authenticated_user, client):
#     """Verify we redirect to the memes page when a user is logged in"""
#     url = urls.reverse('answer-update', kwargs={'pk': 2})
#     resp = client.get(url)
#     pprint.pprint('Test-running...')
#     assert resp.status_code == 302
#     # assert resp.url == urls.reverse('answer-update', kwargs={'pk': 2})


# @pytest.mark.django_db
# def test_redirect_to_marketing_when_logged_out(client):
#     """Verify we redirect to the marketing page when a user is not logged in"""
#     question = Question(fill waith)
#     question.save()

    

#     url = urls.reverse('answer-update', kwargs={'pk': 2})
#     resp = client.get(url)
#     print('*************************************')
#     # pprint.pprint(resp.__dict__, indent=5)
#     assert resp.status_code == 302
#     # assert b'answer List' in resp.content


@pytest.mark.django_db
def test_redirect_to_login(client, django_user_model):
    user = django_user_model.objects.create_user(username='test', password='test123')
    author = Author.objects.create(user=user)
    question = Question.objects.create(author=author, question_text="some question")
    url = urls.reverse('question-detail', kwargs={'pk': question.id})
    response = client.get(url, follow=True)
    print(dir(response))
    print(response.status_code)
    assert response.context['question'].question_text == question.question_text
