import json

class TestUser
def test_login_success(test_client, init_db):
    response = test_client.post('/auth/login/', json=dict(email='rlveiga@gmail.com', password='abc123'))
    
    data = json.loads(response.data)

    assert data['success'] == True

def test_login_fail(test_client, init_db):
    response = test_client.post('/auth/login/', json=dict(email='rlveiga@gmail.com', password='abcd1234'))

    data = json.loads(response.data)

    assert data['success'] == False
