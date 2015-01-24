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
LKDDB_DIR = '{0}/{1}'.format(app.root_path, 'data/lkddbs')


# LKDDB
lkddbs = dict()

def lookup(hint):
    pass

def lkddbs_load():
    for kernel in os.listdir(LKDDB_DIR):
        lkddbs[kernel] = None

# Routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/k/<kernel>', methods=['GET', 'POST'])
def home(kernel=None):
    if not kernel or kernel not in lkddbs:
        kernel = lkddbs.keys()[0]
    if request.method == 'POST' and 'hint' in request.form:
        hits = lookup(request.form['hint'])
    return render_template('home.html', kernel=kernel)

@app.route('/switch')
def switch():
    return render_template('switch.html', kernels=lkddbs.keys())

# Main
if __name__ == '__main__':
    lkddbs_load()
    run()
