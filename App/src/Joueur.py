from App.src.Jeton import Jeton


class Joueur:

    def __init__(self, first_jeton, second_jeton, third_jeton, fourth_jeton):
        self.jeton = Jeton()
        self.list_jeton = []
        self.add_jeton(first_jeton)
        self.add_jeton(second_jeton)
        self.add_jeton(third_jeton)
        self.add_jeton(fourth_jeton)

    def add_jeton(self, jeton):
        self.list_jeton.append(jeton)
        return jeton

    def remove_jeton(self, jeton):
        index = self.list_jeton.index(jeton)
        return self.list_jeton.pop(index)

    def new_jeton(self, jeton):
        self.jeton = jeton
        return jeton

    def get_jeton(self):
        return self.jeton

    def get_list(self):
        return self.list_jeton