

class Jeton:

    def __init__(self, number=0, color="blanc"):
        self.number = number # nombre
        self.color = color # couleur
        self.image = 'images/'+ str(number) +'/'+ str(number) + color +'.png' # chemin de l'image associer dans le dossier static
