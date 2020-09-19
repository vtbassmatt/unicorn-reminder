from unicorn import Unicorn

class Scene:
    def __init__(self, unicorn: Unicorn):
        self.unicorn = unicorn
        self.unicorn.clear()
    
    def handle_event(self, event, current):
        pass

    async def update(self, current, elapsed):
        pass

    async def render(self):
        self.unicorn.show()

    def end(self):
        self.unicorn.off()
