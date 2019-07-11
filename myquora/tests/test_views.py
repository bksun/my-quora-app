from django import urls
import pytest
import pprint
from django.contrib.sessions.models import Session


@pytest.mark.django_db
def test_redirect_to_memes_when_logged_in(authenticated_user, client):
    """Verify we redirect to the memes page when a user is logged in"""
    url = urls.reverse('answer-update', kwargs={'pk': 2})
    resp = client.get(url)
    pprint.pprint('Test-running...')
    assert resp.status_code == 302
    # assert resp.url == urls.reverse('answer-update', kwargs={'pk': 2})


@pytest.mark.django_db
def test_redirect_to_marketing_when_logged_out(client):
    """Verify we redirect to the marketing page when a user is not logged in"""
    url = urls.reverse('answer-update', kwargs={'pk': 2})
    resp = client.get(url)
    print('*************************************')
    # pprint.pprint(resp.__dict__, indent=5)
    assert resp.status_code == 302
    # assert b'answer List' in resp.content
