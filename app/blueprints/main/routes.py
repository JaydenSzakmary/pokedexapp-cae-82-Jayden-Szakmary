from .import bp as main
from flask import render_template, request, flash
import requests
from flask_login import  current_user, login_required
from .forms import SearchForm
from app.models import Pokemon


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/pokedex', methods = ['GET','POST'])
@login_required
def pokedex():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            new_data = []
            poke_dict = {}
            poke_dict={
                "form_name": data['forms'][0]['name'], 
                "abilities": data['abilities'][0]['ability']['name'],
                "base_hp": data['stats'][0]['base_stat'],
                "sprite_url" : data['sprites']['versions']['generation-vii']['ultra-sun-ultra-moon']['front_shiny'],
                }
            new_data.append(poke_dict)
            try:
                new_poke_data = Pokemon()
                new_poke_data.from_dict(poke_dict)
                new_poke_data.save_to_db()
                flash("Pokemon added to local Pokedex!",'success')
            except:
                flash("Pokemon already in local Pokedex!",'warning') 
            return render_template('pokedex.html', pokemon = new_data, form=form)
        else:
            error_msg = f"Pokemon not found! {name} is not registered in the global Pokedex!"
            return render_template('pokedex.html',form=form, error = error_msg)
    return render_template('pokedex.html', form=form)


@main.route('/pokedex_add', methods = ['GET','POST'])
@login_required
def pokedex_add():
    form = SearchForm()
    poke = []
    if request.method == 'POST' and form.validate_on_submit():
        poke = Pokemon.query.filter_by(name=form.name.data.lower()).first()
        if poke:
            
            print(poke)
            if len(list(current_user.mons))>=5:
     
                current_user.save_mons(poke)
                flash('pokemon added to party successfully!','success')

            return render_template('pokedex_add.html', poke = poke, form=form)
        else:
            error_msg = f"Pokemon not found! is not registered in the global Pokedex!"
            return render_template('pokedex_add.html',form=form, error = error_msg)
    return render_template('pokedex_add.html',poke= poke , form=form)


@main.route('/pokedex_remove', methods = ['GET','POST'])
@login_required
def pokedex_remove():
    form = SearchForm()
    poke = []
    if request.method == 'POST' and form.validate_on_submit():
        
        poke = Pokemon.query.filter_by(name=form.name.data.lower()).first()
        if poke:
            
            
     
            current_user.remove_mons(poke)
            flash('pokemon removed from party successfully!','success')

            return render_template('pokedex_remove.html', poke = poke, form=form)
        else:
            error_msg = f"Pokemon not found! is not registered in the global Pokedex!"
            return render_template('pokedex_remove.html',form=form, error = error_msg)
    return render_template('pokedex_remove.html',poke= poke , form=form)

