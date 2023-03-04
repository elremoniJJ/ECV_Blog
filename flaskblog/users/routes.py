from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post

from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccoutForm

from flaskblog.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already registered and logged in', 'info')
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in', 'info')
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)

            next_page = request.args.get('next')    # Reference to login?next=%2Faccount

            # The 'success' argument is taken directly from bootstrap css
            flash(f'You are logged in with {form.email.data}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            # The 'danger' argument is taken directly from bootstrap css
            flash(f'Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html',
                           title='Login',
                           form=form)


@users.route("/logout")
@login_required
def logout():
    # logout extension already knows the credentials of a user already logged in
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_already_logged_in']
    flash(f'You have logged out successfully', 'info')
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccoutForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 'image_file' reference to database column for User

    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form)



@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/all_users")
@login_required
def all_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)


@users.route("/all_users/<string:user_email>/delete_user", methods=['GET', 'POST'])
@login_required
def delete_user(user_email):
    flash(f"Deleted - {user_email} - ", 'warning')


    return redirect(url_for('main.home'))


