from app import db, login
from flask_login import UserMixin #for user moddel!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default= dt.utcnow)

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

    #select * from user where id = ??
@login.user_loader
def load_user(id):
    return User.query.get(int(id))