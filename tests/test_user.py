import json

def test_login_success(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(email='rlveiga@gmail.com', password='abc123'))
    
    data = json.loads(response.data)

    assert data['success'] == True
    assert response.status_code == 200
    assert type(data['token']) is str

def test_login_fail(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(email='rlveiga@gmail.com', password='abcd1234'))

    data = json.loads(response.data)

    assert data['success'] == False
    assert response.status_code == 200

def test_login_not_found(test_client, init_db):
    response = test_client.post('/auth/login', json=dict(email='mark@fb.com', password='abc123'))

    data = json.loads(response.data)

    assert data['success'] == False
    assert response.status_code == 404