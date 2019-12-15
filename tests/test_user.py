def test_get_users(test_client, init_db):
    response = test_client.get('/users/')

    assert response.status_code == 200
    assert b'rlveiga' in response.data