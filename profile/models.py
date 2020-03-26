from datetime import datetime
from profile import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='img_avatar.jpg')
    designation = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(40), nullable=False)
    address = db.Column(db.Text(300), nullable=False)
    github_url = db.Column(db.String(180), nullable=False)
    linkedin_url = db.Column(db.String(180), nullable=False)
    fb_url = db.Column(db.String(180), nullable=False)
    skype_id = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.image_file}', '{self.email}', '{self.mobile}')"


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(40), nullable=False)
    message = db.Column(db.Text(500), nullable=False)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(180), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


class Testimonials(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(120), nullable=False)
    test_comment = db.Column(db.Text(500), nullable=False)
    test_caption = db.Column(db.String(180), nullable=False)


class Projects(db.Model):
    proj_id = db.Column(db.Integer, primary_key=True)
    proj_title = db.Column(db.String(120), nullable=False)
    proj_desc = db.Column(db.Text(500), nullable=False)
    proj_url = db.Column(db.String(80), nullable=False)
    proj_tag = db.Column(db.String(300), nullable=False)
    proj_stacks = db.Column(db.String(180), nullable=False)
    proj_img = db.Column(db.String(80), nullable=False)
