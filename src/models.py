from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.name,
            "population": self.population
        }
    
# class People(db.Model):

#     id = db.Column(db.Integer, primary_key=True, nullable=True)
#     name = db.Column(db.String(250), nullable=True)
#     age = db.Column(db.String(250))

#     def __repr__(self):
#         return '<People %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "people name": self.name,
#             "age": self.age
#         }


