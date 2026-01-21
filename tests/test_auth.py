from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


# Precisa ser email no nosso caso! Tome cuidado caso mude!
def test_unauthorized_username(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token == {'detail': 'Incorrect email or password'}


# Nao pode ser a senha hash! Exemplo no teste para lembrar disso!
def test_unauthorized_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token == {'detail': 'Incorrect email or password'}


def test_token_expired_after_time(client, user):
    # Para o tempo nessa data e hora
    with freeze_time('2023-07-15 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        token = response.json()['access_token']
        assert response.status_code == HTTPStatus.OK

    with freeze_time('2023-07-15 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-15 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-15 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
