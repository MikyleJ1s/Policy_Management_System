import pytest
from flask.testing import FlaskClient
from flask import Flask, url_for
from policy_management_system import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login(client: FlaskClient):
    response = client.get('/')
    assert response.status_code ==200
    assert b"login" in response.data

def test_logging_out(client: FlaskClient):
    response = client.get('/logging_out')
    assert client.get(url_for('login')).status_code == 200

def test_user_login(client: FlaskClient):
    response = client.get('/login')
    assert client.get(url_for('user_policies')).status_code == 200
   

def test_policies(client: FlaskClient):
    response = client.get('/fetch_policies')
    assert client.get(url_for('user_policies')).status_code == 200
  

def test_payments(client: FlaskClient):
    response = client.get('/payments')
    assert response.status_code ==200
    assert b"Pay" in response.data

def test_settings(client: FlaskClient):
    response = client.get('/settings')
    assert response.status_code ==200
    assert b"Update" in response.data


def test_stats(client: FlaskClient):
    response = client.get('/statistics')
    assert response.status_code ==200
    # assert b"stats" in response.data




