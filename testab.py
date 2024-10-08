
class Ball:
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return repr(('b', self.pos))


b11 = Ball(True)
b12 = Ball(False)

a11 = {}

a12 = sorted(a11, key=lambda x: a11[x])
print(a11, a12)

for e in None:
    print(1)



