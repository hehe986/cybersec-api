# 23.83.0981 - Muhammad Ardita Hilmi
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///cybersec_api.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cybersec-uts-0981-amikom'
db = SQLAlchemy(app)
app.app_context().push()

def hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()
