from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

def generate_code():
    return f"NeedsQR{str(random.randint(100000000, 999999999))}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return jsonify({'code': generate_code()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
