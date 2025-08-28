from flask import Flask, jsonify, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import csv
import io
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/codes.db'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'codes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)


class CodeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(9), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def generate_code():
    while True:
        code = str(random.randint(100000, 999999))
        if not CodeEntry.query.filter_by(code=code).first():
            return f"NeedsQR-{code}"

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str).strip()

    query = CodeEntry.query

    if search_query:
        query = query.filter(CodeEntry.code.contains(search_query))

    query = query.order_by(CodeEntry.timestamp.desc())

    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html',
                           history=pagination.items,
                           pagination=pagination,
                           search_query=search_query)


@app.route('/generate')
def generate():
    code = generate_code()
    entry = CodeEntry(code=code)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'code': code})


@app.route('/export')
def export_csv():
    entries = CodeEntry.query.order_by(CodeEntry.timestamp.desc()).all()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Code', 'Timestamp'])  # Header
    for entry in entries:
        cw.writerow([entry.code, entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')])

    output = si.getvalue()
    return Response(
        output,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=code_history.csv'
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
