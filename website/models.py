from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = "groupe5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe5@localhost/scrapy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


    
class Ebay(db.Model):
    __tablename__ = 'ebay'
    id = db.Column(db.Integer(), primary_key=True)
    titre = db.Column(db.String(255))
    prix = db.Column(db.String(255))
   
class Olx(db.Model):
    __tablename__ = 'olx'
    id = db.Column(db.Integer(), primary_key=True)
    titre = db.Column(db.String(5000))
    prix = db.Column(db.String(5000))
    
class Flipkart(db.Model):
    __tablename__ = 'flipkart'
    id = db.Column(db.Integer(), primary_key=True)
    prix = db.Column(db.String(255))
    titre = db.Column(db.String(255))
    
   

if __name__=="__main__":
    db.drop_all()
    db.create_all()
    