import os

from flask import Flask, render_template

from App.src.Game import Game

app = Flask(__name__)
game = Game()

@app.route('/')
@app.route('/Acceuil')
def acceuil():
    return render_template('Acceuil.html', game=game)

@app.route('/index')
def index():
    return render_template('index.html', game=game)


app.run()