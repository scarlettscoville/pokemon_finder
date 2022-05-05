from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import LoginForm, PokemonForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, logout_user, login_user, login_required

# Routes
@app.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
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

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        # Doing the Login stuff :)
        email = form.email.data.lower()
        password = form.password.data

        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('index'))
        flash('Incorrect Email/Password combo. Please try again.', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template("login.html.j2", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name" : form.first_name.data.title(),
                "last_name" : form.last_name.data.title(),
                "email" : form.email.data.lower(),
                "password" : form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()

        except:
            flash("There was an unexpected error creating your account. Please try again later.", "danger")
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered with PokeFind!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out.', 'warning')
        return redirect(url_for('login'))