# main configs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)



    def to_json(self):
        return {
            "id": self.id, 
            "date": self.date, 
            "description": self.description,
            "category": self.category,
            "amount": self.amount
        }
