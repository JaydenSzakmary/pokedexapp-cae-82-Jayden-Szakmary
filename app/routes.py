from app import app
from .forms import LoginForm, RegisterForm, SearchForm
import requests
from flask import Flask , render_template, request, flash, redirect, url_for
from .models import User
from flask_login import login_user, login_user ,current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pokedex', methods = ['GET','POST'])
def pokedex():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            new_data = []
            print(new_data)
            poke_dict = {}
            poke_name=f"{ name }" 
            poke_dict={
                "form_name": data['forms'][0]['name'], 
                "abilities": data['abilities'][0]['ability']['name'],
                "base_xp": data['base_experience'],
                "sprite_url" : data['sprites']['versions']['generation-vii']['ultra-sun-ultra-moon']['front_shiny'],
                }
            new_data.append(poke_dict)
            print(new_data)
            return render_template('pokedex.html', pokemon = new_data, form=form)
        else:
            error_msg = f"Pokemon not found! {name} is not registered in the global Pokedex!"
            return render_template('pokedex.html', error = error_msg)
    return render_template('pokedex.html', form=form)


@app.route('/login', methods=['GET','POST'])
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

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('logout successful', 'success')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
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