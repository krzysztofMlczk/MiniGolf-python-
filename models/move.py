class Move:
    def __init__(self, pressed, released):
        self.pressed = pressed
        self.released = released

    def __str__(self):
        return "Pressed: {}, Released: {}".format(str(self.pressed), str(self.released))