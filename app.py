from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)

from routes import *
from models import *



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)