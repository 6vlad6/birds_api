import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from birds.models import *
from birds.serializers import *

from datetime import datetime


@pytest.mark.django_db
def test_get_birdseens_not_empty():
    """
    Тест получения заполненного массива BirdSeen
    """
    api_client = APIClient()
    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')
    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird)

    url = reverse('bird-seens-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['bird_seens']) == 1


@pytest.mark.django_db
def test_get_birdseens_empty():
    """
    Тест получения пустого массива BirdSeen
    """
    api_client = APIClient()

    url = reverse('bird-seens-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['bird_seens']) == 0

    expected_data = [
    ]
    assert response.data['bird_seens'] == expected_data

@pytest.mark.django_db
def test_get_birdseen_exist():
    """
    Тест получения существующего BirdSeen
    """
    api_client = APIClient()

    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')
    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird)

    response = api_client.get(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}))

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_birdseen_not_exist():
    """
    Тест получения несуществующего BirdSeen
    """
    api_client = APIClient()

    response = api_client.get(reverse('bird-seen-detail', kwargs={'birdseen_id': 9}))

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_create_birdseen_correct():
    """
    Тест правильного создания BirdSeen
    """
    api_client = APIClient()

    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')

    data = {
        'user_id': user,
        'bird_id': bird,
    }
    response = api_client.post(reverse('bird-seens-list'), data=data)

    assert response.status_code == status.HTTP_201_CREATED

    birdseen = BirdSeen.objects.get(user_id=response.data['data']['bird_seen']['user_id'],
                                    bird_id=response.data['data']['bird_seen']['bird_id'])
    assert birdseen.user_id == user
    assert birdseen.bird_id == bird

@pytest.mark.django_db
def test_create_birdseen_no_bird():
    """
    Тест создания BirdSeen с пустым bird_id
    """
    api_client = APIClient()

    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')

    data = {
        'user_id': user,
    }

    response = api_client.post(reverse('bird-seens-list'), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_bird_no_user():
    """
    Тест создания BirdSeen с пустым user_id
    """
    api_client = APIClient()

    bird = Bird.objects.create(name='aa', color='bb')

    data = {
        'bird_id': bird,
    }
    response = api_client.post(reverse('bird-seens-list'), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_birdseen_user_correct():
    """
    Тест обновления BirdSeen правильным user_id
    """
    api_client = APIClient()
    user_1 = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    user_2 = CustomUser.objects.create(password='user12345', first_name='viewer', last_name='common', username='bb')
    bird = Bird.objects.create(name='aa', color='bb')

    birdseen = BirdSeen.objects.create(user_id=user_1, bird_id=bird)

    data = {
        'user_id': user_2,
    }
    response = api_client.patch(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}), data=data)

    assert response.status_code == status.HTTP_200_OK

    birdseen.refresh_from_db()
    assert birdseen.user_id == user_2
    assert birdseen.bird_id == bird

@pytest.mark.django_db
def test_update_birdseen_bird_correct():
    """
    Тест обновления BirdSeen правильным bird_id
    """
    api_client = APIClient()
    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird_1 = Bird.objects.create(name='aa', color='bb')
    bird_2 = Bird.objects.create(name='cc', color='dd')

    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird_1)

    data = {
        'bird_id': bird_2,
    }
    response = api_client.patch(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}), data=data)

    assert response.status_code == status.HTTP_200_OK

    birdseen.refresh_from_db()
    assert birdseen.user_id == user
    assert birdseen.bird_id == bird_2

@pytest.mark.django_db
def test_update_birdseen_no_user():
    """
    Тест обновления BirdSeen пустым user_id
    """
    api_client = APIClient()

    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')

    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird)

    data = {
        'user_id': '',
    }
    response = api_client.patch(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_birdseen_no_bird():
    """
    Тест обновления BirdSeen пустым bird_id
    """
    api_client = APIClient()

    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')

    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird)

    data = {
        'bird_id': '',
    }
    response = api_client.patch(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_birdseen_correct():
    """
    Тест удаления существующего BirdSeen
    """
    api_client = APIClient()
    user = CustomUser.objects.create(password='user12345', first_name='user', last_name='common', username='aa')
    bird = Bird.objects.create(name='aa', color='bb')

    birdseen = BirdSeen.objects.create(user_id=user, bird_id=bird)

    response = api_client.delete(reverse('bird-seen-detail', kwargs={'birdseen_id': birdseen.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not BirdSeen.objects.filter(id=birdseen.id).exists()

@pytest.mark.django_db
def test_delete_birdseen_error():
    """
    Тест удаления несуществующего BirdSeen
    """
    api_client = APIClient()

    response = api_client.delete(reverse('bird-seen-detail', kwargs={'birdseen_id': 9}))

    assert response.status_code == status.HTTP_404_NOT_FOUND