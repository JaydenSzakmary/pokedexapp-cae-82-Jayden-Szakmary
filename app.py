from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pokedex', methods = ['GET','POST'])
def pokedex():
    if request.method == 'POST':
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
            return render_template('pokedex.html', pokemon = new_data)
        else:
            error_msg = f"Pokemon not found! {name} is not registered in the global Pokedex!"
            return render_template('pokedex.html', error = error_msg)
    return render_template('pokedex.html')