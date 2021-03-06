import os
import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        app.app.config['TESTING'] = True
        app.db.session.close()
        app.db.drop_all()
        app.db.create_all()
        app.add_user('admin', 'password', 1)
        app.add_user('investor', 'password', 0)

    def tearDown(self):
        pass

    # usefull functions

    def register(self, username, email):
        return self.app.post('/personal', data=dict(
            username=username,
            email=email,
            doRegister='doRegister'
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # tests

    def test_login(self):
        rv = self.login('admin', 'password')
        assert b'User successfully logged' in rv.data

    def test_not_logged(self):
        rv = self.app.get('/home')
        assert b'Unauthorized' in rv.data

    def test_login_without_register(self):
        rv = self.login('user', 'password')
        assert b'Given username ' in rv.data  # I can't put the ' character because this test will fail.

    def test_add_user_not_in_investor(self):
        self.login('investor', 'password')
        rv = self.app.get('/personal')
        assert b'Add new user' not in rv.data

    def test_register_without_admin(self):
        self.login('investor', 'password')
        rv = self.register('user', 'user@foreverfunds.com')
        assert b'Unauthorized' in rv.data

    def test_access_register_with_admin(self):
        self.login('admin', 'password')
        rv = self.app.get('/personal')
        assert b'Add new user' in rv.data

    def test_register_with_admin(self):
        self.login('admin', 'password')
        rv = self.register('user', 'user@foreverfunds.com')
        assert b'New user sucessfully created!' in rv.data

    def test_password_change_works(self):
        self.login('investor', 'password')
        rv = self.app.post('/personal',data=dict(
            old_password='password',
            new_password1='new_password',
            new_password2='new_password',
            changePassword="changePassword"
        ), follow_redirects=True)
        self.logout()
        self.login('investor', 'new_password')
        assert b'This page will be the dashboard with summary about funds and research' in rv.data

    def test_password_change_not_works_1(self):
        self.login('admin', 'password')
        rv = self.app.post('/personal', data=dict(
            old_password='password1',
            new_password1='new_password',
            new_password2='new_password',
            changePassword="changePassword"
        ), follow_redirects=True)
        assert b'Wrong password!' in rv.data

    def test_password_change_not_works_2(self):
        self.login('admin', 'password')
        rv = self.app.post('/personal', data=dict(
            old_password='password',
            new_password1='new_password1',
            new_password2='new_password',
            changePassword="changePassword"
        ), follow_redirects=True)
        assert b'Passwords don' in rv.data

    def test_add_user_that_exists(self):
        self.login('admin', 'password')
        rv = self.register('investor', 'user@foreverfunds.com')
        assert b"Given username already exists!" in rv.data

if __name__ == '__main__':
    unittest.main()