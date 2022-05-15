from app import db, login
from flask_login import UserMixin, current_user
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import re

class PokeFind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    pokemon = db.relationship('Pokemon', secondary = 'pokefind', backref = 'users', lazy = 'dynamic',)
    win = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/pixel-art/{self.icon}.svg'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def collect_poke(self, poke):
        self.pokemon.append(poke)
        db.session.commit()

    def remove_poke(self, poke):
        self.pokemon.remove(poke)
        db.session.commit()

class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hp = db.Column(db.Integer)
    exp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    ability = db.Column(db.String)

    def __repr__(self):
        return f'<Pokemon: {self.poke_id} | {self.name}>'

    def poke_from_dict(self, pokemon_data):
        self.name = pokemon_data['pokemon']
        self.ability = pokemon_data['ability']
        self.experience = pokemon_data['experience']
        self.sprite = pokemon_data['sprite']
        self.attack = pokemon_data['attack']
        self.hp = pokemon_data['hp']
        self.defense = pokemon_data['defense']

    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))