from . import client

def test_threads_page(client):
    # Login the user
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)

    response = client.get('/threads/')
    assert response.status_code == 200
    assert b'Threads' in response.data
