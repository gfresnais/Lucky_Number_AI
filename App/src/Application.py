import os

from flask import Flask, render_template

from App.src.Game import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def acceuil():
    jeton1 = game.pioche.piocheJeton()
    jeton2 = game.pioche.piocheJeton()
    jeton3 = game.pioche.piocheJeton()
    jeton4 = game.pioche.piocheJeton()
    return render_template('Acceuil.html')



app.run()