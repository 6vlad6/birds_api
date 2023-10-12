import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from birds.models import *
from birds.serializers import *

from datetime import datetime


@pytest.mark.django_db
def test_get_birdseen_total_correct():
    """
    Тест получения количества BirdSeen по bird_id
    """
    api_client = APIClient()

    user_1 = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    user_2 = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='bb')
    bird = Bird.objects.create(name='aa', color='bb')
    birdseen_1 = BirdSeen.objects.create(user_id=user_1, bird_id=bird)
    birdseen_2 = BirdSeen.objects.create(user_id=user_2, bird_id=bird)

    url = reverse('bird-seen-total', kwargs={'bird_id': bird.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
            'status': 'success',
            'bird_id': bird.id,
            'seen_total': 2,
    }
    assert response.data == expected_data

@pytest.mark.django_db
def test_get_birdseen_total_incorrect():
    """
    Тест получения неправильного количества BirdSeen по bird_id
    """
    api_client = APIClient()

    user_1 = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    user_2 = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='bb')
    bird = Bird.objects.create(name='aa', color='bb')
    birdseen_1 = BirdSeen.objects.create(user_id=user_1, bird_id=bird)
    birdseen_2 = BirdSeen.objects.create(user_id=user_2, bird_id=bird)

    url = reverse('bird-seen-total', kwargs={'bird_id': bird.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
            'status': 'success',
            'bird_id': bird.id,
            'seen_total': 3,
    }
    assert response.data != expected_data

@pytest.mark.django_db
def test_get_birdseen_total_error():
    """
    Тест получения количества BirdSeen по несуществующему bird_id
    """
    api_client = APIClient()

    url = reverse('bird-seen-total', kwargs={'bird_id': 9})
    response = api_client.get(url)

    expected_data = {
        'status': 'fail',
        'message': f'Bird with Id: 9 not found'
    }

    assert response.data == expected_data
    assert response.status_code == status.HTTP_404_NOT_FOUND
