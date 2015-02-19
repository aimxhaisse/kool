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
    server.socket_port = 20007
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

def run_debug():
    json_load()
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


# Misc
def sort_kernel(ka, kb):
    reg = '^linux\-([0-9])\.([0-9]+)(?:\.([0-9]+))?$'
    va = re.match(reg, ka)
    vb = re.match(reg, kb)
    major_a = int(va.group(1))
    major_b = int(vb.group(1))
    if major_a > major_b:
        return 1
    if major_b > major_a:
        return -1
    minor_a = int(va.group(2))
    minor_b = int(vb.group(2))
    if minor_a > minor_b:
        return 1
    if minor_a < minor_b:
        return -1
    if len(va.groups()) == 3 and len(vb.groups()) == 3:
        subversion_a = int(va.group(3))
        subversion_b = int(vb.group(3))
        if subversion_a > subversion_b:
            return 1
        if subversion_a < subversion_b:
            return -1
    return 0


# Routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/k/<kernel>', methods=['GET', 'POST'])
def home(kernel=None):
    if not kernel or kernel not in jsons:
        kernel = 'linux-3.19'
    hits = None
    hint = None
    if request.method == 'POST' and 'hint' in request.form:
        hint = request.form['hint']
        if len(hint) >= 3:
            hits = lookup(kernel, hint.upper())
            if len(hits) == 1:
                return redirect(url_for('conf', kernel=kernel, cfg=hits[0]),
                                302)
    return render_template('home.html', kernel=kernel, hint=hint, hits=hits)

@app.route('/i/<kernel>')
def index(kernel):
    configs = get_configs(kernel)
    return render_template('index.html', kernel=kernel, configs=configs)

@app.route('/switch')
def switch():
    return render_template('switch.html', kernels=sorted(jsons.keys(),
                                                         sort_kernel))

@app.route('/c/<kernel>/<cfg>')
def conf(kernel, cfg):
    conf = None
    also_in = None
    if kernel in jsons:
        if cfg in jsons[kernel]:
            conf = jsons[kernel][cfg]
            also_in = get_also_in(cfg, kernel)
    return render_template('conf.html', conf=conf,
                           requested=cfg, kernel=kernel,
                           also_in=sorted(also_in, sort_kernel))

# Main
if __name__ == '__main__':
    run()
