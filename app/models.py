from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class PokeTeam(db.Model):
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
    pokemon = db.relationship('Pokemon', 
                    secondary = 'poke_team', 
                    backref = 'users', 
                    lazy = 'dynamic'
                    )
    win_count = db.Column(db.Integer, default=0)
    loss_count = db.Column(db.Integer, default=0)

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))  


class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sprite = db.Column(db.String)
    experience = db.Column(db.String)
    ability = db.Column(db.String)
    attack = db.Column(db.String)
    hp = db.Column(db.String)
    defense = db.Column(db.String)

    def __repr__(self):
        return f'<Pokemon: {self.poke_id} | {self.name}>'

    def pokemon_from_dict(self, pokemon_data):
        self.name = pokemon_data['name']
        self.sprite = pokemon_data['sprite']
        self.experience = pokemon_data['base_experience']
        self.ability = pokemon_data['ability_name']
        self.attack = pokemon_data['attack_base']
        self.hp = pokemon_data['hp_base']
        self.defense = pokemon_data['defense_base']


    def save(self):
        db.session.add(self)
        db.session.commit()


