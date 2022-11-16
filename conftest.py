import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from django.test.client import Client

fake = Faker()
User = get_user_model()


@pytest.fixture(scope='session')
def faker():
    # global fake
    yield fake


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    from pprint import pp
    __builtins__['pp'] = pp
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run


@pytest.fixture(scope='function')
def user(db):
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        first_name='John Smith',
        phone='123456789',
        is_phone_valid=True
    )
    user.set_password('123456789')
    user.save()
    yield user


@pytest.fixture(scope='function')
def login_user(db):
    phone = '123456789'
    password = '123456789'
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        first_name='John Smith',
        phone=phone,
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'), data={'phone': phone,
                                                   'password': password})
    assert response.status_code == 302
    yield client, user
