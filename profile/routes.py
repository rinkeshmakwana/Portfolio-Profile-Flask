from flask import render_template, request, session, redirect, url_for, flash
from profile import app, db, bcrypt
from profile.forms import LoginForm, UpdateProfileForm
from profile.models import User, Blogs, Testimonials, Projects, Contacts
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.all()
    blogs = Blogs.query.all()
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
    return render_template('blog.html', blog=blog, user=user)


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
        flash('Your profile details updated','success')
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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST':
        inp_title = request.form.get('title')
        inp_content = request.form.get('content')
        inp_img = request.form.get('image')

        if id == 0:
            blog = Blogs(title=inp_title, description=inp_content, image=inp_img)
            db.session(blog)
            db.session.commit()
        else:
            blog = Blogs.query.filter_by(id=id).first()
            title = inp_title
            description = inp_content
            image = inp_img
            db.session.commit()
            return redirect('/editblogs')
    blog = Blogs.query.filter_by(id=id).first()

    return render_template('edit.html', blog=blog)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = Blogs.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('editblogs'))
