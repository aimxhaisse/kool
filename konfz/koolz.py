# -*- coding: utf-8 -*-

from flask import (
    Flask,
    render_template
)

# Flask init
app = Flask(__name__)

def run():
    app.config.update(dict(SECRET_KEY='oui'))
    app.run(host='0.0.0.0', debug=True)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Main
if __name__ == '__main__':
    run()
