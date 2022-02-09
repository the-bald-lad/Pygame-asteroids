import pygame as p, os, math, time
from random import randint
p.font.init() # inialises pygame fonts

WIDTH, HEIGHT = 750, 750 # This will change depending on which machine it was being programmed
SHIP_SIZE_X, SHIP_SIZE_Y = 50, 50
DIS = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Big Rocks in Space") # Sets the title of the window
WHITE = (255, 255, 255) # This is just so i can be lazy and don't have to type out the 3 numbers every time

# Loading images 
ASTEROID = p.transform.scale(p.image.load(os.path.join("assets", "asteroid.png")), (60, 60)) 
SHIP = p.transform.scale(p.image.load(os.path.join("assets", "ship.png")), (SHIP_SIZE_X, SHIP_SIZE_Y))
LASER = p.image.load(os.path.join("assets", "laser (2).png"))
BG = p.transform.scale(p.image.load(os.path.join("assets", "background-space.jpg")), (WIDTH, HEIGHT))

# Classes for objects on the window
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.w = SHIP.get_width()
        self.h = SHIP.get_height()
        self.rect = SHIP.get_rect()
        self.ship_img = SHIP
        self.mask = p.mask.from_surface(self.ship_img)
        self.health = health

        self.angle = 0
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, window):
        window.blit(self.rotated_surf, self.rotated_rect)

    def turn_left(self):
        self.angle += 5
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turn_right(self):
        self.angle -= 5
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
        self.cosine  = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
    
    def move_forward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotated_surf = p.transform.rotate(self.ship_img, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect()
        self.rotated_rect.center = (self.x, self.y)
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
            
    def colide(self, obj):
        return collsion(self, obj)


class Asteroid:
    def __init__(self,x, y, level, health=100):
        self.x = x
        self.y = y
        self.lvl = level
        self.sx = x # needed for original x value for reset
        self.sy = y # needed for original x value for reset
        self.w = ASTEROID.get_width()
        self.h = ASTEROID.get_height()
        self.rect = ASTEROID.get_rect()
        self.vel = randint(1, self.lvl)
        
        self.health = health
        self.ast_img = ASTEROID
        self.mask = p.mask.from_surface(self.ast_img)
        
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
        
    def colide(self, obj):
        return collsion(self, obj)
    
    def reset(self):
        self.x = self.sx
        self.y = self.sy

class Laser(object):
    def __init__(self, head, cosine, sine, lasers):
        self.laser_img = LASER
        self.point = head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = cosine
        self.s = sine
        self.xv = self.c * 10
        self.yv = self.s * 10
        self.lasers = lasers
        self.mask = p.mask.from_surface(self.laser_img)
        
    def move(self):
        self.x += self.xv
        self.y -= self.yv
        
    def draw(self, window):
        window.blit(self.laser_img, (self.x, self.y))
        
    def colide(self, obj):
        return collsion(self, obj)
    
    def offscreen(self):
        if self.x > WIDTH:
            return True
        if self.x < 0:
            return True
        if self.y > WIDTH:
            return True
        if self.y < 0:
            return True

def collsion(o1, o2):
    offset_x = o2.x - o1.x
    offset_y = o2.y - o1.y
    return o1.mask.overlap(o2.mask, (offset_x, offset_y)) != None

# main function
def main():
    running = True # makes the game loop start
    lost = False
    FPS = 60
    level, lives = 0, 4
    m_font = p.font.SysFont("opensans", 50)
    l_font = p.font.SysFont("Opensans", 40)
    hyper_cooldown, life_lost =  0, 0

    player = Ship(WIDTH/2 - 30, HEIGHT/2)
    player_lasers = []
    asts = []

    clock = p.time.Clock()

    #function to redraw the window
    def redraw_display():
        DIS.blit(BG, (0, 0))
        
        # text
        lives_label = m_font.render(f"Lives: {lives+1}", 1, WHITE)
        level_label = m_font.render(f"Level: {level}", 1, WHITE)
        hyper_label = m_font.render(f"Hyperspace cooldown: {round(hyper_cooldown/60)}", 1, WHITE)
        lost_life_label = m_font.render("You lost a life", 1, WHITE)

        player.draw(DIS)
        
        for i in asts:
            i.draw(DIS)
            
        for b in player_lasers:
            b.draw(DIS)
            
        if life_lost > 0:
            DIS.blit(lost_life_label, (WIDTH/2 - lost_life_label.get_width()/2, HEIGHT/2))
            
        DIS.blit(lives_label, (10, 10))
        DIS.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        DIS.blit(hyper_label, (WIDTH/2 - hyper_label.get_width()/2, 10))
                
        p.display.update()

    def draw_asts():
        # adds meteors to the top of the window
        for i in range(level+1): 
            asts.append(Asteroid(randint(0, WIDTH), randint(-10, 0), level))

        # adds meteors to the bottom of the window
        for i in range(level+1): 
            asts.append(Asteroid(randint(0, WIDTH), randint(HEIGHT, HEIGHT+10), level))

    # main loop
    while running:
        # end game sequence
        if lost: 
            a = "Congratulations!" if level > 5 else "Better luck next time!" 
            word = "levels" if level > 1 else "level"
            lost_label2 = l_font.render(f"You completed {level} {word}. {a}", 1, WHITE)
            lost_label3 = l_font.render("Press the spacebar to exit", 1, WHITE)
            lost_label1 = l_font.render(f"You have lost the game.", 1, WHITE)

            DIS.blit(BG, (0, 0))
            DIS.blit(lost_label1, (WIDTH/2 - lost_label1.get_width()/2, HEIGHT/2-20))
            DIS.blit(lost_label2, (WIDTH/2 - lost_label2.get_width()/2, HEIGHT/2+20))
            DIS.blit(lost_label3, (WIDTH/2 - lost_label3.get_width()/2, HEIGHT/2+40))
            p.display.update()

            while True:
                keys = p.key.get_pressed()
                if keys[p.K_SPACE]:
                    break

            running = False
        
        clock.tick(FPS)
        hyper_cooldown -= 1 
        if hyper_cooldown < 0: 
            hyper_cooldown = 0
        
        if len(asts) == 0:
            level += 1
            draw_asts()

        if life_lost > 0:
            life_lost -= 1

        # event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN and event.key == p.K_c and len(player_lasers) <= 4:
                player_lasers.append(Laser(player.head, player.cosine, player.sine, player_lasers))
        
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
                pass


        # check player positions
        player.check()
        
        # laser-asteroid colision
        for i in player_lasers[:]:
            for j in asts[:]:
                if i.colide(j):
                    asts.remove(j)
                    try:
                        player_lasers.remove(i)
                    except(ValueError):
                        continue
        
        for i in asts[:]:
            if i.colide(player):
                if lives < 1:
                    lost = True
                else:
                    player.x = WIDTH/2
                    player.y = WIDTH/2
                    player.move_forward()
                    for i in asts:
                        i.reset()
                    player_lasers.clear()
                    lives = lives - 1
                    life_lost = FPS*2
                    redraw_display()
        
        # checks each asteroid position
        for i in asts:
            i.check()        
        
        # calls the function to redraw the display
        redraw_display()


if __name__ == "__main__":
    main()