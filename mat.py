from pygame import image
class Mat:
    
    def __init__(self, name, screen, locx, locy):
        
        # Default state
        self.state = 0
        
        # Identifying string
        self.name = name
        
        # Screen to draw on
        self.screen = screen
        
        # Location on screen
        self.locx = locx
        self.locy = locy
        self.location = (self.locx, self.locy)

        # Images
        self.grey = image.load("/home/pi/PressureMat/images/grey.png")
        self.green = image.load("/home/pi/PressureMat/images/green.png")
        self.image = self.grey


    def draw(self):
        # Default grey state
        if self.state == 0:
            self.screen.blit(self.grey, self.location)

        # Mat was pressed, revert to grey state
        if self.state == 1:
            self.screen.blit(self.grey, self.location)

        # Algorithm has selected an unused part of the board
        # proceed to change it to green
        if self.state == 2:
            self.screen.blit(self.green, self.location)

