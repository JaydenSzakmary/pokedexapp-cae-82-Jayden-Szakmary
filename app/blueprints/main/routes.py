from .import bp as main
from flask import render_template, request
import requests
from flask_login import  login_required
from .forms import SearchForm



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


