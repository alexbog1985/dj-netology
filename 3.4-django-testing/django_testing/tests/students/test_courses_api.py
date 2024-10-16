import pytest
import random

from django.urls import reverse

from students.models import Course


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    """Тест получения первого курса"""

    courses = course_factory(_quantity=10)
    url = reverse("courses-detail", args=[courses[0].id])

    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['name'] == courses[0].name


@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    """Тест получения списка курсов"""

    courses = course_factory(_quantity=10)
    url = reverse("courses-list")

    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_id_filter_course(client, course_factory):
    """Тест фильтрации по id"""

    courses = course_factory(_quantity=10)
    rnd_index = random.randint(0, len(courses) - 1)
    rnd_id = courses[rnd_index].id
    url = reverse("courses-list")

    response = client.get(url + f'?id={str(rnd_id)}')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == courses[rnd_index].name


@pytest.mark.django_db
def test_name_filter_course(client, course_factory):
    """Тест фильтрации по названию"""

    courses = course_factory(_quantity=10)
    names_count = 0
    rnd_index = random.randint(0, len(courses) - 1)
    rnd_name = courses[rnd_index].name
    url = reverse("courses-list")

    response = client.get(url + f'?name={rnd_name}')

    for course in courses:
        if course.name == rnd_name:
            names_count += 1
    assert response.status_code == 200
    assert len(response.json()) == names_count
    for course in response.json():
        assert course['name'] == courses[rnd_index].name


@pytest.mark.django_db
def test_create_course(client, course_factory, student_factory):
    """Тест создания курса"""

    count = Course.objects.count()
    student = student_factory()
    course_data = {
        'name': 'Test course',
        'student': student.id,
    }
    url = reverse("courses-list")

    response = client.post(url, data=course_data)

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    """Тест обновления курса"""

    course = course_factory()
    student = student_factory()
    course_data = {
        'name': 'Test course',
        'student': student.id,
    }
    url = reverse("courses-detail", args=[course.id])

    response = client.put(url, data=course_data)

    assert response.status_code == 200
    assert Course.objects.get(id=course.id).name == 'Test course'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    """Тест удаления курса"""

    course = course_factory()
    count = Course.objects.count()
    url = reverse("courses-detail", args=[course.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
@pytest.mark.parametrize('max_count, students_count, status_code', [(20, 25, 400), (20, 15, 201), (20, 20, 201)])
def test_max_limit_students_course(settings, client, course_factory, student_factory,
                                   max_count, students_count, status_code):
    """Тест максимального количества студентов на курсе"""

    settings.MAX_STUDENTS_PER_COURSE = max_count
    course = course_factory()
    students = student_factory(_quantity=students_count)
    student_data = {
        'name': 'Test student',
        'course': course.id,
        'student': [student.id for student in students]
    }
    url = reverse("courses-list")

    response = client.post(url, data=student_data)

    assert response.status_code == status_code
