from django.contrib.auth.models import User
from myquora.models import Question, Answer, Comment, Author
from mixer.backend.django import mixer
import pytest


# @pytest.mark.django_db
# def authenticated_user_setup():
#     print('*******************Set Up********************')
#     user = User.objects.create(username='test14', password='Test1pass')
#     user.save()
#     author = Author.objects.create(user=user, email='sun@gm.in')
#     author.save()
#     return author
#     print('*******************Tear Down********************')


@pytest.mark.django_db
class TestModels:
    def __init__(self):
        self.auth = None

    def test_author_object(self, authenticated_user):
        print('*******************Get Author Object********************')
        print(authenticated_user)
        print('*******************Done Get Author Object********************')

    def get_author_object(self):
        return self.auth


class Testing:
    test = TestModels()
    # test.create_author_object()

    @pytest.mark.django_db
    def test_create_question(self, authenticated_user):
        user = User.objects.create(username='test14', password='Test1pass')
        user.save()
        author = Author.objects.create(user=user, email='sun@gm.in')
        author.save()
        que = Question.objects.create(author=authenticated_user, question_text='Who is DDM?')
        print(que)
        print(type(que))
        assert 'Who is DDM' in que
