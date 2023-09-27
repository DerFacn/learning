from app.deco import get_log, logged_in
import sqlalchemy.exc
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
@logged_in
@get_log
def register(log=None):
    if request.method == 'POST':  # If user send form
        username = request.form['username']  # Fetch username
        password = request.form['password']  # Fetch password
        if username is None:  # Checking username is not None
            flash('Username required!')  # Flash error
        elif password is None:  # Checking password is not None
            flash('Password required!')  # Flash error
        hashed_password = generate_password_hash(password)  # Hash password for store in database
        new_user = User(username=username, password=hashed_password)  # Create new user
        try:
            db.session.add(new_user)  # Add user to database
            db.session.commit()  # Accept commit - write a new user to database
        except sqlalchemy.exc.IntegrityError:  # If user already in database
            flash('User already exists!')  # Flash error
        return redirect(url_for('auth.login'))  # Success!
    return render_template('auth/form.html', title='Register', action='register', log=log)
    # If someone just come to our register url


@bp.route('/login', methods=['GET', 'POST'])
@logged_in
@get_log
def login(log=None):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None:
            flash('Username required!')
        if password is None:
            flash('Password required!')
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User not exists!')
        if not check_password_hash(user.password, password):
            flash('Wrong password! Try again!')
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('blog.index'))
    return render_template('auth/form.html', title='Login', action='login', log=log)


@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
