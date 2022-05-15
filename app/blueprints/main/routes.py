from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required, current_user
from app.models import Pokemon, PokeTeam

# Routes
@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/poketeam', methods = ['GET', 'POST'])
def poketeam():
    team = current_user.team.all()
    return render_template('poketeam.html.j2', team=team)

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm
    if request.method == 'POST':
        name = request.form.get('name').lower()

        url = f'https://pokeapi.co/api/v2/pokemon/{name}'.lower()
        response = requests.get(url)
        if not response.ok:
            flash("There was an error...did you spell the name correctly?", "danger")
            return render_template("pokemon.html.j2", form=form)

        if not response.json():
            flash("Please re-enter...that Pokemon does not exist!", "danger")
            return render_template("pokemon.html.j2", form=form)

        data = response.json()
        
        pokemon_dict = {
            "name": data["species"]["name"].title(),
            "sprite": data["sprites"]["front_shiny"],
            "base_experience": data["base_experience"],
            "ability_name": data["abilities"][0]["ability"]["name"],
            "attack_base": data["stats"][1]["base_stat"],
            "hp_base": data["stats"][0]["base_stat"],
            "defense_base":data["stats"][2]["base_stat"],
        }
        
        p = Pokemon.query.filter_by(name = pokemon_dict['name']).first()
        if p in current_user.team.all():
            caught=True;
        else:
            caught = False;

        if p:
            pass
        else:
            p=Pokemon()
            p.from_dict(pokemon_dict)
            p.save()

        return render_template("pokemon.html.j2", pokemon=pokemon_dict, form=form, pokemon_id = p.pokemon_id, caught=caught)
    return render_template("pokemon.html.j2", form=form)

@main.route('/catch/<int:id>', methods = ['GET', 'POST'])
def catch(id):
    if len(current_user.team.all()) == 5:
        flash('Only five Pokémon to a team, please!', 'danger')
        return redirect(url_for('main.pokemon'))
    flash('You have added a Pokémon to your team!', 'success')

    p = Pokemon.query.filter_by(pokemon_id = id).first()
    current_user.edit_team(p)
    current_user.save()

    return redirect(url_for('main.pokemon'))

@main.route('/release/<int:id>', methods = ['GET', 'POST'])
def release(id):
    p = Pokemon.query.filter_by(pokemon_id = id).first()
    current_user.remove(p)
    current_user.save()
    flash('You have released a Pokémon from your team.', 'danger')
    return redirect(url_for('main.pokemon'))


