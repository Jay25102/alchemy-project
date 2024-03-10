from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLACHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):
        """add a sample user to start"""
        User.query.delete()

        user = User(first_name="johnny", last_name="test")
        db.session.add(user)
        db.session.commit()

        post = Post(title="some title", content="blog post content here", user_id=1)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        db.session.flush()
        db.session.rollback()

    def test_root_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            #This only works if the redirection debug page is enabled
            self.assertIn('Redirecting...', html)

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('johnny test', html)

    def test_edit_page(self):
        with app.test_client() as client:
            resp = client.get("/users/1/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Change First Name', html)

    def test_new_page(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add', html)

    def test_users_post(self):
        with app.test_client as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('some title', html)