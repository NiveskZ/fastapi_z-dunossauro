from http import HTTPStatus


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
