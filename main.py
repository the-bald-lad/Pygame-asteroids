import pygame as p
from math import cos, sin, radians # needed for turning the player
from os import path
from random import randint
p.font.init() # inialises pygame fonts

WIDTH, HEIGHT = 750, 750 # This will change depending on which machine it was being programmed
SHIP_SIZE_X, SHIP_SIZE_Y = 50, 50
DIS = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Big Rocks in Space") # Sets the title of the window
WHITE = (255, 255, 255) # This is just so i can be lazy and don't have to type out the 3 numbers every time

# Loading images 
ASTEROID = p.transform.scale(p.image.load(path.join("assets", "asteroid.png")), (60, 60)) 
SMALL_ASTEROID =  p.transform.scale(ASTEROID, (30, 30))
SHIP = p.transform.scale(p.image.load(path.join("assets", "ship.png")), (SHIP_SIZE_X, SHIP_SIZE_Y))
LASER = p.image.load(path.join("assets", "laser (2).png"))
BG = p.transform.scale(p.image.load(path.join("assets", "background-space.jpg")), (WIDTH, HEIGHT))

# Classes for objects on the window
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = SHIP.get_width()
        self.h = SHIP.get_height()
        self.rect = SHIP.get_rect()
        self.ship_img = SHIP
        self.mask = p.mask.from_surface(self.ship_img) # for colision

        self.angle = 0
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = cos(radians(self.angle + 90))
        self.sine = sin(radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    # In order to call a specific ship if another was implemented in the future
    def draw(self, window):
        window.blit(self.rotated_surf, self.rotated_rect)

    # This will be called when the ship needs to be rotated left
    def turn_left(self):
        self.angle += 4
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = cos(radians(self.angle + 90))
        self.sine = sin(radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    # This will be called when the ship needs to be rotated right
    def turn_right(self):
        self.angle -= 4
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = cos(radians(self.angle + 90))
        self.sine = sin(radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
    
    # This moves the ship according to the position worked out by the formula above
    def move_forward(self):
        self.x += self.cosine * 7
        self.y -= self.sine * 7
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = cos(radians(self.angle + 90))
        self.sine = sin(radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
    
    # This randomises the ships position when called
    def hyper_space(self):
        self.x = randint(0, WIDTH-self.ship_img.get_width())
        self.y = randint(0, HEIGHT-self.ship_img.get_width())
    
    # Checks for border colisions
    def check(self):
        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y > WIDTH:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT
            
    # This is to gather whether the player is coliding or not with an asteroid
    def colide(self, obj):
        return collsion(self, obj)


class Asteroid:
    def __init__(self,x, y, level):
        self.x = x
        self.y = y
        self.lvl = level # needed for speed of asteroid
        self.sx = x # needed for original x value for reseta
        self.sy = y # needed for original x value for reset
        self.w = ASTEROID.get_width()
        self.h = ASTEROID.get_height()
        self.rect = ASTEROID.get_rect()
        self.vel = randint(1, self.lvl)
        
        self.ast_img = ASTEROID
        self.mask = p.mask.from_surface(self.ast_img)
        
    # This moves each asteroid depending on where is it placed on the screen when initialised
    def move(self):
        if self.sx < WIDTH/2:
            if self.sy > HEIGHT/2:
                self.x += self.vel
                self.y -= self.vel
            else:
                self.x += self.vel
                self.y += self.vel
        else:
            if self.sy > HEIGHT/2:
                self.x -= self.vel
                self.y -= self.vel
            else:
                self.x -= self.vel
                self.y += self.vel
    
    # Border checks for reseting position once reached edge of screen
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

    # This will be called when an asteroid needs to be placed upon the screen
    def draw(self, window):
        window.blit(self.ast_img, (self.x, self.y))
    
    # This is for colision detection
    def colide(self, obj):
        return collsion(self, obj)
    
    # This is so the meteors can go back to their original position when the player loses a life
    def reset(self):
        self.x = self.sx
        self.y = self.sy


class Asteroid2:
    def __init__(self,x, y, level):
        self.x = x
        self.y = y
        self.lvl = level # needed for speed
        self.w = ASTEROID.get_width()
        self.h = ASTEROID.get_height()
        self.rect = ASTEROID.get_rect()
        self.vel = level+1
        
        self.ast_img = SMALL_ASTEROID
        self.mask = p.mask.from_surface(self.ast_img)
        
    # This will check which direction to send an asteroid
    def move(self, num):
        if num % 2 == 0:
            self.x += self.vel
            self.y += self.vel
        else:
            self.x -= self.vel
            self.y -= self.vel
    
    # This checks for border colisions
    def check(self):
        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y < 0:
            self.y = HEIGHT
        if self.y > HEIGHT:
            self.y = 0

    # This will place each asteroid onto the screen when called
    def draw(self, window):
        window.blit(self.ast_img, (self.x, self.y))
        
    # This returns whether an asteroid is coliding with the player
    def colide(self, obj):
        return collsion(self, obj)
    
    # This places the asteroids onto the edge of the screen when reset
    def reset(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)


class Laser(object):
    def __init__(self, head, cosine, sine, lasers):
        self.laser_img = LASER
        self.point = head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = cosine # Passed through from player object
        self.s = sine # Passed through from player object
        self.xv = self.c * 10 # Passed through from player object
        self.yv = self.s * 10 # Passed through from player object
        self.mask = p.mask.from_surface(self.laser_img)
        
    # For moving the lasers
    def move(self):
        self.x += self.xv
        self.y -= self.yv
        
    # Will place each laser onto the screen
    def draw(self, window):
        window.blit(self.laser_img, (self.x, self.y))
        
    # Checks for colisions
    def colide(self, obj):
        return collsion(self, obj)
    
    # Checks if the laser is offscreen
    def offscreen(self):
        if self.x > WIDTH:
            return True
        if self.x < 0:
            return True
        if self.y > WIDTH:
            return True
        if self.y < 0:
            return True

# Collision Detection
def collsion(o1, o2):
    offset_x = o2.x - o1.x # Will get the distance between two x values
    offset_y = o2.y - o1.y # Will get the distance between two y values
    return o1.mask.overlap(o2.mask, (round(offset_x), round(offset_y))) != None # Will return either true or false if the values are overlapping, but only if it is not a null value

# Starting Sequence
def start_screen():
    start = True # Will start the starting loop
    FPS = 60 # Sets an FPS cap
    clock = p.time.Clock() # Initialises the clock
    
    # Fonts
    bs_font = p.font.SysFont("Opensans", 100) # Big Starting font
    s_font = p.font.SysFont("Opensans", 60) # Starting font
    c_font = p.font.SysFont("Opensans", 50) # Control font
    ss_font = p.font.SysFont("Opensans", 40) # Smaller Small font
    
    # temporary asteroids that will move across the screen
    temp_ast = Asteroid(randint(WIDTH-200, WIDTH-100), HEIGHT+10, 1)
    temp_ast1 = Asteroid(randint(200, 300), -10, 1) 
    
    # Rendered fonts
    start_label = bs_font.render("Big Rocks In Space!", 1, WHITE)
    start_label2 = s_font.render("Press the H key to start", 1, WHITE)
    controls = c_font.render("Controls:", 1, WHITE)
    controls2 = ss_font.render("W: Forward. A: Rotate Left. D: Rotate Right", 1, WHITE)
    controls3 = ss_font.render("C: Shoot. SPACE: Hyperspace", 1, WHITE)
    
    # starting loop
    while start:
        DIS.blit(BG, (0, 0)) # Places background
        clock.tick(FPS)
        
        # move temp asts
        temp_ast.move()
        temp_ast1.move()
        
        # draw temp asts to screem
        temp_ast.draw(DIS)
        temp_ast1.draw(DIS)
        
        # Temporary big asteroid for logo on starting screen
        logo_asts = p.transform.scale(p.image.load(path.join("assets", "asteroid.png")), (200, 200))
        
        DIS.blit(logo_asts, (WIDTH/2-logo_asts.get_width()+85, HEIGHT/2-logo_asts.get_height()-15))
        
        # draw everything else to the screen
        DIS.blit(start_label, (WIDTH/2 - start_label.get_width()/2, HEIGHT/2))
        DIS.blit(start_label2, (WIDTH/2 - start_label2.get_width()/2, HEIGHT/2+start_label.get_height()))
        DIS.blit(controls, (WIDTH/2 - controls.get_width()/2, HEIGHT/2+controls.get_height()+80))
        DIS.blit(controls2, (WIDTH/2 - controls2.get_width()/2, HEIGHT/2+controls2.get_height()+130))
        DIS.blit(controls3, (WIDTH/2 - controls3.get_width()/2, HEIGHT/2+controls3.get_height()+170))
        
        p.display.update()
        
        # checking for temporary asteroid border colisions
        temp_ast.check()
        temp_ast1.check()

        # event loop
        for event in p.event.get():
            # For if the player needs to quit the game
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                p.quit()
                exit()
            # Starting key
            elif event.type == p.KEYDOWN and event.key == p.K_h:   
                start = False

# ending sequence
def ending():
    global level, lost
    clock = p.time.Clock() # initialises the clock
    FPS = 60 # sets a maximum FPS
    
    # fonts
    l_font = p.font.SysFont("Opensans", 40)
    
    # logic for winning or losing
    a = "Congratulations!" if level > 5 else "Better luck next time!"
    word = "levels" if level > 1 else "level"
    
    # rendered fonts
    lost_label2 = l_font.render(f"You completed {level} {word}. {a}", 1, WHITE)
    lost_label1 = l_font.render(f"You have lost the game.", 1, WHITE)

    end = True # starts the ending loop
    b = 0 # for auto closing of the window
    
    # ending loop
    while end:
        clock.tick(FPS)
        
        # drawing objects to the screen
        DIS.blit(BG, (0, 0)) # background
        DIS.blit(lost_label1, (WIDTH/2 - lost_label1.get_width()/2, HEIGHT/2-20)) # writing
        DIS.blit(lost_label2, (WIDTH/2 - lost_label2.get_width()/2, HEIGHT/2+20)) # writing
        p.display.update()
        
        # event loop
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.K_ESCAPE: # allows for early ending
                end = False
        b += 1 # increases counter for auto close
        
        if b >= FPS*4:
            end = False

# main function
def main():
    global level, lost
    running = True # makes the game loop start
    FPS = 60 # so that the game refreshes at a constant rate
    lost = False # sets the game to start
    level, lives = 0, 4
    m_font = p.font.SysFont("opensans", 50) # sets a font object to be able to draw text to the screen
    hyper_cooldown, life_lost =  0, 0

    # Creates ship object
    player = Ship(WIDTH/2 - 30, HEIGHT/2)
    
    # lists for created objects
    player_lasers = []
    asts, small_asts = [], []

    clock = p.time.Clock() # sets a clock object so game follows a specified FPS

    #will draw the entire game when called
    def redraw_display():
        DIS.blit(BG, (0, 0))
        
        # text
        lives_label = m_font.render(f"Lives: {lives+1}", 1, WHITE)
        level_label = m_font.render(f"Level: {level}", 1, WHITE)
        hyper_label = m_font.render(f"Hyperspace cooldown: {round(hyper_cooldown/60)}", 1, WHITE)
        lost_life_label = m_font.render("You lost a life", 1, WHITE)

        # place player on screen
        player.draw(DIS)
        
        # place all asteroids on screen
        for i in asts:
            i.draw(DIS)
            
        for i in small_asts:
            i[1].draw(DIS)
            
        # place all lasers on screen    
        for b in player_lasers:
            b.draw(DIS)
        
        # check for lives to place on screen after a life loss
        if life_lost > 0:
            DIS.blit(lost_life_label, (WIDTH/2 - lost_life_label.get_width()/2, HEIGHT/2))
        
        # placing text onto the screen
        DIS.blit(lives_label, (10, 10))
        DIS.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        DIS.blit(hyper_label, (WIDTH/2 - hyper_label.get_width()/2, 10))
                
        p.display.update()

    # drawing asteroids onto the display
    def draw_asts():
        # adds meteors to the top of the window
        for i in range(level+1): 
            asts.append(Asteroid(randint(0, WIDTH), randint(-10, 0), level))

        # adds meteors to the bottom of the window
        for i in range(level+1): 
            asts.append(Asteroid(randint(0, WIDTH), randint(HEIGHT, HEIGHT+10), level))

    # main loop
    while running:
        clock.tick(FPS) # sets frames per second to specified FPS
        
        # loop for checking to see if hyper cooldown is completed
        hyper_cooldown -= 1 
        if hyper_cooldown < 0: 
            hyper_cooldown = 0
            
        # checks for a level complete
        if len(asts) == 0 and len(small_asts) == 0:
            level += 1
            draw_asts()

        # checks for game over event
        if life_lost > 0:
            life_lost -= 1

        # event loop
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.K_ESCAPE:
                p.quit()
                exit()
            if event.type == p.KEYDOWN and event.key == p.K_c and len(player_lasers) <= 5: # cannot hold down laser button to fire a huge amount
                player_lasers.append(Laser(player.head, player.cosine, player.sine, player_lasers))
        
        keys = p.key.get_pressed() # This returns a dictionary containing all keys pressed
        if keys[p.K_a]: # rotate left
            player.turn_left()
        if keys[p.K_d]: # rotate right
            player.turn_right()
        if keys[p.K_w]: # move forward
            player.move_forward()
        if keys[p.K_SPACE] and hyper_cooldown <= 0: # hyperspace
            player.hyper_space()
            player.move_forward() # This is needed to make the ship update on the screen
            hyper_cooldown = FPS*5 # This is for a 5 second cooldown

        # move each asteroid, large or small
        for i in asts:
            i.move()
        
        for i in small_asts:
            i[1].move(i[0])

        # laser move loop
        for i in player_lasers[:]:
            i.move()
            try:
                if i.x > WIDTH:
                    player_lasers.remove(i)
                if i.x < 0:
                    player_lasers.remove(i)
                if i.y > HEIGHT:
                    player_lasers.remove(i)
                if i.y < 0:
                    player_lasers.remove(i)
            except(ValueError):
                print(f"{ValueError} in laser move loop.")
                continue

        # check player positions
        player.check()
        
        # laser-asteroid colision
        for i in player_lasers[:]:
            for j in asts[:]:
                if i.colide(j):
                    for k in range(2):
                        small_asts.append([k, Asteroid2(j.x, j.y, level)])
                    asts.remove(j)
                    try:
                        player_lasers.remove(i)
                    except(ValueError):
                        print(f"{ValueError} in laser-asteroid colision")
                        continue
        
        for i in player_lasers[:]:
            for j in small_asts[:]:
                if i.colide(j[1]):
                    small_asts.remove(j)
                    try:
                        player_lasers.remove(i)
                    except(ValueError):
                        print(f"{ValueError} in laser-small asteroid loop")
                        continue
        
        # checks for asteroid colisions with the player
        for i in asts[:]:
            if i.colide(player):
                if lives < 1:
                    lost = True
                    running = False
                else:
                    player.x = WIDTH/2
                    player.y = WIDTH/2
                    player.move_forward()
                    for h in small_asts:
                        h[1].reset()
                    for i in asts:
                        i.reset()
                    player_lasers.clear()
                    lives = lives - 1
                    life_lost = FPS*2
                    redraw_display()
        
        for i in small_asts[:]:
            if i[1].colide(player):
                if lives < 1:
                    lost = True
                    running = False
                else:
                    player.x = WIDTH/2
                    player.y = WIDTH/2
                    player.move_forward()
                    for h in asts:
                        h.reset()
                    for i in small_asts:
                        i[1].reset()
                    player_lasers.clear()
                    lives = lives - 1
                    life_lost = FPS*2
                    redraw_display()
        
        # checks each asteroid position for border colision
        for i in asts:
            i.check()   
            
        for i in small_asts:
            i[1].check()      
        
        # calls the function to redraw the display
        redraw_display()


# guard statement
if __name__ == "__main__":
    start_screen() # starts the starting screen
    main() # once start sequence is finished, the main game begins
    ending() # once main game is finished, the ending is called