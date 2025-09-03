from . import client

def test_files_page(client):
    # Login the user
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)

    response = client.get('/files/')
    assert response.status_code == 200
    assert b'Files' in response.data
