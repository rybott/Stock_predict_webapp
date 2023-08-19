from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#Tutorial was a note taking webapp
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # Automatically adds the date and time of the note 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Adding the user who created the note
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #Creating a relationship with other tables
    notes = db.relationship('Note')