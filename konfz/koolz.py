# -*- coding: utf-8 -*-

from flask import Flask

# Flask init
app = Flask(__name__)

def run():
    app.config.update(dict(SECRET_KEY='oui'))
    app.run(host='0.0.0.0', debug=True)

# Routes
@app.route('/')
def home():
    return 'Hello'

# Main
if __name__ == '__main__':
    run()
