class Constituent():

    def __init__(self, i, j, word, pos, left=None, right=None):
        self.i = i
        self.j = j
        self.left = left
        self.right = right
        self.word = word
        self.pos = pos

    def is_leaf(self):
        if self.left == None and self.right == None:
            return True
        else:
            return False


class TableNode():

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.cons = list()

