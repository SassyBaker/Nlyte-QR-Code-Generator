from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/codes.db'
db = SQLAlchemy(app)

class CodeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(9), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

def generate_code():
    return str(random.randint(100000000, 999999999))

@app.route('/')
def index():
    history = CodeEntry.query.order_by(CodeEntry.timestamp.desc()).limit(10).all()
    return render_template('index.html', history=history)

@app.route('/generate')
def generate():
    code = generate_code()
    entry = CodeEntry(code=code)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'code': code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
