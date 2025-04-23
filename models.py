from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id= db.Column(db.Integer, primary_key =True)
    username= db.Column(db.String(200))
    email=db.Column(db.String(100))

    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email
        }