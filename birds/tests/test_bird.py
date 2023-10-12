import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from birds.models import *
from birds.serializers import *

from datetime import datetime


@pytest.mark.django_db
def test_get_birds_not_empty():
    """
    Тест получения заполненного массива Bird
    """
    api_client = APIClient()
    bird_1 = Bird.objects.create(name='aa', color='bb')
    bird_2 = Bird.objects.create(name='cc', color='dd')

    url = reverse('birds-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['birds']) == 2

    expected_data = [
        {
            'id': bird_1.id,
            'name': 'aa',
            'color':'bb',
        },
        {
            'id': bird_2.id,
            'name': 'cc',
            'color': 'dd',
        },
    ]
    assert response.data['birds'] == expected_data


@pytest.mark.django_db
def test_get_birds_empty():
    """
    Тест получения пустого массива Bird
    """
    api_client = APIClient()

    url = reverse('birds-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['birds']) == 0

    expected_data = [
    ]
    assert response.data['birds'] == expected_data

@pytest.mark.django_db
def test_get_bird_exist():
    """
    Тест получения существующего Bird
    """
    api_client = APIClient()

    bird = Bird.objects.create(name='aa', color='bb')

    response = api_client.get(reverse('bird-detail', kwargs={'bird_id': bird.id}))

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
            'id': bird.id,
            'name': 'aa',
            'color': 'bb',
        }
    assert response.data['data']['bird'] == expected_data

@pytest.mark.django_db
def test_get_bird_not_exist():
    """
    Тест получения несуществующего Bird
    """
    api_client = APIClient()

    response = api_client.get(reverse('bird-detail', kwargs={'bird_id': 9}))

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_create_bird_correct():
    """
    Тест правильного создания Bird
    """
    api_client = APIClient()

    data = {
        'name': 'aa',
        'color': 'bb',
    }
    response = api_client.post(reverse('birds-list'), data=data)

    assert response.status_code == status.HTTP_201_CREATED

    bird = Bird.objects.get(id=response.data['data']['bird']['id'])
    assert bird.name == 'aa'
    assert bird.color == 'bb'

@pytest.mark.django_db
def test_create_bird_no_color():
    """
    Тест создания Bird с пустым color
    """
    api_client = APIClient()

    data = {
        'name': 'aa',
    }
    response = api_client.post(reverse('birds-list'), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_bird_no_name():
    """
    Тест создания Bird с пустым name
    """
    api_client = APIClient()

    data = {
        'color': 'aa',
    }
    response = api_client.post(reverse('birds-list'), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_bird_correct():
    """
    Тест правильного обновления Bird
    """
    api_client = APIClient()
    bird = Bird.objects.create(name='aa', color='bb')

    data = {
        'name': 'aaa',
        'color': 'bbb'
    }
    response = api_client.patch(reverse('bird-detail', kwargs={'bird_id': bird.id}), data=data)

    assert response.status_code == status.HTTP_200_OK

    bird.refresh_from_db()
    assert bird.name == 'aaa'
    assert bird.color == 'bbb'

@pytest.mark.django_db
def test_update_bird_no_name():
    """
    Тест обновления Bird пустым name
    """
    api_client = APIClient()
    bird = Bird.objects.create(name='aa', color='bb')

    data = {
        'name': '',
        'color': 'bbb'
    }
    response = api_client.patch(reverse('bird-detail', kwargs={'bird_id': bird.id}), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_bird_no_color():
    """
    Тест обновления Bird пустым color
    """
    api_client = APIClient()
    bird = Bird.objects.create(name='aa', color='bb')

    data = {
        'name': 'aaa',
        'color': ''
    }
    response = api_client.patch(reverse('bird-detail', kwargs={'bird_id': bird.id}), data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_delete_bird_correct():
    """
    Тест удаления существующего Bird
    """
    api_client = APIClient()
    bird = Bird.objects.create(name='aa', color='bb')

    response = api_client.delete(reverse('bird-detail', kwargs={'bird_id': bird.id}))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Bird.objects.filter(id=bird.id).exists()


@pytest.mark.django_db
def test_delete_bird_error():
    """
    Тест удаления несуществующего Bird
    """
    api_client = APIClient()

    response = api_client.delete(reverse('bird-detail', kwargs={'bird_id': 9}))

    assert response.status_code == status.HTTP_404_NOT_FOUND