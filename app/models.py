from app import db, login
from flask_login import UserMixin #for user moddel!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref


class User_Pokemon(db.Model):
    __tablename__= 'user_pokemon'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'),primary_key=True)
    


class Pokemon(db.Model):
    __tablename__= 'pokemon'
    poke_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),unique=True)
    abilities = db.Column(db.String(150))
    base_hp = db.Column(db.Integer)
    sprite_url = db.Column(db.String(1500))
    

    def __repr__(self):
        return f'<Pokemon: {self.poke_id} | {self.name}>'

    def from_dict(self, data):
        self.name = data['form_name']
        self.abilities = data['abilities']
        self.base_hp = data['base_hp']
        self.sprite_url = data['sprite_url']
    
    def save_to_db(self):
        db.session.add(self)  #add tghe yser ti seession
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default= dt.utcnow)
    mons = db.relationship('Pokemon',secondary='user_pokemon',lazy='dynamic',backref='trainer')

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    #SALTS AND HASHES PSSWRD
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    #COMPARES USER PASSWORD TO PASSOWRD IN THE LOGIN FORM
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password,login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    #saves user to database
    def save_to_db(self):
        db.session.add(self)  #add tghe yser ti seession
        db.session.commit()  #save everything in the session to database

    def save_mons(self,poke):
        self.mons.append(poke)
        print(self.mons)
        print('hello')
        db.session.commit()

    def remove_mons(self,poke):
        self.mons.remove(poke)
        print(self.mons)
        print('hello')
        db.session.commit()   

    #select * from user where id = ??



@login.user_loader
def load_user(id):
    return User.query.get(int(id))