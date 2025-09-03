from . import client
from app.models import User, Organization
from app import db

def test_org_scoping(client):
    # Create a user and organization
    org = Organization(name='Test Org', slug='test-org')
    user = User(email='test@example.com', role='client', org_id=org.id)
    user.set_password('password')
    db.session.add(org)
    db.session.add(user)
    db.session.commit()

    # Login the user
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)

    # Try to access a resource in another organization
    response = client.get('/org/1/dashboard', follow_redirects=True)
    assert response.status_code == 403
