import pytest
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.mark.django_db
def test_api():
    client = APIClient()
    Student.objects.create(name='test', birth_date='2000-01-01')
    Course.objects.create(name='test')

    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
