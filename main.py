# cheese
import pygame as p
# cheese
from math import cos, sin, radians
# cheese
from os import path
# cheese
from random import randint
# cheese
p.font.init() # inialises pygame fonts
# cheese

# cheese
WIDTH, HEIGHT = 750, 750 # This will change depending on which machine it was being programmed
# cheese
SHIP_SIZE_X, SHIP_SIZE_Y = 50, 50
# cheese
DIS = p.display.set_mode((WIDTH, HEIGHT))
# cheese
p.display.set_caption("Big Rocks in Space") # Sets the title of the window
# cheese
WHITE = (255, 255, 255) # This is just so i can be lazy and don't have to type out the 3 numbers every time
# cheese

# cheese
# Loading images 
# cheese
ASTEROID = p.transform.scale(p.image.load(path.join("assets", "asteroid.png")), (60, 60)) 
# cheese
SMALL_ASTEROID =  p.transform.scale(ASTEROID, (30, 30)) 
# cheese
SHIP = p.transform.scale(p.image.load(path.join("assets", "ship.png")), (SHIP_SIZE_X, SHIP_SIZE_Y))
# cheese
LASER = p.image.load(path.join("assets", "laser (2).png"))
# cheese
BG = p.transform.scale(p.image.load(path.join("assets", "background-space.jpg")), (WIDTH, HEIGHT))
# cheese

# cheese
# Classes for objects on the window
# cheese
class Ship:
# cheese
    def __init__(self, x, y):
# cheese
        self.x = x
# cheese
        self.y = y
# cheese
        self.w = SHIP.get_width()
# cheese
        self.h = SHIP.get_height()
# cheese
        self.rect = SHIP.get_rect()
# cheese
        self.ship_img = SHIP
# cheese
        self.mask = p.mask.from_surface(self.ship_img) # for colision
# cheese

# cheese
        self.angle = 0
# cheese
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
# cheese
        self.rotated_rect = self.rotated_surf.get_rect()
# cheese
        self.rotated_rect.center = (self.x, self.y)
# cheese
        self.cosine  = cos(radians(self.angle + 90))
# cheese
        self.sine = sin(radians(self.angle + 90))
# cheese
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
# cheese

# cheese
    def draw(self, window):
# cheese
        window.blit(self.rotated_surf, self.rotated_rect)
# cheese

# cheese
    def turn_left(self):
# cheese
        self.angle += 4
# cheese
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
# cheese
        self.rotated_rect = self.rotated_surf.get_rect()
# cheese
        self.rotated_rect.center = (self.x, self.y)
# cheese
        self.cosine  = cos(radians(self.angle + 90))
# cheese
        self.sine = sin(radians(self.angle + 90))
# cheese
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
# cheese

# cheese
    def turn_right(self):
# cheese
        self.angle -= 4
# cheese
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
# cheese
        self.rotated_rect = self.rotated_surf.get_rect()
# cheese
        self.rotated_rect.center = (self.x, self.y)
# cheese
        self.cosine  = cos(radians(self.angle + 90))
# cheese
        self.sine = sin(radians(self.angle + 90))
# cheese
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
# cheese
    
# cheese
    def move_forward(self):
# cheese
        self.x += self.cosine * 6
# cheese
        self.y -= self.sine * 6
# cheese
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
# cheese
        self.rotated_rect = self.rotated_surf.get_rect()
# cheese
        self.rotated_rect.center = (self.x, self.y)
# cheese
        self.cosine  = cos(radians(self.angle + 90))
# cheese
        self.sine = sin(radians(self.angle + 90))
# cheese
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
# cheese
    
# cheese
    def hyper_space(self):
# cheese
        self.x = randint(0, WIDTH-self.ship_img.get_width())
# cheese
        self.y = randint(0, HEIGHT-self.ship_img.get_width())
# cheese
    
# cheese
    def check(self):
# cheese
        if self.x > WIDTH:
# cheese
            self.x = 0
# cheese
        if self.x < 0:
# cheese
            self.x = WIDTH
# cheese
        if self.y > WIDTH:
# cheese
            self.y = 0
# cheese
        if self.y < 0:
# cheese
            self.y = HEIGHT
# cheese
            
# cheese
    def colide(self, obj):
# cheese
        return collsion(self, obj)
# cheese

# cheese

# cheese
class Asteroid:
# cheese
    def __init__(self,x, y, level):
# cheese
        self.x = x
# cheese
        self.y = y
# cheese
        self.lvl = level
# cheese
        self.sx = x # needed for original x value for reset
# cheese
        self.sy = y # needed for original x value for reset
# cheese
        self.w = ASTEROID.get_width()
# cheese
        self.h = ASTEROID.get_height()
# cheese
        self.rect = ASTEROID.get_rect()
# cheese
        self.vel = randint(1, self.lvl)
# cheese
        
# cheese
        self.ast_img = ASTEROID
# cheese
        self.mask = p.mask.from_surface(self.ast_img)
# cheese
        
# cheese
    def move(self):
# cheese
        if self.sx < WIDTH/2:
# cheese
            if self.sy > HEIGHT/2:
# cheese
                self.x += self.vel
# cheese
                self.y -= self.vel
# cheese
            else:
# cheese
                self.x += self.vel
# cheese
                self.y += self.vel
# cheese
        else:
# cheese
            if self.sy > HEIGHT/2:
# cheese
                self.x -= self.vel
# cheese
                self.y -= self.vel
# cheese
            else:
# cheese
                self.x -= self.vel
# cheese
                self.y += self.vel
# cheese
    
# cheese
    def check(self):
# cheese
        if self.x > WIDTH+15:
# cheese
            self.x = self.sx
# cheese
            self.y = self.sy
# cheese
        if self.x < -15:
# cheese
            self.x = self.sx
# cheese
            self.y = self.sy
# cheese
        if self.y > WIDTH+15:
# cheese
            self.x = self.sx
# cheese
            self.y = self.sy
# cheese
        if self.y < -15:
# cheese
            self.x = self.sx
# cheese
            self.y = self.sy
# cheese

# cheese
    def draw(self, window):
# cheese
        window.blit(self.ast_img, (self.x, self.y))
# cheese
        
# cheese
    def colide(self, obj):
# cheese
        return collsion(self, obj)
# cheese
    
# cheese
    def reset(self):
# cheese
        self.x = self.sx
# cheese
        self.y = self.sy
# cheese

# cheese

# cheese
class Asteroid2:
# cheese
    def __init__(self,x, y, level):
# cheese
        self.x = x
# cheese
        self.y = y
# cheese
        self.lvl = level
# cheese
        self.w = ASTEROID.get_width()
# cheese
        self.h = ASTEROID.get_height()
# cheese
        self.rect = ASTEROID.get_rect()
# cheese
        self.vel = randint(1, self.lvl)
# cheese
        
# cheese
        self.ast_img = SMALL_ASTEROID
# cheese
        self.mask = p.mask.from_surface(self.ast_img)
# cheese
        
# cheese
    def move(self, num):
# cheese
        if num % 2 == 0:
# cheese
            self.x += self.vel
# cheese
            self.y += self.vel
# cheese
        else:
# cheese
            self.x -= self.vel
# cheese
            self.y -= self.vel
# cheese
    
# cheese
    def check(self):
# cheese
        if self.x > WIDTH:
# cheese
            self.x = 0
# cheese
        if self.x < 0:
# cheese
            self.x = WIDTH
# cheese
        if self.y < 0:
# cheese
            self.y = HEIGHT
# cheese
        if self.y > HEIGHT:
# cheese
            self.y = 0
# cheese

# cheese
    def draw(self, window):
# cheese
        window.blit(self.ast_img, (self.x, self.y))
# cheese
        
# cheese
    def colide(self, obj):
# cheese
        return collsion(self, obj)
# cheese
    
# cheese
    def reset(self):
# cheese
        self.x = randint(0, WIDTH)
# cheese
        self.y = randint(0, HEIGHT)
# cheese

# cheese

# cheese
class Laser(object):
# cheese
    def __init__(self, head, cosine, sine, lasers):
# cheese
        self.laser_img = LASER
# cheese
        self.point = head
# cheese
        self.x, self.y = self.point
# cheese
        self.w = 4
# cheese
        self.h = 4
# cheese
        self.c = cosine
# cheese
        self.s = sine
# cheese
        self.xv = self.c * 10
# cheese
        self.yv = self.s * 10
# cheese
        self.lasers = lasers
# cheese
        self.mask = p.mask.from_surface(self.laser_img)
# cheese
        
# cheese
    def move(self):
# cheese
        self.x += self.xv
# cheese
        self.y -= self.yv
# cheese
        
# cheese
    def draw(self, window):
# cheese
        window.blit(self.laser_img, (self.x, self.y))
# cheese
        
# cheese
    def colide(self, obj):
# cheese
        return collsion(self, obj)
# cheese
    
# cheese
    def offscreen(self):
# cheese
        if self.x > WIDTH:
# cheese
            return True
# cheese
        if self.x < 0:
# cheese
            return True
# cheese
        if self.y > WIDTH:
# cheese
            return True
# cheese
        if self.y < 0:
# cheese
            return True
# cheese

# cheese
def collsion(o1, o2):
# cheese
    offset_x = o2.x - o1.x
# cheese
    offset_y = o2.y - o1.y
# cheese
    return o1.mask.overlap(o2.mask, (offset_x, offset_y)) != None
# cheese

# cheese

# cheese
def start_screen():
# cheese
    start = True
# cheese
    FPS = 60
# cheese
    clock = p.time.Clock()
# cheese
    
# cheese
    bs_font = p.font.SysFont("Opensans", 100)
# cheese
    s_font = p.font.SysFont("Opensans", 60)
# cheese
    
# cheese
    temp_ast = Asteroid(randint(WIDTH-200, WIDTH-100), HEIGHT+10, 1)
# cheese
    temp_ast1 = Asteroid(randint(200, 300), -10, 1)
# cheese
    
# cheese
    start_label = bs_font.render("Big Rocks In Space!", 1, WHITE)
# cheese
    start_label2 = s_font.render("Press the H key to start", 1, WHITE)
# cheese
    
# cheese
    # starting loop
# cheese
    while start:
# cheese
        DIS.blit(BG, (0, 0))
# cheese
        clock.tick(FPS)
# cheese
        temp_ast.move()
# cheese
        temp_ast1.move()
# cheese
        
# cheese
        temp_ast.draw(DIS)
# cheese
        temp_ast1.draw(DIS)
# cheese
        
# cheese
        a = p.transform.scale(p.image.load(path.join("assets", "asteroid.png")), (200, 200))
# cheese
        
# cheese
        DIS.blit(a, (WIDTH/2-a.get_width()+85, HEIGHT/2-a.get_height()-15))
# cheese
        
# cheese
        DIS.blit(start_label, (WIDTH/2 - start_label.get_width()/2, HEIGHT/2))
# cheese
        DIS.blit(start_label2, (WIDTH/2 - start_label2.get_width()/2, HEIGHT/2+start_label.get_height()))
# cheese
        
# cheese
        p.display.update()
# cheese
        
# cheese
        temp_ast.check()
# cheese
        temp_ast1.check()
# cheese

# cheese
        # event loop
# cheese
        for event in p.event.get():
# cheese
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
# cheese
                p.quit()
# cheese
                exit()
# cheese
            elif event.type == p.KEYDOWN and event.key == p.K_h:   
# cheese
                start = False
# cheese

# cheese

# cheese
def ending():
# cheese
    global level, lost
# cheese
    clock = p.time.Clock()
# cheese
    FPS = 60
# cheese
    l_font = p.font.SysFont("Opensans", 40)
# cheese
    a = "Congratulations!" if level > 5 else "Better luck next time!" 
# cheese
    word = "levels" if level > 1 else "level"
# cheese
    lost_label2 = l_font.render(f"You completed {level} {word}. {a}", 1, WHITE)
# cheese
    lost_label1 = l_font.render(f"You have lost the game.", 1, WHITE)
# cheese

# cheese
    end = True
# cheese
    b = 0
# cheese
    
# cheese
    # ending loop
# cheese
    while end:
# cheese
        clock.tick(FPS)
# cheese
        DIS.blit(BG, (0, 0))
# cheese
        DIS.blit(lost_label1, (WIDTH/2 - lost_label1.get_width()/2, HEIGHT/2-20))
# cheese
        DIS.blit(lost_label2, (WIDTH/2 - lost_label2.get_width()/2, HEIGHT/2+20))
# cheese
        p.display.update()
# cheese
        
# cheese
        # event loop
# cheese
        for event in p.event.get():
# cheese
            if event.type == p.QUIT or event.type == p.K_ESCAPE:
# cheese
                end = False
# cheese
        b += 1
# cheese
        
# cheese
        if b >= FPS*4:
# cheese
            end = False
# cheese

# cheese
# main function
# cheese
def main():
# cheese
    global level, lost
# cheese
    running = True # makes the game loop start
# cheese
    FPS = 60 # so that the game refreshes at a constant rate
# cheese
    lost = False
# cheese
    level, lives = 0, 4
# cheese
    m_font = p.font.SysFont("opensans", 50) # sets a font object to be able to draw text to the screen
# cheese
    hyper_cooldown, life_lost =  0, 0
# cheese

# cheese
    player = Ship(WIDTH/2 - 30, HEIGHT/2) # places ship in centre of screen
# cheese
    player_lasers = []
# cheese
    asts, small_asts = [], []
# cheese

# cheese
    clock = p.time.Clock() # sets a clock object so game follows a specified FPS
# cheese

# cheese
    #function to redraw the window
# cheese
    def redraw_display():
# cheese
        DIS.blit(BG, (0, 0))
# cheese
        
# cheese
        # text
# cheese
        lives_label = m_font.render(f"Lives: {lives+1}", 1, WHITE)
# cheese
        level_label = m_font.render(f"Level: {level}", 1, WHITE)
# cheese
        hyper_label = m_font.render(f"Hyperspace cooldown: {round(hyper_cooldown/60)}", 1, WHITE)
# cheese
        lost_life_label = m_font.render("You lost a life", 1, WHITE)
# cheese

# cheese
        # place player on screen
# cheese
        player.draw(DIS)
# cheese
        
# cheese
        # place all asteroids on screen
# cheese
        for i in asts:
# cheese
            i.draw(DIS)
# cheese
            
# cheese
        for i in small_asts:
# cheese
            i[1].draw(DIS)
# cheese
            
# cheese
        # place all lasers on screen    
# cheese
        for b in player_lasers:
# cheese
            b.draw(DIS)
# cheese
            
# cheese
        if life_lost > 0:
# cheese
            DIS.blit(lost_life_label, (WIDTH/2 - lost_life_label.get_width()/2, HEIGHT/2))
# cheese
            
# cheese
        DIS.blit(lives_label, (10, 10))
# cheese
        DIS.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
# cheese
        DIS.blit(hyper_label, (WIDTH/2 - hyper_label.get_width()/2, 10))
# cheese
                
# cheese
        p.display.update()
# cheese

# cheese
    def draw_asts():
# cheese
        # adds meteors to the top of the window
# cheese
        for i in range(level+1): 
# cheese
            asts.append(Asteroid(randint(0, WIDTH), randint(-10, 0), level))
# cheese

# cheese
        # adds meteors to the bottom of the window
# cheese
        for i in range(level+1): 
# cheese
            asts.append(Asteroid(randint(0, WIDTH), randint(HEIGHT, HEIGHT+10), level))
# cheese

# cheese
    # main loop
# cheese
    while running:
# cheese
        clock.tick(FPS) # sets frames per second to specified FPS
# cheese
        
# cheese
        # loop for checking to see if hyper cooldown is completed
# cheese
        hyper_cooldown -= 1 
# cheese
        if hyper_cooldown < 0: 
# cheese
            hyper_cooldown = 0
# cheese
            
# cheese
        # checks for a level complete
# cheese
        if len(asts) == 0 and len(small_asts) == 0:
# cheese
            level += 1
# cheese
            draw_asts()
# cheese

# cheese
        # checks for game over event
# cheese
        if life_lost > 0:
# cheese
            life_lost -= 1
# cheese

# cheese
        # event loop
# cheese
        for event in p.event.get():
# cheese
            if event.type == p.QUIT or event.type == p.K_ESCAPE:
# cheese
                p.quit()
# cheese
                exit()
# cheese
            if event.type == p.KEYDOWN and event.key == p.K_c and len(player_lasers) <= 4: # cannot hold down laser button to fire a huge amount
# cheese
                player_lasers.append(Laser(player.head, player.cosine, player.sine, player_lasers))
# cheese
        
# cheese
        keys = p.key.get_pressed() # This returns a dictionary containing all keys pressed
# cheese
        if keys[p.K_a]: # rotate left
# cheese
            player.turn_left()
# cheese
        if keys[p.K_d]: # rotate right
# cheese
            player.turn_right()
# cheese
        if keys[p.K_w]: # move forward
# cheese
            player.move_forward()
# cheese
        if keys[p.K_SPACE] and hyper_cooldown <= 0: # hyperspace
# cheese
            player.hyper_space()
# cheese
            player.move_forward() # This is needed to make the ship update on the screen
# cheese
            hyper_cooldown = FPS*5 # This is for a 5 second cooldown
# cheese

# cheese
        # move each asteroid
# cheese
        for i in asts:
# cheese
            i.move()
# cheese
            
# cheese
        for i in small_asts:
# cheese
            i[1].move(i[0])
# cheese

# cheese
        # laser move loop
# cheese
        for i in player_lasers[:]:
# cheese
            i.move()
# cheese
            try:
# cheese
                if i.x > WIDTH:
# cheese
                    player_lasers.remove(i)
# cheese
                if i.x < 0:
# cheese
                    player_lasers.remove(i)
# cheese
                if i.y > HEIGHT:
# cheese
                    player_lasers.remove(i)
# cheese
                if i.y < 0:
# cheese
                    player_lasers.remove(i)
# cheese
            except(ValueError):
# cheese
                pass
# cheese

# cheese
        # check player positions
# cheese
        player.check()
# cheese
        
# cheese
        # laser-asteroid colision
# cheese
        for i in player_lasers[:]:
# cheese
            for j in asts[:]:
# cheese
                if i.colide(j):
# cheese
                    for k in range(2):
# cheese
                        small_asts.append([k, Asteroid2(j.x, j.y, level)])
# cheese
                    asts.remove(j)
# cheese
                    try:
# cheese
                        player_lasers.remove(i)
# cheese
                    except(ValueError):
# cheese
                        continue
# cheese
        
# cheese
        for i in player_lasers[:]:
# cheese
            for j in small_asts[:]:
# cheese
                if i.colide(j[1]):
# cheese
                    small_asts.remove(j)
# cheese
                    try:
# cheese
                        player_lasers.remove(i)
# cheese
                    except(ValueError):
# cheese
                        continue
# cheese
        
# cheese
        # checks for asteroid colisions with the player
# cheese
        for i in asts[:]:
# cheese
            if i.colide(player):
# cheese
                if lives < 1:
# cheese
                    lost = True
# cheese
                    running = False
# cheese
                else:
# cheese
                    player.x = WIDTH/2
# cheese
                    player.y = WIDTH/2
# cheese
                    player.move_forward()
# cheese
                    for h in small_asts:
# cheese
                        h[1].reset()
# cheese
                    for i in asts:
# cheese
                        i.reset()
# cheese
                    player_lasers.clear()
# cheese
                    lives = lives - 1
# cheese
                    life_lost = FPS*2
# cheese
                    redraw_display()
# cheese
        
# cheese
        for i in small_asts[:]:
# cheese
            if i[1].colide(player):
# cheese
                if lives < 1:
# cheese
                    lost = True
# cheese
                    running = False
# cheese
                else:
# cheese
                    player.x = WIDTH/2
# cheese
                    player.y = WIDTH/2
# cheese
                    player.move_forward()
# cheese
                    for h in asts:
# cheese
                        h.reset()
# cheese
                    for i in small_asts:
# cheese
                        i[1].reset()
# cheese
                    player_lasers.clear()
# cheese
                    lives = lives - 1
# cheese
                    life_lost = FPS*2
# cheese
                    redraw_display()
# cheese
        
# cheese
        # checks each asteroid position
# cheese
        for i in asts:
# cheese
            i.check()   
# cheese
            
# cheese
        for i in small_asts:
# cheese
            i[1].check()      
# cheese
        
# cheese
        # calls the function to redraw the display
# cheese
        redraw_display()
# cheese

# cheese

# cheese
if __name__ == "__main__":
# cheese
    start_screen()
# cheese
    main()
# cheese
    ending()