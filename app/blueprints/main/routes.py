from flask import render_template, request, flash
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required

# Routes
@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm
    if request.method == 'POST':
        name = request.form.get('name').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if not response.ok:
            flash("There was an error...did you spell the name correctly?", "danger")
            return render_template("pokemon.html.j2", form=form)

        if not response.json():
            flash("Please re-enter...that Pokemon does not exist!", "danger")
            return render_template("pokemon.html.j2", form=form)

        data = response.json()
        
        new_data = []
        pokemon_dict = {
            "name": data["species"]["name"].title(),
            "sprite": data["sprites"]["front_shiny"],
            "base_experience": data["base_experience"],
            "ability_name": data["abilities"][0]["ability"]["name"],
            "attack_base": data["stats"][1]["base_stat"],
            "hp_base": data["stats"][0]["base_stat"],
            "defense_base":data["stats"][2]["base_stat"],
        }
        new_data.append(pokemon_dict)

        return render_template("pokemon.html.j2", table = new_data, form=form)
    return render_template("pokemon.html.j2", form=form)