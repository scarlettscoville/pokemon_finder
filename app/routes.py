from flask import render_template, request
import requests
from .forms import LoginForm
from .forms import PokemonForm
from app import app

# Routes
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        # Doing the Login stuff :)
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get("REGISTERED_USERS") and password == app.config.get("REGISTERED_USERS").get(email).get('password'):
            return f"Login successful! Welcome, {app.config.get('REGISTERED_USERS').get(email).get('name')}!"
        error_string = "Incorrect email/password combo."
        return render_template("login.html.j2", form=form)

    return render_template("login.html.j2", form=form)

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    form = PokemonForm()
    if request.method == 'POST':
        name = request.form.get('name').lower()

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if not response.ok:
            error_string = "There was an error...did you spell the name correctly?"
            return render_template("pokemon.html.j2", error=error_string)

        if not response.json():
            error_string = "Please re-enter...that Pokemon does not exist!"
            return render_template("pokemon.html.j2", error=error_string)

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