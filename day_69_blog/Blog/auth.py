from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import current_user, logout_user, login_url, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            found_user = User.query.filter_by(email=form.email.data).one()
        except:
            flash('Email not in database.', category='Error')
        else:
            if check_password_hash(found_user.password, form.password.data):
                login_user(found_user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='Error')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            pass_hash = generate_password_hash(form.password.data, method='sha256', salt_length=8)
            new_user = User(name=form.name.data, email=form.email.data, password=pass_hash)
            db.session.add(new_user)
            db.session.commit()
        except:
            flash('Email already registered. Login instead.', category='Error')
            return redirect(url_for('auth.login'))
        else:
            flash('Registered successfully', category='Success')
            login_user(new_user)
            return redirect(url_for('views.home'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))