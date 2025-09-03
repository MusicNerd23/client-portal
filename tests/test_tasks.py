from . import client

def test_tasks_page(client):
    # Login the user
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)

    response = client.get('/tasks/')
    assert response.status_code == 200
    assert b'Tasks' in response.data
