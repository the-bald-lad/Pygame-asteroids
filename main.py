import pygame as p, os, math 
from random import randint
p.font.init() # inialises pygame fonts

WIDTH, HEIGHT = 750, 750 # This will change depending on where it was being programmed
SHIP_SIZE_X, SHIP_SIZE_Y = 50, 50
DIS = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Big Rocks in Space") # Sets the title of the window
black = (0, 0, 0) # These are just so i can be lazy and don't have to type out the 3 numbers every time
white = (255, 255, 255)

# loading images 
ASTEROID = p.transform.scale(p.image.load(os.path.join("assets", "asteroid.png")), (60, 60)) 
SHIP = p.transform.scale(p.image.load(os.path.join("assets", "ship.png")), (SHIP_SIZE_X, SHIP_SIZE_Y))

BG = p.transform.scale(p.image.load(os.path.join("assets", "background-space.jpg")), (WIDTH, HEIGHT))

# classes for objects on the window
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.w = SHIP.get_width()
        self.h = SHIP.get_height()

        self.move = 0
        self.health = health
        self.ship_img = SHIP

        self.angle = 0
        self.rotatedSurf = p.transform.rotate(self.ship_img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    
    def draw(self, window):
        window.blit(self.rotatedSurf, self.rotatedRect)


    def turn_left(self):
        self.angle += 5
        self.rotatedSurf = p.transform.rotate(self.ship_img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)


    def turn_right(self):
        self.angle -= 5
        self.rotatedSurf = p.transform.rotate(self.ship_img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
    

    def move_forward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = p.transform.rotate(self.ship_img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
    
    def hyper_space(self):
        self.x = randint(0, WIDTH-self.ship_img.get_width())
        self.x = randint(0, HEIGHT-self.ship_img.get_width())
    
    def check(self):
        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y > WIDTH:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT


class Asteroid:
    def __init__(self,x, y, health=100):
        self.x = x
        self.y = y
        self.sx = x # needed for original x value for reset
        self.sy = y # needed for original x value for reset
        self.w = ASTEROID.get_width()
        self.h = ASTEROID.get_height()
        
        self.health = health
        self.ast_img = ASTEROID
    
    def move(self):
        if self.sx < WIDTH/2:
            if self.sy > HEIGHT/2:
                self.x += 1
                self.y -= 1
            else:
                self.x += 1
                self.y += 1
        else:
            if self.sy > HEIGHT/2:
                self.x -= 1
                self.y -=1
            else:
                self.x -= 1
                self.y += 1
    
    def check(self):
        if self.x > WIDTH+15:
            self.x = self.sx
            self.y = self.sy
        if self.x < -15:
            self.x = self.sx
            self.y = self.sy
        if self.y > WIDTH+15:
            self.x = self.sx
            self.y = self.sy
        if self.y < -15:
            self.x = self.sx
            self.y = self.sy

    def draw(self, window):
        window.blit(self.ast_img, (self.x, self.y))

# main function
def main():
    running = True # makes the game loop start
    FPS = 60
    level, lives = 1, 5
    m_font = p.font.SysFont("opensans", 50)
    hyper_cooldown = 0

    player = Ship(WIDTH/2 - 30, HEIGHT/2)
    asts = []
    
    # adds meteors to the top of the window
    for i in range(3): 
        asts.append(Asteroid(randint(0, WIDTH), randint(-10, 0)))

    # adds meteors to the bottom of the window
    for i in range(3): 
        asts.append(Asteroid(randint(0, WIDTH), randint(HEIGHT, HEIGHT+10)))

    clock = p.time.Clock()

    #function to redraw the window
    def redraw_display():
        DIS.blit(BG, (0, 0))
        
        # text
        lives_label = m_font.render(f"Lives: {lives}", 1, white)
        level_label = m_font.render(f"Level: {level}", 1, white)
        hyper_label = m_font.render(f"Hyperspace cooldown: {round(hyper_cooldown/60)}", 1, white)

        player.draw(DIS)
        
        for i in asts:
            i.draw(DIS)
            
        DIS.blit(lives_label, (10, 10))
        DIS.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        DIS.blit(hyper_label, (WIDTH/2 - hyper_label.get_width()/2, 10))

        p.display.update()

    # main loop
    while running:
        clock.tick(FPS)
        hyper_cooldown -= 1 
        if hyper_cooldown < 0: hyper_cooldown = 0

        # event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        
        # This returns a dictionary with all keypresses
        keys = p.key.get_pressed()
        if keys[p.K_a]: # left
            player.turn_left()
        if keys[p.K_d]: # right
            player.turn_right()
        if keys[p.K_w]: # up
            player.move_forward()
        if keys[p.K_SPACE] and hyper_cooldown <= 0: # hyperspace
            player.hyper_space()
            player.move_forward() # This is needed to make the ship update on the screen
            hyper_cooldown = FPS*5 # This is for a 5 second cooldown, since FPS is 60

        # move each asteroid
        for i in asts:
            i.move()

        # check player positions
        player.check()
        
        # checks each asteroid position
        for i in asts:
            i.check()
        
        # calls the function to redraw the display
        redraw_display()

if __name__ == "__main__":
    main()