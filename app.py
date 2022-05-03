from flask import Flask, render_template, request
import requests


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url).json()
        if not response.ok:
            error_string = "There was an error...did you spell the name correctly?"
            return render_template("pokemon.html.j2", error=error_string)

        if not response.json():
            error_string = "Please re-enter...that Pokemon does not exist!"
            return render_template("pokemon.html.j2", error=error_string)
        data = response.json()
        pokemon_dict = {
            "name": data["species"]["name"],
            "sprite": data["sprites"]["front_shiny"],
            "base_experience": data["base_experience"],
            "ability_name": data["abilities"][0]["ability"]["name"],
            "attack_base": data["stats"][1]["base_stat"],
            "hp_base": data["stats"][0]["base_stat"],
            "defense_base":data["stats"][2]["base_stat"],
        }

        return render_template("pokemon.html.j2", table = pokemon_dict)
    return render_template("pokemon.html.j2")