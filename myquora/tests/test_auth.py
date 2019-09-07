import pytest
from django import urls

from myquora.models import Author, Question


@pytest.mark.django_db
def test_author_register_success(client, django_user_model):
    user = django_user_model.objects.create_user(username='test1', password='test123')
    author = Author.objects.create(user=user, email="test1@g.com")
    assert isinstance(author, Author)
    url = urls.reverse('author-add')
    user_details = {
      'username': 'bksun1212',
      'email': 'sonu123@g.com',
      'password1': 'Sonu@123',
      'password2': 'Sonu@123'
    }
    response = client.post(url, user_details, follow=True)
    assert b'Username' in response.content
    assert b'Password' in response.content
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_when_logged_out_from_unsecure_links_like_home_page(
  authenticated_user):
    """
      Verify we don't redirect to the login page when a user is logged 
      out from unsecure links like home page
    """
    client, author = authenticated_user
    url = urls.reverse('index')
    client.logout()
    resp = client.get(url)
    assert b'Authors' in resp.content
    assert b'Answers' in resp.content
    assert b'Questions' in resp.content
    assert b'Comments' in resp.content
    assert resp.status_code == 200
