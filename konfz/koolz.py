# -*- coding: utf-8 -*-

from flask import (
    Flask,
    render_template,
    request,
)

# Flask init
app = Flask(__name__)

def run():
    app.config.update(dict(SECRET_KEY='oui'))
    app.run(host='0.0.0.0', debug=True)

def lookup(hint):
    pass
    
# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.has('hint'):
        hits = lookup(request.form['hint'])
    return render_template('home.html')

# Main
if __name__ == '__main__':
    run()
