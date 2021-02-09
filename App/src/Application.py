import os

from flask import Flask, render_template

from App.src.Game import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def acceuil():
    for i in range(4):
        game.joueur.add_jeton(game.pioche.piocheJeton())
    return render_template('Acceuil.html', game)

@app.route('/index')
def index():
    return render_template('index.html')


app.run()