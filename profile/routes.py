from flask import render_template, request, session, redirect, url_for, flash
from profile import app, db, bcrypt, mail
from profile.forms import LoginForm, UpdateProfileForm, BlogForm, RequestResetForm, ResetPasswordForm
from profile.models import User, Blogs, Testimonials, Projects, Contacts
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.all()
    blogs = Blogs.query.order_by(Blogs.date_posted.desc())
    testimonials = Testimonials.query.all()
    projects = Projects.query.all()

    if request.method == 'POST':
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, mobile=mobile, message=message)
        db.session.add(entry)
        db.session.commit()
        # getting bad credentials error while using this use if any other way else remove it
        # mail.send_message('New Message from' + name,
        #                   sender=email,
        #                   recipients = 'ricks14348@gmail.com',
        #                   body = message + "\n" + mobile
        #                   )

    return render_template('index.html', user=user, blogs=blogs, testimonials=testimonials, projects=projects)


@app.route('/blog/<int:id>', methods=['GET'])
def blog_route(id):
    user = User.query.all()
    blog = Blogs.query.filter_by(id=id).first()
    blogs = Blogs.query.all()
    return render_template('blog.html', blog=blog, user=user, blogs=blogs)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('signin.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.designation = form.designation.data
        current_user.age = form.age.data
        current_user.mobile = form.mobile.data
        current_user.address = form.address.data
        current_user.github_url = form.github_url.data
        current_user.linkedin_url = form.linkedin_url.data
        current_user.fb_url = form.fb_url.data
        current_user.skype_id = form.skype_id.data
        db.session.commit()
        flash('Your profile details updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.designation.data = current_user.designation
        form.age.data = current_user.age
        form.mobile.data = current_user.mobile
        form.address.data = current_user.address
        form.github_url.data = current_user.github_url
        form.linkedin_url.data = current_user.linkedin_url
        form.fb_url.data = current_user.fb_url
        form.skype_id.data = current_user.skype_id
    user = User.query.filter_by(id=1).first()
    return render_template('/profile.html', user=user, form=form)


@app.route('/editblogs', methods=['GET', 'POST'])
@login_required
def editblogs():
    blogs = Blogs.query.all()
    return render_template('editBlogs.html', blogs=blogs)


@app.route('/edit/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blogs(title=form.title.data, description=form.content.data, image=form.image.data)
        db.session.add(blog)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect('/editblogs')
    return render_template('edit.html', form=form, heading='New Blog')


@app.route('/edit/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    blog = Blogs.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.description = form.content.data
        blog.image = form.image.data
        db.session.commit()
        flash('Your Blog has been updated.', 'success')
        return redirect(url_for('editblogs'))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.description
        form.image.data = blog.image
    return render_template('edit.html', form=form, blog=blog, heading='Update Blog')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = Blogs.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('editblogs'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To Reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this mail and no change will happen to your account
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('your password has been updated. You are now able to login now', 'success')
        return request(url_for('login'))
    return render_template('reset_token.html', form=form)


