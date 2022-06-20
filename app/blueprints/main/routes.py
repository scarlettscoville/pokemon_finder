from flask import render_template, request, flash, redirect, url_for
import requests
from ...forms import PokemonForm
from .import bp as main
from flask_login import login_required, current_user
from app.models import Pokemon, PokeTeam, User
import random

# Routes
@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')


@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm
    if request.method == 'POST' and form.validate_on_submit:
        name = form.name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        pokemon = response.json()

        pokemon_dict = {
            "name": pokemon["species"]["name"].title(),
            "sprite": pokemon["sprites"]["front_shiny"],
            "base_experience": pokemon["base_experience"],
            "ability_name": pokemon["abilities"][0]["ability"]["name"],
            "attack_base": pokemon["stats"][1]["base_stat"],
            "hp_base": pokemon["stats"][0]["base_stat"],
            "defense_base": pokemon["stats"][2]["base_stat"],
        }
        new_pokemon=Pokemon()
        new_pokemon.poke_from_dict(pokemon_dict)
        new_pokemon.save()

        new_poketeam=PokeTeam()
        new_poketeam.user_id=current_user.id
        new_poketeam.poke_id=new_pokemon.poke_id
        my_pokemon=PokeTeam.query.filter_by(user_id=current_user.id).all()

        pokemons=''
        my_names=[]
        pokemon_list=[]
        for entry in my_pokemon:
            p=Pokemon.query.filter_by(poke_id=entry.poke_id).first().name
            my_names.append(p)
        
        if new_pokemon.name in my_names:
            flash(f'Pokemon already on team. Please choose a different Pokemon.', 'danger')
        else:
            if len(my_names) < 5:
                current_user.collect.poke(new_pokemon)
            else:
                flash('Your team is full!', 'danger')

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

@main.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    users=User.query.filter(User.id != current_user.id).all()
    all_users = {}
    for user in users:
        pokemons = user.pokemon.all()
        pokemon_list=pokemons[:5]
        all_users[user.id]=pokemon_list

    return render_template('battle.html.j2', pokemons=all_users, users=users)

@main.route('/battle_view/<int:id>', methods=['GET', 'POST'])
@login_required
def battle_view(id):
    user=User.query.get(id)
    print('poke battle current_user: ', current_user.id)
    print('poke battle user: ', user.id)
    if request.method == 'GET':
        choice = [0,1]
        selection = random.choice(choice)
        print('Selection: ', selection)

        if selection == 1:
            current_user.loss_count += 1
            user.win_count += 1
            flash('You have lost this battle.', 'danger')
        else:
            current_user.win_count += 1
            user.loss_count += 1
            flash('You won this battle!', 'success')
        current_user.save()
        user.save()
    users = User.query.all()
    all_users = {}
    for user in users:
        pokemons = user.pokemon.all()
        pokemon_list = pokemons[:5]
        all_users[user.id]=pokemon_list

    return render_template('battle.html.j2', users=users, pokemons=all_users)


@main.route('/delete_pokemon/<int:id>')
@login_required
def delete_pokemon(id):
    p=Pokemon.query.filter_by(poke_id=id).first()
    current_user.remove_poke(p)
    return redirect(url_for('main.pokemon_team'))
