from flask import Flask, render_template, url_for, request, flash, redirect, session, abort, g
from flask_debugtoolbar import DebugToolbarExtension
import sqlite3
import os

DATABASE = '/tmp/flask.db'
DEBUG = True
SECRET_KEY = '1818'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

app.config['SECRET_KEY'] = '1818'

app.config.update(DATABASE=os.path.join(app.root_path, 'flask.db'))

# toolbar = DebugToolbarExtension(app)


menu = [{"name": "Приложение", "url": "first-app"},
        {"name": "Регистрация", "url": "contact"},
        {"name": "Авторизация", "url": "login"},
        {"name": "Обратная связь", "url": "contact"},
        ]


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    return render_template('index.html', menu=[])


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def main_page():  # put application's code here
    return render_template('index.html', title="Про Flask", menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title="О сайте", menu=menu)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Message sended', category='success')
        else:
            flash('Error', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'Profile user: {username}'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' and request.form['psw'] == 'admin':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)
