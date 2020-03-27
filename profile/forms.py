from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from profile.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    designation = StringField('Designation', validators=[DataRequired(), Length(min=2, max=40)])
    age = IntegerField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=300)])
    github_url = StringField('GitHub Link', validators=[DataRequired(), Length(min=2, max=80)])
    linkedin_url = StringField('LinkedIn Link', validators=[DataRequired(), Length(min=2, max=80)])
    fb_url = StringField('Facebook Link', validators=[DataRequired(), Length(min=2, max=80)])
    skype_id = StringField('Skype Id', validators=[DataRequired(), Length(min=2, max=80)])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('That name is already exist.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already exist.')

    def validate_designation(self, designation):
        if designation.data != current_user.designation:
            user = User.query.filter_by(designation=designation.data).first()
            if user:
                raise ValidationError('That designation is already exist.')

    def validate_age(self, age):
        if age.data != current_user.age:
            user = User.query.filter_by(age=age.data).first()
            if user:
                raise ValidationError('That age is already exist.')

    def validate_mobile(self, mobile):
        if mobile.data != current_user.mobile:
            user = User.query.filter_by(mobile=mobile.data).first()
            if user:
                raise ValidationError('That mobile is already exist.')

    def validate_address(self, address):
        if address.data != current_user.address:
            user = User.query.filter_by(address=address.data).first()
            if user:
                raise ValidationError('That address is already exist.')

    def validate_github_url(self, github_url):
        if github_url.data != current_user.github_url:
            user = User.query.filter_by(github_url=github_url.data).first()
            if user:
                raise ValidationError('That github_url is already exist.')

    def validate_linkedin_url(self, linkedin_url):
        if linkedin_url.data != current_user.linkedin_url:
            user = User.query.filter_by(linkedin_url=linkedin_url.data).first()
            if user:
                raise ValidationError('That linkedin_url is already exist.')

    def validate_fb_url(self, fb_url):
        if fb_url.data != current_user.fb_url:
            user = User.query.filter_by(fb_url=fb_url.data).first()
            if user:
                raise ValidationError('That fb_url is already exist.')

    def validate_skype_id(self, skype_id):
        if skype_id.data != current_user.skype_id:
            user = User.query.filter_by(skype_id=skype_id.data).first()
            if user:
                raise ValidationError('That skype_id is already exist.')


class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = StringField('Image File', validators=[DataRequired()])
    submit = SubmitField('Post')