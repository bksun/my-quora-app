from django import urls
import pytest
import pprint
from myquora.models import Question, Author


# @pytest.mark.django_db
# def test_question_update_success(authenticated_user, create_a_question):
#     """creating a question"""
#     client, author = authenticated_user
#     question = create_a_question
#     url = urls.reverse('question-update', kwargs={'pk': question.id})
#     updated_question = {'question_text': "Newdfdf"}
#     response = client.post(url, updated_question, follow=True)
#     assert response.status_code == 200

