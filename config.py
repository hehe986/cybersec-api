# 23.83.0981 - Muhammad Ardita Hilmi
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cybersec_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cybersec-uts-0981-amikom'
db = SQLAlchemy(app)
app.app_context().push()

def hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()