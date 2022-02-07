from .import bp as auth
from .forms import LoginForm, RegisterForm, EditProfileForm
from flask import render_template, request, flash, redirect, url_for
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('welcome to swagbook', 'success')
            return redirect(url_for('index'))
        else:
            flash('try again', 'danger')    
            return render_template('login.html',form=form)
    return render_template('login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('logout successful', 'success')
        return redirect(url_for('login'))


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #create new user
        try:
            new_user_data = {
                'first_name':form.first_name.data.title(),
                'last_name':form.last_name.data.title(),
                'email':form.email.data.lower(),
                'password':form.password.data
            }
            #create an empty user
            new_user_object = User()
            #build user withdata
            new_user_object.from_dict(new_user_data)
            #save user to db
            new_user_object.save_to_db()
        except:
            flash("there was an unexpected error creating account",'danger')
            #error return
            return render_template('register.html', form=form)
        flash('User account registered!', 'success')
        return redirect(url_for('login'))
    #getrequest
    return render_template('register.html',form=form)


@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.email != current_user.email:
            flash('Email already in use','danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except:
            flash('There was an unexpected Error. Please Try again', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html', form = form)