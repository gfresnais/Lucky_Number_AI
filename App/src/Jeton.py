

class Jeton:

    def __init__(self, number=0, color="blanc"):
        self.number = number
        self.color = color
        self.image = 'App/res/images/'+ str(number) +'/'+ str(number) + color +'.png'
