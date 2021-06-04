import unittest
from flask_login import current_user
from miloblog.models import User
from miloblog import app, db


class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False
        self.client = app.test_client()
        db.create_all()
        # if not User.query.filter_by(username='test'):
        self.user_data = {'email': 'test@mail.com', 'password': 'test_password', 'username': 'test'}
        if not User.query.filter_by(email=self.user_data['email']).first():
            self.user = User(email=self.user_data['email'],
                             username=self.user_data['username'],
                             password=self.user_data['password'])
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_login_logout(self):
        with self.client:
            response = self.client.post('/login', data={
                'email': self.user_data['email'],
                'password': self.user_data['password']
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, self.user_data['username'])

            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)
            self.assertFalse(current_user.is_authenticated)

    def test_login_required(self):
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response.location, 'http.*/login.*')

    def test_index(self):
        response = self.client.get('/')
        self.assertIn('Milo', str(response.data))
