class Scene:
    def __init__(self, unicorn):
        self.unicorn = unicorn
        self.unicorn.clear()

    def update(self, current, elapsed):
        pass

    def render(self):
        self.unicorn.show()

    def end(self):
        self.unicorn.off()
