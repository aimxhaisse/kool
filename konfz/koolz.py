# -*- coding: utf-8 -*-

import os
import json
import re
import cherrypy

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)


# Flask
app = Flask(__name__)

def run():
    json_load()
    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 5000
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

def debug():
    json_load()
    app.run(host='0.0.0.0', debug=False)

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

def get_also_in(config, kernel):
    res = []
    for name, configs in jsons.iteritems():
        if name != kernel:
            if config in configs:
                res.append(name)
    return res

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
            if len(hits) == 1:
                return redirect(url_for('conf', kernel=kernel, cfg=hits[0]), 302)
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
    also_in = None
    if kernel in jsons:
        if cfg in jsons[kernel]:
            conf = jsons[kernel][cfg]
            also_in = get_also_in(cfg, kernel)
    return render_template('conf.html', conf=conf, requested=cfg, kernel=kernel, also_in=also_in)

# Main
if __name__ == '__main__':
    run()
