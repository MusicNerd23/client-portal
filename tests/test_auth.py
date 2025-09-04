
def test_login_logout(client):
    # Test login
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

    # Test logout via POST (CSRF disabled in tests)
    response = client.post('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
