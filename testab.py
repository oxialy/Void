import random as rd

class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.net = [1, 2, 3]

    def __repr__(self):
        return repr(('b', self.pos))


b11 = Ball(True)
b12 = Ball(False)

a11 = {b11: False, b12: True}
b13 = [1, 2, 3]
b14 = -11

a12 = sorted(a11, key=lambda x: a11[x])
print(a11, a12)

c15 = rd.randint(range(0,5))



