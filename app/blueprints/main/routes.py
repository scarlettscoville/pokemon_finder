from flask import redirect, render_template, request, flash, url_for
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required, current_user
from app.models import Pokemon, PokeFind, User
import random

# Routes
@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit:
        name = request.form.get('name').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
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

        new_pokemon=Pokemon()
        new_pokemon.poke_from_dict(pokemon_dict)
        new_pokemon.save()

        new_pokefind=PokeFind()
        new_pokefind.user_id=current_user.id
        new_pokefind.poke_id=new_pokemon.poke.id
        my_pokemon = PokeFind.query.filter_by(user_id = current_user.id).all()

        pokemons=''
        my_names=[]
        pokemon_list=[]
        for entry in my_pokemon:
            p=Pokemon.query.filter_by(poke_id = entry.poke_id).first().pokemon_name
            my_names.append(p)

        if new_pokemon.pokemon_name in my_names:
            flash(f"You already have this Pokémon. Please select another.", "danger")
        else:
            if len(my_names) < 5:
                current_user.collect_poke(new_pokemon)
            else:
                flash(f"Your team is full!", "danger")
        
        pokemons = current_user.pokemon.all()
        pokemon_list=pokemons[:5]

        return render_template('pokemon.html.j2', pokemons=pokemon_list, form=form)
    return render_template('pokemon.html.j2', form=form)

@main.route('/pokemon_team', methods=['GET', 'POST'])
@login_required
def pokemon_team():
    pokemons = current_user.pokemon.all()
    pokemon_list=pokemons[:5]
    return render_template('pokemon_team.html.j2', pokemons=pokemon_list)

@main.route('/pokemon_battle', methods=['GET', 'POST'])
@login_required
def pokemon_battle():
    users=User.query.filter(User.id != current_user.id).all()
    user_list = {}
    for user in users:
        pokemons = user.pokemon.all()
        pokemon_list=pokemons[:5]
        user_list[user.id]=pokemon_list
    return render_template('pokemon_battle.html.j2', pokemons=user_list, users=users)

# Actual battle...selecting winner/loser by random number
    # Want to update this to include battle by actual characteristics - hp, exp, etc.
@main.route('pokemon_battle_view/<int:id>', methods=['GET', 'POST'])
@login_required
def pokemon_battle_view(id):
    user=User.query.get(id)
    print("poke battle current_user: ", current_user.id)
    print("poke battle user: ", user.id)
    if request.method == 'GET':
        choice = [0,1]
        selection = random.choice(choice)
        print("Selection: ", selection)

        if selection == 1:
            current_user.loss += 1
            user.win += 1
            flash("You have lost this battle.", "danger")
        else:
            current_user.win += 1
            user.loss += 1
            flash(f"You won this battle!", "success")
        current_user.save()
        user.save()
    users = User.query.all()
    user_list = {}
    for user in users:
        pokemons = user.pokemon.all()
        pokemon_list=pokemons[:5]
        user_list[user.id]=pokemon_list

    return render_template('pokemon_battle.html.j2', users=users, pokemons=user_list)

@main.route('/delete_pokemon/<int:id>')
@login_required
def delete_pokemon(id):
    p = Pokemon.query.filter_by(poke_id=id).first()
    current_user.remove_poke(p)
    return redirect(url_for('main.pokemon_team'))