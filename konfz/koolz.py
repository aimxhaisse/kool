# -*- coding: utf-8 -*-

import os
import json
import re

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

def lookup(kernel, hint):
    m = re.match('CONFIG_(.*)', hint)
    if m:
        hint = m.group(1)
    result = []
    for config in jsons[kernel]:
        if hint in config:
            result.append(config)
    return result

def get_configs(kernel):
    return jsons[kernel].keys()

def json_load():
    for kernel in os.listdir(JSON_DIR):
        path = '{0}/{1}'.format(JSON_DIR, kernel)
        with open(path) as file:
            jsons[kernel] = json.load(file)


# Routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/k/<kernel>', methods=['GET', 'POST'])
def home(kernel=None):
    if not kernel or kernel not in jsons:
        kernel = jsons.keys()[0]
    hits = None
    hint = None
    if request.method == 'POST' and 'hint' in request.form:
        hint = request.form['hint']
        if len(hint) >= 3:
            hits = lookup(kernel, hint.upper())
    return render_template('home.html', kernel=kernel, hint=hint, hits=hits)

@app.route('/i/<kernel>')
def index(kernel):
    configs = get_configs(kernel)
    return render_template('index.html', kernel=kernel, configs=configs)

@app.route('/switch')
def switch():
    return render_template('switch.html', kernels=jsons.keys())

@app.route('/c/<kernel>/<cfg>')
def conf(kernel, cfg):
    conf = None
    if kernel in jsons:
        if cfg in jsons[kernel]:
            conf = jsons[kernel][cfg]
    return render_template('conf.html', conf=conf, requested=cfg, kernel=kernel)

# Main
if __name__ == '__main__':
    json_load()
    run()
