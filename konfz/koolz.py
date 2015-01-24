# -*- coding: utf-8 -*-

import os

from flask import (
    Flask,
    render_template,
    request,
)


# Flask
app = Flask(__name__)

def run():
    app.config.update(dict(SECRET_KEY='oui'))
    app.run(host='0.0.0.0', debug=True)


# Confz
JSON_DIR = '{0}/{1}'.format(app.root_path, 'data')


# JSON
jsons = dict()

def lookup(hint):
    pass

def jsons_load():
    for kernel in os.listdir(JSON_DIR):
        jsons[kernel] = None

# Routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/k/<kernel>', methods=['GET', 'POST'])
def home(kernel=None):
    if not kernel or kernel not in jsons:
        kernel = jsons.keys()[0]
    if request.method == 'POST' and 'hint' in request.form:
        hits = lookup(request.form['hint'])
    return render_template('home.html', kernel=kernel)

@app.route('/switch')
def switch():
    return render_template('switch.html', kernels=jsons.keys())

# Main
if __name__ == '__main__':
    json_load()
    run()
