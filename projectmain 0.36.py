import csv
import pygame
import pygame.gfxdraw
import time
import random
import os
import math

#initialises pygame mixer for audio if there is an audio device detected
try:
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
except:
    pass

#gets screen resolution
info = pygame.display.Info()

#sets dimensions of game screen
sh = 600
sw = 1008

#sets dimensions of game window
sh1 = (info.current_h)
sw1 = (info.current_w)

#sets start positon of game screen so it is centered within the window
gamescreenx = (sw1/2)-(sw/2)
gamescreeny = (sh1/2)-(sh/2)

#gets the file directory of the program
path = os.path.realpath('')
path = os.path.join(path, r"data")
#divides the gamescreeen into a 16*16 grid and sets the scale factor of all objects so theyre in proportion
bw = sw /16
sf = bw/100
bh = sh/8
tsf = sf*1.6

#creates the window in which the game will play on
screen = pygame.display.set_mode(((sw1),(sh1)), pygame.FULLSCREEN | pygame.SRCALPHA)

#loads and scales button images to be used later
unpressed_button = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\button.png")),(250,75))
pressed_button = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\buttonpressed.png")),(250,75))
unpressed_square_button = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\squarebutton.png")),(75,75))
pressed_square_button = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\squarebuttonpressed.png")),(75,75))

#creates surface in which the scoreboard will occupy 
scoreboard1 = pygame.Surface((116,36))  
scoreboard1 = pygame.transform.scale(scoreboard1,(60,15))

#loads and scales the background of the game to the dimensions of the window
background = pygame.image.load(os.path.join(path, r"images\background.png"))
background = pygame.transform.scale(background,(sw1,sh1))

#sets the caption of the window
pygame.display.set_caption('Tanks!') 

#sets global variables for each colour of tank in RGB values (0-255)
blue = ((0, 162, 232), (63, 72, 204))
brown = ((190, 137, 58), (143, 103, 44))
grey = ((93, 93, 93), (70, 70, 70 ))
red = ((248, 58, 58), (206, 9, 9))
white = ((210, 210, 210), (166, 166, 166))
black = ((10, 10, 10), (30, 30, 30))
yellow = ((250, 250, 54), (153, 153, 26))
green = ((43, 138, 40), (30, 94, 28))
purple =((107, 0, 215), (55, 0, 111))
turquoise = ((4, 166, 157), (2, 91, 87))

#creates a list of all colour tuples
colours = [blue, brown, grey, turquoise, yellow, red, green, purple, white, black]

#scoreboard is a small box in the corner of the screen that will display how many bullets are left and the state of power ups that are available or in use
class Scoreboards:
    
    def __init__(self):
        
        #loads scoreboard images into a list
        self.images = []
        for i in range(0,6):
            self.images.append(pygame.image.load(os.path.join(path, r"images\scoreboards\scoreboard" +str(i)+".png")))
        
        #loads images for each power up
        self.speedicon = pygame.image.load(os.path.join(path, r"images\PowerUpicons\speedicon.png"))
        self.bangbulleticon = pygame.image.load(os.path.join(path, r"images\PowerUpicons\bangbulleticon.png"))
        self.bulleticon = pygame.image.load(os.path.join(path, r"images\PowerUpicons\fastbulleticon.png"))

        #sets how many bullets will be displayed when the scoreboard is first displayed
        self.bulletsshow = 5
        
    def GetBulletAmount(self):

        #gets how many bullets should be shown from the amount of available bullets the player tank has
        self.bulletsshow = (5- GameMec.player.totalbulletsfired)
        
    def render(self):

        #gets bulletsshow value for which image to display as the scoreboard
        self.GetBulletAmount()

        #sets current image corresponding to how many bullets need displaying
        self.image = self.images[self.bulletsshow]

        #if the player has a power up available for use...
        if GameMec.player.powerReady == True:

            #draw a green rectangle around the power up icon
            pygame.draw.rect(self.image,(0, 255, 0), (83, 7, 22, 22), 1)

            #if the power up stored is speed up
            if GameMec.player.powerStored == 1:

                #display icon for speed up
                self.image.blit(self.speedicon, (84, 8))

            #if the power up stored is fast bullets
            elif GameMec.player.powerStored == 0:

                #display icon for fast bullets
                self.image.blit(self.bulleticon, (84, 8))

            #if the power up stored is explosive rounds
            elif GameMec.player.powerStored == 2:

                #display icon for explosive rounds
                self.image.blit(self.bangbulleticon, (84, 8))

        #if the power up is activated...
        elif GameMec.player.powerActive == True:

            #draw a red rectangle around the power up icon
            pygame.draw.rect(self.image,(255, 0, 0), (83, 7, 22, 22), 1)

            #if the power up stored is speed up
            if GameMec.player.powerStored == 1:

                #display icon for speed up
                self.image.blit(self.speedicon, (84, 8))

            #if the power up stored is fast bullets    
            elif GameMec.player.powerStored == 0:

                #display icon for fast bullets
                self.image.blit(self.bulleticon, (84, 8))

            #if the power up stored is explosive rounds
            elif GameMec.player.powerStored == 2:

                #display icon for explosive rounds
                self.image.blit(self.bangbulleticon, (84, 8))
                
        #display scoreboard on screen
        screen.blit(self.image,(10,10)) ##
        
    


class Wall(pygame.sprite.Sprite):
    
    def __init__(self,x,y,w,h,name,walltype):

        #initialises pygame sprite class
        super().__init__()

        #sets attributes of wall
        self.name = name
        self.sightwalls =[]
        self.walltype = walltype

        #sets dimensions of wall
        self.image = pygame.Surface((w,h))
        self.image.fill((0,0,0))

        #sets start position of wall
        self.rect = self.image.get_rect(topleft = (x,y))


class Block(pygame.sprite.Sprite):
    
    def __init__(self,x,y,blocktype,colour):

        #initialises pygame sprite class
        super().__init__()

        #sets the block to not destroyed and sets type and position
        self.destroyed = False
        self.type = blocktype
        self.x = x
        self.y = y

        #if block is solid wood...
        if blocktype == 0:

            #set image to wood image
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\block.png")),(int(bw), int(bh)))

        #if block is breakeable...
        elif blocktype == 1:

            #set image to breakable block image
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\breakblock.png")),(int(bw), int(bh)))

        #if block is a hole...
        elif blocktype == 2:

            #set image to hole image
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\hole.png")),(int(bw), int(bh)))

        #if block is tank...
        elif blocktype  >= 10:

            #set image to tank image that corresponds to the blocktype (each type is a different colour)
            self.image = colourchange(pygame.image.load(os.path.join(path, r"images\playerrightfull.png")),colour)

        #sets the top left position of the block
        self.rect = self.image.get_rect(topleft = (x,y))

class Mine(pygame.sprite.Sprite):
    
    def __init__(self,pos):

        #initialises pygame sprite class
        super().__init__()

        #sets position of mine
        self.x = pos[0]
        self.y = pos[1]

        #loads 2 images of mine , one fore light being on or off
        self.image1 = pygame.image.load(os.path.join(path, r"images\mine1.png"))
        self.image2 = pygame.image.load(os.path.join(path, r"images\mine2.png"))

        #sets starting image
        self.image = self.image1

        #sets speed in which mine will count down to explosion
        self.speed = 128

        #timer starts at 0
        self.time = 0

        #sets top left of mine position
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

        #sets the mine to not exploded
        self.boom = False

                                        
    def animate(self):

        #increments timer by 1
        self.time +=1

        #if the timer is more than half the speed (if completed half a cycle)
        if self.time > (self.speed/2):

            #set light on
            self.image = self.image1
        else:

            #set light off
            self.image = self.image2

        #if timer is greater than speed (a whole cycle has been completed)
        if self.time > (self.speed):

            #reset timer
            self.time = 0

            #increase speed (increases flash time)
            self.speed /= 1.5
            self.speed += .55

        #if the mine is flashing faster than every 2 frames    
        if self.speed < 2:

            #set mine to exploded
            self.boom = True

            #instansiate an explosion
            GameMec.boomlist.append(BOOM(self.x,self.y))

            #end cycle
            return
        
        #if mine has already exploded
        if self.boom == True:
            
            #instansiate an explosion
            GameMec.boomlist.append(BOOM(self.x,self.y))

            #end cycle
            return
            
class BOOM:
    
    def __init__(self, x, y, destructive = True):

        #sets explosion to start on the first explosion image
        self.timer = 0

        #sets start position and centres it on the source
        self.x = x - 75
        self.y = y - 75

        #sets whether the explosion can destroy blocks
        self.destructive = destructive

        #creates a list of 8 images for the explosion
        self.images = []
        for i in range(1,8):
            self.images.append(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Explosions\boom"+str(i)+".png")),(200,200)))

        #sets the initial image for the explosion
        self.image = self.images[0]

        #sets rectangle for the explostion and centres is on the source 
        self.rect = self.image.get_rect(center = (x,y))

        #plays explosion sound
        sounds.play(0)
        
    def main(self):

        #if timer is less than or equal to 15 (timer hasnt ran out)
        if self.timer <= 15:

            #go to next image every 5 frames
            display_surface.blit(self.images[int(round(self.timer, 1))], (self.x, self.y))
            self.timer += 1/5
        
class object1:

    def __init__(self, x, y, speed, colour, bounce, name, bulletType, accuracy, shootwaitlimit):

        #sets colour of tank
        self.colour = colour

        #creates an empty list for lines of sight
        self.sightlines = []

        #sets name of tank to identify if its an enemy or player
        self.name = name

        #sets powers to False unless it has pre defined buffs
        self.powerActive = False
        self.powerStored = None
        self.powers = [bulletType,0,0,0,0,0]
        self.powerTimer = 0
        self.powerReady = False
        
        #sets tank to have the ability to move in all directions
        self.move_up = True
        self.move_right = True
        self.move_left = True
        self.move_down = True

        #sets the amount of times bullets fired from this tank can bounce
        self.bounce = bounce

        #sets enemy tanks to not being able to see the player
        self.canseeplayer = False

        #sets how long a tank has been waiting to shoot
        self.shootwait = 0

        #sets the offset of a tank when aiming at the player
        self.accuracy = accuracy

        #sets how long a tank has to wait before firing another bullet
        self.shootwaitlimit = shootwaitlimit

        #creates empty pathfinding path (will fill up as a list of coordinates to follow)
        self.coordpath = []

        #if tank is player tank 
        if colour == (blue) :

            #load images for blue tank and scale them in proportion to game window
            self.imagel1 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerleft1.png")),(int(60*tsf),int(42*tsf)))
            self.imagel2 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerleft2.png")),(int(60*tsf),int(42*tsf)))
            self.imager1 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerright1.png")),(int(60*tsf),int(42*tsf)))
            self.imager2 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerright2.png")),(int(60*tsf),int(42*tsf)))

        else:

            #load images for blue tank and scale them in proportion to game window AND change them to match the colour specified using colourchange function 
            self.imagel1 = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerleft1.png")),(int(60*tsf),int(42*tsf))), self.colour)
            self.imagel2 = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerleft2.png")),(int(60*tsf),int(42*tsf))), self.colour)
            self.imager1 = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerright1.png")),(int(60*tsf),int(42*tsf))), self.colour)
            self.imager2 = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Hulls\playerright2.png")),(int(60*tsf),int(42*tsf))), self.colour)

        #sets tank to start facing right
        self.direction = 1

        #instantiate turret class and set its colour to the same as the body
        self.turret = turret(self, self.colour)

        #set the tank to not have fired any bullets yet
        self.bulletsfired = 0
        self.totalbulletsfired = 0

        #sets base speed multiplier
        self.speed = speed

        #sets variable speed multiplier for powerups
        self.speedmult = self.speed

        #creates movement vector
        self.vector = pygame.Vector2()

        #creates rectangel for image and reduces size
        self.rect = self.imager1.get_rect(topleft = (x,y))
        self.rect.inflate(-25,-30)

        #sets start coordinates
        self.x = x
        self.y = y

        #sets location of where bullets are fired from
        self.bulletfirex, self.bulletfirey  = (self.rect.centerx), (self.rect.centery-10)

        #sets position along pathfinding path
        self.nodepos = 0

        
        try:
            #if tank is player tank, play sounds through channel 2
            if self.name == "player":
                self.channel = pygame.mixer.Channel(2)

            #otherwise play sounds through channel that corresponds to enemy number
            else:
                self.channel = pygame.mixer.Channel(int(self.name[5]))
        except:
            pass

        
    def main(self,master):

        #find coordinates in 16*16 grid, used for pathfinding
        self.coord = (int(self.rect.centerx/(bw)),int((self.rect.centery-10)/(bh/2)))

        #sets bullets to be fired from the current centre of tank
        self.bulletfirex, self.bulletfirey  = (self.rect.centerx), (self.rect.centery)

        #run ai shooting function
        self.ai_shoot(master)

        #manage power ups
        self.powermanager()
        


    def norm(self,x,y):

        #normalises vector, so it always has a magnitude of 1
        rat = abs(x)+ abs(y)
        return 1/rat *x, 1/rat *y


    def setPower(self):

        #create a random value between 0 and 100
        self.powerValue = random.randint(0,100)

        #if tank doesnt already have a powerup
        if self.powerStored == None:

            # 30% chance of activating fast bullets
            if self.powerValue < 30:
                self.powerStored = 0

            # 40% chance of activating speed up
            elif self.powerValue >= 30 and self.powerValue <= 70:
                self.powerStored = 1

            # 30% chance of activating explosive bullets
            else:
                self.powerStored = 2

            #set the tank to be ready to use a power up
            self.powerReady = True

        
    def powermanager(self):

        #activate power up if e key is pressed and there is a power ready to be used
        if self.powerReady == True and pressed[(ord("e"))] == True:

            #set the tank to not having a ready power up
            self.powerReady = False

            #if tank has activated speed power up
            if self.powerStored == 1:

                #set corresponding value in powers list to true and multiply the movement speed of the tank by 2
                self.powers[1] = True
                self.speedmult = self.speed*2

            #if tank has activated fast bullets power up   
            elif self.powerStored == 0:

                #set corresponding value in powers list to true
                self.powers[0] = 1

            #if tank has activated explosive bullets power up
            elif self.powerStored == 2:

                #set corresponding value in powers list to true
                self.powers[0] = 2

            #set the tank to be actively using a power up
            self.powerActive = True

        #if power up has been activated
        if self.powerActive == True:

            #increment timer by 1 
            self.powerTimer += 1

        #if power up has been active for 200 frames
        if self.powerTimer > 200:

            #reset speed multiplier
            self.speedmult = self.speed

            #set all active powers to false
            self.powers = [0, 0, 0, 0, 0, 0]

            #empties power up storage (tank can now pick up another power up)
            self.powerStored = None

            #reset timer
            self.powerTimer = 0

            #set the tank to not usng a power up
            self.powerActive = False

    def render(self):

        #if tank has a positive horizontal component (its moving right)
        if self.vector.x > 0:
            self.direction = 1

        #if tank has a negative horizontal component (its moving left)
        elif self.vector.x < 0:
            self.direction = 0

        #if tank is moving right or has stopped after moving right    
        if self.direction == 1:

            #display image based on a timer that cycles between true and false regularly to animate tank
            if clock1.skinstate() == 1:
                display_surface.blit(self.imager1, (self.rect.x, self.rect.y))
            else:
                display_surface.blit(self.imager2, (self.rect.x, self.rect.y))

        #if tank is moving left or has stopped after moving left
        elif self.direction == 0:

            #display image based on a timer that cycles between true and false regularly to animate tank
            if clock1.skinstate() == 1:
                display_surface.blit(self.imagel1, (self.rect.x, self.rect.y))
            else:
                display_surface.blit(self.imagel2, (self.rect.x, self.rect.y))
        
    
    def control(self, master):

        #reset movement vector
        self.vector = pygame.math.Vector2()

        #if w key is pressed
        if pressed[(ord("w"))] == True:

            #if allowed to move up
            if self.move_up:

                #set y vector to 1 upwards
                self.vector.y = -1

        #if s key is pressed
        elif pressed[(ord("s"))] == True:

            #if allowed to move down
            if self.move_down:

                #set y vector to 1 down
                self.vector.y = 1

        #if d key is pressed
        if pressed[(ord("d"))] == True:

            #if allowed to move right
            if self.move_right:

                #set x vector to 1 right
                self.vector.x = 1

        #if a key is pressed 
        elif pressed[(ord("a"))] == True:

            #if allowed to move left
            if self.move_left:

                #set x vector to 1 left
                self.vector.x = -1

        #if tank is moving diagonally
        if self.vector.x != 0 and self.vector.y != 0:

            #normalise movement vector so it has a magnitude of 1
            self.vector.x,self.vector.y = self.norm(self.vector.x,self.vector.y)

        #if tank is moving
        if self.vector.x != 0 or self.vector.y != 0:
            try:

                #if tank isnt playing track sound
                if self.channel.get_busy() == False:

                        #play track sound
                        self.channel.play(sounds.trundle)

                        #^^ this will continuously loop over the track sound while the tank is moving 
            except:
                pass
            
        #add vector multiplied by speed onto position to move the tank 
        self.x += self.vector.x*self.speedmult
        self.y += self.vector.y*self.speedmult

        #update collision rectangle to ontop of tank
        self.rect.x = self.x  
        self.rect.y = self.y 

        #if q key is pressed
        if pressed[(ord("q"))] == True:

            #set mine to not have been placed on another yet
            hit = False

            #get list of mines
            sprite_list = master.Get_Mine_List()

            #create a new mine
            new_mine = Mine((self.rect.centerx - 15, self.rect.centery - 20))

            #for every mine in the level dectect if the new mine has been placed ontop of it
            for mine in sprite_list:
                if mine.rect.colliderect(new_mine.rect):
                    hit = True

            #if mine hasnt been placed on another , add it to the level
            if hit == False:
                sprite_list.add(new_mine)

            #update mine list    
            master.Set_Mine_List(sprite_list)
        

        
    def undo_move(self, wall):

        #get name of wall being collided with
        self.wall = wall.name

        #if colliding with wall on the right of an object (NOT colliding with a wall on the right side of the tank)
        if self.wall == "right":

            #only allow tank to move away from wall, not into it
            self.move_right = True
            self.move_left = False

        #if colliding with wall on the bottom of an object    
        elif self.wall == "bottom":

            #only allow tank to move away from wall, not into it
            self.move_down = True                                  
            self.move_up = False

        #if colliding with wall on the left of an object
        elif self.wall == "left":

            #only allow tank to move away from wall, not into it
            self.move_left = True
            self.move_right = False

        #if colliding with wall on the top of an object
        elif self.wall == "top":

            #only allow tank to move away from wall, not into it
            self.move_up = True
            self.move_down = False

    
        
            

            
    def move_random(self):

        #create a random integer between 0 and 1000
        self.prob = random.randint(1, 1000)

        #1 in 40 chance per frame that tank will change direction
        if self.prob < 25:

            #if tank can move in either horizontal direction
            if self.move_left and self.move_right:

                #move in a random amount in horizontal axis
                self.vector.x = random.uniform(-1,1)

            #if tank can only move left
            elif self.move_right == False and self.move_left:

                #move a random amount left
                self.vector.x  = random.uniform(-1,0)

            #if tank can only move right
            elif self.move_left == False and self.move_right:

                #move a random amount right
                self.vector.x  = random.uniform(0,1)

            #if tank can move in either vertical direction
            if self.move_up and self.move_down:
                
                #move a random amount up or down
                self.vector.y = random.uniform(-1,1)

            #if tank can only move down
            elif self.move_up == False and self.move_down:
                
                #move a random amount down
                self.vector.y  = random.uniform(0,1)

            #if tank can only move up
            elif self.move_down == False and self.move_up:

                #move a random amount up
                self.vector.y  = random.uniform(-1,0)

        #if tank is moving, noramlise the vector so its magnitude is 1
        if self.vector.x != 0 and self.vector.y != 0:
            self.vector.x,self.vector.y = self.norm(self.vector.x,self.vector.y)

        #move the tank by vector multiplied by the speed multiplier
        self.x += self.vector.x*self.speedmult
        self.y += self.vector.y*self.speedmult

        #if not already playing sound and tank is moving, play tank track sound (creates looping audio)
        try:
            if self.channel.get_busy() == False and abs(self.vector.x*self.speedmult) > 0.1:
                self.channel.play(sounds.trundle)
        except:
            pass

        #centres pygame rect object over tank image
        self.rect.x = self.x
        self.rect.y = self.y

    def pathupdate(self):

        #creates a path between current tanks coordinates and player tanks coordinates
        self.path = GameMec.astar(GameMec.mappoints, (int(self.coord[0]),int(self.coord[1])), (int(GameMec.player.coord[0]),int(GameMec.player.coord[1])))

        #creates empty list
        self.coordpath = []

        #if tank isnt at destination, and a path has been found
        if self.path != None:

            #create a list of screen coordinates that correspond to map coordinates 
            for point in self.path:
                self.coordpath.append([point[0]*bw + bw/2, point[1]*bh/2+ bh/4])

            #sets tank to start at first coordinate
            self.nodepos = 1
            
    def nodemove(self):

        #if tank isnt at destination
        if len(self.coordpath)>0 and self.nodepos < (len(self.coordpath)):
                
            #set the objective to the next coordinate in the list
            self.objective = self.coordpath[self.nodepos]
            indicator(self.objective, (0,0,255))
            #create a displacement vector from tank to next coordinate
            self.vector.x = self.objective[0] - self.rect.centerx
            self.vector.y = self.objective[1] - self.rect.centery

            #normalise vector so it has magnitude of 1
            self.vector.x,self.vector.y = self.norm(self.vector.x,self.vector.y)

            #move tank using vector multiplied by speed multiplier
            self.x += self.vector.x*self.speedmult
            self.y += self.vector.y*self.speedmult
            
            #if tank is close enough to path coordinate, set destination to next coordinate
            if abs(self.objective[0] - self.rect.centerx) < 5 and abs(self.objective[1] - self.rect.centery) < 5:
                self.nodepos += 1

            #centre rect object
            self.rect.x = self.x
            self.rect.y = self.y

            #if not already playing sound and tank is moving, play tank track sound (creates looping audio)
            try:
                if self.channel.get_busy() == False and abs(self.vector.x*self.speedmult) > 0.1:
                    self.channel.play(sounds.trundle)
            except:
                pass
            
        #move randomly if path not found
        else:
            self.move_random()
            
    def force_move_random(self):

        #if tank can move in either horizontal direction
        if self.move_left and self.move_right:

            #move in a random amount in horizontal axis
            self.vector.x = random.uniform(-1,1)

        #if tank can only move left
        elif self.move_right == False and self.move_left:

            #move a random amount left
            self.vector.x  = random.uniform(-1,0)

        #if tank can only move right
        elif self.move_left == False and self.move_right:

            #move a random amount right
            self.vector.x  = random.uniform(0,1)

        #if tank can move in either vertical direction
        if self.move_up and self.move_down:
            
            #move a random amount up or down
            self.vector.y = random.uniform(-1,1)

        #if tank can only move down
        elif self.move_up == False and self.move_down:
            
            #move a random amount down
            self.vector.y  = random.uniform(0,1)

        #if tank can only move up
        elif self.move_down == False and self.move_up:
            
            #move a random amount up
            self.vector.y  = random.uniform(-1,0)

        #if tank is moving diagonally, normalise its vector to a magnitude of 1 
        if self.vector.x != 0 and self.vector.y != 0:
            self.vector.x,self.vector.y = self.norm(self.vector.x,self.vector.y)

        #move tank using vector multiplied by speed multiplier    
        self.x += self.vector.x*self.speedmult
        self.y += self.vector.y*self.speedmult

        #centres pygame rect object over tank image
        self.rect.x = self.x 
        self.rect.y =self.y
        

    def CollideWithTank(self, tank2):

        #gets rect object of tank being collided with
        rect = tank2.rect

        #if top left point is colliding with tank
        if rect.collidepoint(((self.rect.topleft[0]+self.vector.x-4),(self.rect.topleft[1]))):

            #force the tank to move away from the other tank
            self.move_left = False
            self.move_right = True
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.topright[0]+self.vector.x+4,self.rect.topright[1])):

            #force the tank to move away from the other tank
            self.move_right = False
            self.move_left = True
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.bottomleft[0]+self.vector.x-4,self.rect.bottomleft[1])):
            
            #force the tank to move away from the other tank
            self.move_left = False
            self.move_right = True
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.bottomright[0]+self.vector.x+4,self.rect.bottomright[1])):
            
            #force the tank to move away from the other tank
            self.move_right = False
            self.move_left = True
            self.force_move_random()

        #if top left corner is colliding with tank
        if rect.collidepoint((self.rect.topleft[0],self.rect.topleft[1]+self.vector.y-4)):

            #force the tank to move away from the other tank
            self.move_up = False
            self.move_down = True
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.topright[0],self.rect.topright[1]+self.vector.y-4)):

            #force the tank to move away from the other tank
            self.move_down = True
            self.move_up = False
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.bottomleft[0],self.rect.bottomleft[1]+self.vector.y+4)):

            #force the tank to move away from the other tank
            self.move_up = True
            self.move_down = False
            self.force_move_random()

        #if top left corner is colliding with tank
        elif rect.collidepoint((self.rect.bottomright[0],self.rect.bottomright[1]+self.vector.y+4)):

            #force the tank to move away from the other tank
            self.move_down = False
            self.move_up = True
            self.force_move_random()
            
    def ai_shoot(self, master):

        #fire a bullet if the tank has seen the player for long enough and reset the wait timer
        if self.shootwait > self.shootwaitlimit :
            self.fire()
            self.shootwait = 0
    
    def is_collided_with(self, sprite):

        #return true if rect objects are overlapping
        return self.rect.colliderect(sprite.rect)

    def fire(self):

        #if tank has any bullets left
        if self.totalbulletsfired < 5:

            #play shoot sound
            sounds.play(2)

            #add a bullet to the list of all bullets on screen
            GameMec.Bullets_list.append(bullet(self,len(GameMec.Bullets_list)+1,self.bounce))
            self.bulletsfired += 1
            self.totalbulletsfired += 1
            
class turret:

    def __init__(self, master, colour):

        #copy colour from the hull of the tank that the turret is on
        self.colour = colour

        #get the hull of the tank
        self.master = master

        #set turret to start facing 0
        self.turretangle = 0

        #for random movement , start turning anticlockwise
        self.turn = -1

        #create a random starting angle
        self.findangle(None)

        #load, scale and colour an image for each turret direction
        self.turretimager = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretr.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimagerd = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretrd.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimaged = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretd.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimageld = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretld.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimagel = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretl.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimagelu = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretlu.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimageu = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretu.png")),(int(36*tsf),int(23*tsf))), self.colour)
        self.turretimageru = colourchange(pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\Tanks\Player\Turrets\turretru.png")),(int(36*tsf),int(23*tsf))), self.colour)


    def findangle(self, aim_at):
        
        #if theres nothing to aim at
        if aim_at == None:

            #create a random number up to 1000
            self.prob = random.randint(1, 1000)

            #1% chance every frame that the turret will start turning opposite direction
            if self.prob < 10:
                self.turn *= -1

            #turn an angle between 0 and 5 in the direction specified
            self.turretangle += random.randint(0,5)*self.turn

            #correct the angle if its too high
            self.turretangle = self.turretangle%360
            self.angle = -self.turretangle
                
        #if there is something to aim at    
        else:

            #do some pythagoras and find out the vertical and horizontal components of the vector from the tank to wherever its aiming at
            self.vecx = ((0 - (self.master.bulletfirex - aim_at.rect.centerx))/math.hypot((self.master.bulletfirex - aim_at.rect.centerx),(self.master.bulletfirey - aim_at.rect.centery)))
            self.vecy = ((0 - (self.master.bulletfirey - aim_at.rect.centery))/math.hypot((self.master.bulletfirex - aim_at.rect.centerx),(self.master.bulletfirey - aim_at.rect.centery)))

            #find the bearing of said vector and correct its angle
            self.turretangle = math.degrees(math.atan2((self.vecy), (self.vecx)))
            self.turretangle += 90
            self.turretangle = self.turretangle%360
            self.angle = -self.turretangle


    def render(self, x, y):

        #render the turret image according to the angle the turret should be facing ontop of the correct tank
        self.x = x
        self.y = y
        if (self.turretangle < 22.5) or (self.turretangle >= 337.5):
            display_surface.blit(self.turretimageu, (self.x + (13*tsf), self.y))
        elif self.turretangle >=22.5 and self.turretangle < 67.5:
            display_surface.blit(self.turretimageru, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 67.5 and self.turretangle < 112.5:
            display_surface.blit(self.turretimager, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 112.5 and self.turretangle < 157.5:
            display_surface.blit(self.turretimagerd, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 157.5 and self.turretangle < 202.5:
            display_surface.blit(self.turretimaged, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 202.5 and self.turretangle < 247.5:
            display_surface.blit(self.turretimageld, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 247.5 and self.turretangle < 292.5:
            display_surface.blit(self.turretimagel, (self.x + (13*tsf), self.y))
        elif self.turretangle >= 292.5 and self.turretangle < 337.5:
            display_surface.blit(self.turretimagelu, (self.x + (13*tsf), self.y))

class powerbox(pygame.sprite.Sprite):
    
    def __init__(self, x, y):

        #initialises inherited pygame sprite class
        super().__init__()

        #loads image of power up box and scale it 
        self.image = pygame.image.load(os.path.join(path, r"images\powerbox.png"))
        self.image = pygame.transform.scale(self.image,(30,40))
        
        #get rect object of power up box
        self.rect = self.image.get_rect(topleft=(x,y))

class bullet:

    def __init__(self, master, bulletid,bounce):

        #loads images for each type of bullet and scales them in proportion to the rest of the screen
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\bullet.png")),(int(6*sf*2),int(9*sf*2)))
        self.imagefast1 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\fastbullet1.png")),(int(6*sf*2),int(16*sf*2)))
        self.imagefast2 = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\fastbullet2.png")),(int(6*sf*2),int(16*sf*2)))
        self.imageboom = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\bangbullet.png")),(int(9*sf*2),int(12*sf*2)))

        #sets what object shot the bullet
        self.master = master

        #set the bullet to fired (begins movement)
        self.bulletfired = True

        #sets the speed of the bullet if unaltered by a power up
        self.speedmult = 5
        
        #sets the angle in which the bullet wll travel at
        self.angle = 0 - (self.master.turret.angle)

        #gets pygame rect object of the bullet (changes with bullet type)
        self.rect = self.image.get_rect()

        #sets the amount of times the bullet can bounce
        self.bounce = bounce
        self.MaxBounce = self.bounce

        #sets the bullet to not yet bounced
        self.NumBounce = 0

        #set the direction and velocity of bullet 
        self.fire()

        #begin moving
        self.main()

    def main(self):
        
        #if bullet has been fired
        if self.bulletfired == True:

            #move and render the bullet
            self.move()
            self.render()

        #if it hasnt been fired
        else:

            #hold the bullet within the tank
            self.x, self.y = ((self.master.rect.x)+(30*tsf), (self.master.rect.y)+(3.5*tsf))

        #update the rect object of the bullet
        self.rect = self.image.get_rect()
        self.rect.center = ((self.x)+(3*sf*2), (self.y)+(4*sf*2))
        
        
    def fire(self):

        #sets state of animation to first frame
        self.animate = 1

        #sets direction of bullet movement to where the tank is aiming
        self.vector = self.get_mouse_vector()

        #starts the bullet at the tank of which it was fired from
        self.x, self.y = ((self.master.rect.x)+(30*tsf), (self.master.rect.y)+(10*tsf))

        #sets the type of bullet 
        self.type = self.master.powers[0]

        #if bullet is explosive
        if self.type == 2:

            #explode on first hit
            self.MaxBounce = 0

        else:

            #bounce as many times as allowed by the tank
            self.MaxBounce = self.bounce
        
    def move(self):

        #if a normal bullet
        if self.type == 0:

            #move at normal speed
            self.x += self.vector.x
            self.y += self.vector.y

        #if an explosive round
        elif self.type == 2:

            #move half as fast
            self.x += self.vector.x*0.5
            self.y += self.vector.y*0.5

        #if a fast bullet
        else:

            #move twice as fast
            self.x += self.vector.x*2
            self.y += self.vector.y*2


    def render(self):

        #change  animation state every frame
        self.animate *= -1

        #if a normal bullet
        if self.type == 0:

            #display normal bullet image at bullet coordinates and rotated to correct angle
            display_surface.blit((pygame.transform.rotate(self.image, self.angle)), (self.x, self.y))
        
        #if a fast bullet
        elif self.type == 1:
            
            #depending on animation state display either fast bullet image at bullet coordinates and rotated to correct angle
            if self.animate == 1:
                display_surface.blit((pygame.transform.rotate(self.imagefast1, self.angle)), (self.x, self.y))
            else:
                display_surface.blit((pygame.transform.rotate(self.imagefast2, self.angle)), (self.x, self.y))
        
        #if and explosive round
        elif self.type == 2:

            #display explosive bullet image at bullet coordinates and rotated to correct angle
            display_surface.blit((pygame.transform.rotate(self.imageboom, self.angle)), (self.x, self.y))
            
    def setfired(self, boolean):

        #sets a bullet to fired then fires a bullet
        self.bulletfired = boolean
        self.fire()

    def reset_bounce(self):
        
        #resets the bullets bounce count and adds bullet back to available from the tank it was fired from
        self.NumBounce = 0
        self.main()
        self.x = -10
        self.y = -10
        self.master.totalbulletsfired -=1
        self.main()

    def get_mouse_vector(self):

        #sets speed at which bullet will travel
        self.speedmult = 5

        #if the player fired the bullet
        if self.master == GameMec.player:
            try:

                #do some pythagoras and  find the horizontal vector component
                self.vecx = ((0 - (self.master.bulletfirex - cursorpos[0]))/math.hypot((self.master.bulletfirex - cursorpos[0]),(self.master.bulletfirey - cursorpos[1]))*self.speedmult)

                #do some pythagoras and  find the vertical vector component
                self.vecy = ((0 - (self.master.bulletfirey - cursorpos[1]))/math.hypot((self.master.bulletfirex - cursorpos[0]),(self.master.bulletfirey - cursorpos[1]))*self.speedmult)

            #if theres a division by zero error
            except ZeroDivisionError:

                #keep current vector components
                self.vecx = self.vecx
                self.vecy = self.vecy

        #if bullet fired by enemy
        else:
            try:

                #add a random offset to the aiming up to the accuracy limit of the tank
                self.aimposx = random.uniform(-self.master.accuracy,self.master.accuracy) + GameMec.player.rect.centerx
                self.aimposy = random.uniform(-self.master.accuracy,self.master.accuracy) + GameMec.player.rect.centery

                #do some pythagoras and  find the horizontal vector component
                self.vecx = ((0 - (self.master.bulletfirex - self.aimposx))/math.hypot((self.master.bulletfirex - self.aimposx),(self.master.bulletfirey - self.aimposy))*self.speedmult)

                #do some pythagoras and  find the vertical vector component
                self.vecy = ((0 - (self.master.bulletfirey - self.aimposy))/math.hypot((self.master.bulletfirex - self.aimposx),(self.master.bulletfirey - self.aimposy))*self.speedmult)
            
            #if theres a division by zero error
            except ZeroDivisionError:

                #keep current vector components
                self.vecx = self.vecx
                self.vecy = self.vecy
            
        #find bearing of the vector and do some trig on it to find the angle    
        self.angle  = math.degrees(math.atan2((self.vecy), (self.vecx)))

        #correct the angle because it was off for some reason
        self.angle += 90
        self.angle = self.angle%360
        self.angle *= -1
        
        #return the vector in a pygame vector object
        return pygame.Vector2(self.vecx, self.vecy)


    def is_collided_with(self, sprite):
        
        #return true if bullet is coliding with object passed in
        return self.rect.colliderect(sprite.rect)
        
class clock:
    def __init__(self):

        #start at 0
        self.value = 0


    def skinstate(self):

        #after 15 frames out of 30
        if self.value >= 15:

            #return True
            return (1)

        #before 15 frames out of 30
        else:

            #return False
            return (0)


    def increment(self):

        #increase by 1 every frame
        self.value += 1

        #reset if at 30 frames
        if self.value == 30:
            self.value = 0 


class cursor:

    def __init__(self):

        #load image for the cursor and get its rect object
        self.image = pygame.image.load(os.path.join(path, r"images\cursor1.png"))
        self.rect = self.image.get_rect()


    def render(self, x,y):

        #get position
        self.position = (x,y)

        #if in game only display in game window
        if Menu.type == 0:
            display_surface.blit(self.image, (self.position[0]- 8, self.position[1]- 8))

        #if in menu display anywhere on screen
        else:
            screen.blit(self.image, (self.position[0]- 8, self.position[1]- 8))
        
        #update rect object
        self.rect = self.image.get_rect(topleft = (x,y))

class cursordots:
    def __init__(self):

        #load image for dot
        self.image = pygame.image.load(os.path.join(path, r"images\dot.png"))
        
    def render(self, player):

        try:
            
            #get distance between player tank and cursor
            self.vecx = player.bulletfirex - cursorpos[0]
            self.vecy = player.bulletfirey - cursorpos[1]

        #if tank and cursor have same coordinates
        except ZeroDivisionError:

            #use previous coordinates
            self.vecx = self.vecx
            self.vecy = self.vecy

        #display a dot at every 1/6 th of the distance between tank and cursor
        for i in range(1,6):
            display_surface.blit(self.image, ((player.rect.x - ((self.vecx)*(i/6))+ (30*tsf)),(player.rect.y - ((self.vecy)*(i/6))+(10*tsf))))

def colourchange(surface, colour):

    #get an array of pixels for the surface provided
    pxarray = pygame.PixelArray(surface)

    #colour of blue tank
    primary = (0, 162, 232)
    secondary = (63, 72, 204)

    #replace all primary colour with new primary colour
    pxarray.replace(primary, colour[0])

    #replace all secondary colour with new secondary colour
    pxarray.replace(secondary, colour[1])

    #return the new surface
    return (pxarray.make_surface())

class indicator:
    def __init__(self,pos,colour):

        #draw a small box with specified colour at specified location (for debug)
        pygame.draw.rect(display_surface, colour, (pos[0],pos[1],10,10))

class game:
    def __init__(self,file=None):

        #start at first level in file
        self.levelid = 0

        #load level specified
        self.LoadLevel(file)
        self.file = file

        #set to not pressing any buttons
        self.space_down = False
        self.escdown = False
        
        

    def LoadLevel(self,file):

        #create empty lists/groups for everything
        self.blocklist = []
        self.PinkBlocks = []
        self.Bullets_list = []
        self.boomlist = []
        self.EnemyTanks = []
        self.PowerBoxes = []
        self.wallhtop = pygame.sprite.Group()
        self.wallhbot = pygame.sprite.Group()
        self.wallvright = pygame.sprite.Group()
        self.wallvleft = pygame.sprite.Group()
        self.AllWalls = pygame.sprite.Group()
        self.AllPowerBoxes = pygame.sprite.Group()
        self.block_list_sprite = pygame.sprite.Group()
        self.hole_list_sprite = pygame.sprite.Group()
        self.mine_list = pygame.sprite.Group()

        #sets the amount of tanks in the level
        self.enemytanknum = Menu.enemytanknum

        #instantiates scoreboard
        self.playerscoreboard = Scoreboards()

        #loads outer walls
        self.LoadWallList()

        #gets walls from level file
        self.CreateWalls()

        #creates lines that block enemy sight from wall objects
        self.CreateSightBounds()

        #sets attributes of player
        self.LoadPlayerDetails()

        #instantiates player
        self.LoadPlayer()

        #instantiates enemies
        self.LoadEnemies()

        #gets filename
        self.file = file

        #set to create path for first tank
        self.pathnum = 0
        self.pathtime = 0

        #create map of driveable area for pathfinding
        self.remap()
    
    def nextlevel(self):

        #if in career mode
        if Menu.customlvl == False:

            #load next level into game
            Menu.levelid += 1
            Menu.GetLevel(self.file)
            self.LoadLevel(self.file)

        #if in custom level mode
        else:

            #go to win screen
            Menu.setmenu(31)
        
    def LoadPlayer(self):

        #instantiates player and cursordots
        self.player = object1(self.PlayerDetails[0], self.PlayerDetails[1], self.PlayerDetails[2], self.PlayerDetails[3],1, self.PlayerDetails[4], self.PlayerDetails[5],self.PlayerDetails[6], self.PlayerDetails[7])
        self.cursor_dots = cursordots()
        
    def LoadEnemies(self):
        
        #instantiate every enemy tank and add it to a list
        for tank in Menu.enemy_list:
            self.EnemyTanks.append(object1(tank[0], tank[1], tank[2], tank[3],tank[4], tank[5], tank[6],tank[7], tank[8]))
        
    def LoadWallList(self):

        #create wall list and add outer walls to it
        self.wall_list = [[0,-20,sw,20],[-20,-20,20,sh+220],[sw,-20,20,sh+20],[-50,sh,sw+100,20]]

    

    
    def CreateWalls(self):
        
        #creates borders for each side of a wall , each being 8 pixels thick, then add it to a list of walls for each side
        for wally in self.wall_list:
            #objecttop
            top = Wall(wally[0],  wally[1],                 wally[2],   8, 'top',0)
            #objectbot
            bot = Wall(wally[0],  wally[1]+((wally[3])-8),  wally[2],   8, 'bottom',0)
            #objectleft
            left = Wall(wally[0], wally[1],                 8,          wally[3], 'left',0)
            #objectright
            right = Wall(wally[0]+(wally[2]-8),wally[1],    8,          wally[3],'right',0)
            self.wallhtop.add(top)
            self.wallhbot.add(bot)
            self.wallvright.add(right)
            self.wallvleft.add(left)
            self.AllWalls.add(top, bot, left, right)

        #creates borders for each side of a block , each being 8 pixels thick, then add it to a list of walls for each side of the block
        for block in Menu.block_list:
            bottom = Wall(block[0]+8, block[1]+(bh*(block[3]))/2-8 + bh/2, (bw*block[2])-16, 8,'bottom', block[4])
            
            top = Wall(block[0]+8, block[1] +(bh/2), (bw*block[2])-16, 8,'top', block[4])
            
            left = Wall(block[0], block[1]+8+(bh/2), 8, ((bh*block[3])/2)-16,'left', block[4])
            
            right = Wall(block[0]+(bw*block[2])-8, block[1]+8+(bh/2), 8, (bh*block[3])/2-16,'right', block[4])
            
            self.wallhtop.add(top)
            self.wallhbot.add(bottom)
            self.wallvright.add(right)
            self.wallvleft.add(left)
            self.AllWalls.add(top, bottom, left, right)
            self.blocklist.append(block)
            
            #builds level in sprites for each individual block and adds it to a list that it belongs to depending on its type
            for i in range(block[2]): #width
                for j in range(block[3]): #height
                    new_block = Block(block[0]+(i*bw),block[1]+(j*(bh/2)),block[4],0)
                    if block[4] != 2:
                        self.block_list_sprite.add(new_block)
                        if block[4] == 1:
                            self.PinkBlocks.append([bottom,top,left,right,new_block])
                    else:
                        self.hole_list_sprite.add(new_block)
                
    def CreateSightBounds(self):
        
        #for every wall, if it isnt part of a hole, draws a line from start to end and add it to sight walls list 
        for wall in self.wallvleft:
            if wall.walltype != 2:
                wall.sightwalls.append([[wall.rect.centerx - 4 , wall.rect.y - 8 ],[wall.rect.centerx - 4 , wall.rect.y + wall.rect.height + 8]])
        for wall in self.wallvright:
            if wall.walltype != 2:
                wall.sightwalls.append([[wall.rect.centerx + 4 , wall.rect.y - 8],[wall.rect.centerx + 4, wall.rect.y+ wall.rect.height + 8]])
        for wall in self.wallhtop:
            if wall.walltype != 2:
                wall.sightwalls.append([[wall.rect.x - 8, wall.rect.centery - 4 ],[wall.rect.x+wall.rect.width + 8, wall.rect.centery - 4]])
        for wall in self.wallhbot:
            if wall.walltype != 2:
                wall.sightwalls.append([[wall.rect.x - 8, wall.rect.centery + 4 ],[wall.rect.x+wall.rect.width + 8 , wall.rect.centery + 4]])
        

    def CombineAll(self):

        #creates a list of every tank
        self.AllTanks = []
        self.AllTanks.append(self.player)
        for tank in self.EnemyTanks:
            self.AllTanks.append(tank)

    def LoadPlayerDetails(self):

        #sets players spawn location , speed, colour , name and abilities
        self.PlayerDetails = [Menu.spawn[0],Menu.spawn[1],3,blue,"player", 0, 0, 0]   

    def preloop(self):
        
        #combine all tanks to one list
        self.CombineAll()

        #create white background
        display_surface.fill((255,255,255))

        # main loop of all tanks
        self.player.main(self)
        for i in range(len(self.EnemyTanks)):
            self.EnemyTanks[i].main(self)
        
        # detects control for player tank
        self.player.control(self)

        # update pathfinding
        self.pathtime +=1
        self.pathtime = self.pathtime%20
        if self.pathtime == 0:
            self.pathnum+=1
            self.pathnum = self.pathnum%len(self.EnemyTanks)
            self.EnemyTanks[self.pathnum].pathupdate()

        # move enemy
        for tank in self.EnemyTanks:
            tank.nodemove()

        #work out angle for player
        self.player.turret.findangle(cursor1)

        #work out angle for enemy
        for tank in self.EnemyTanks:
            if tank.canseeplayer == True:
                tank.turret.findangle(self.player)
            else: 
                tank.turret.findangle(None)

        #for every mine , make it count down and if its exploded, remove it
        for i in self.mine_list:
            i.animate()
            if i.boom == True:
                self.mine_list.remove(i)
        
        #display all mines on screen
        self.mine_list.draw(display_surface)
        
        #display all tanks on screen
        self.player.render()
        for i in range(len(self.EnemyTanks)):
            self.EnemyTanks[i].render()

        #for every tank, chack if it can see the player
        self.InFieldOfView()

        #for every explosion currently happening, run its animation and remove it once the animation is complete
        for explosion in self.boomlist:
            explosion.main()
            if explosion.timer > 7:
                self.boomlist.remove(explosion)


    def main(self):
        
        #constantly moves the cursor to back into the game screen while the game is running
        if cursorpos[0] < (0):
            pygame.mouse.set_pos([gamescreenx, cursorpos[1]+gamescreeny])
        if cursorpos[0] > (sw):
            pygame.mouse.set_pos([gamescreenx+sw, cursorpos[1]+gamescreeny])
        if cursorpos[1] < (0):
            pygame.mouse.set_pos([cursorpos[0]+gamescreenx, gamescreeny])
        if cursorpos[1] > (sh):
            pygame.mouse.set_pos([cursorpos[0]+gamescreenx, gamescreeny+sh])
        
        #gets the state of the space and escape key in the frame before
        self.pre_space = self.space_down
        self.pre_esc = self.escdown

        #if the space key has been pressed , and previously wasnt pressed, fire a bullet    
        if pressed[ord(" ")] == True:
            self.space_down = True
            if self.space_down == self.pre_space:
                if pressed[ord(" ")] == True:
                    pressed[ord(" ")] = False
            else:
                self.player.fire()
        else:
            self.space_down = False
            self.pre_space = False
        
        #if the escape key has been pressed , and previously wasnt pressed, load pause menu
        if pressed[27]:
            self.escdown = True
            if self.escdown == self.pre_esc:
                if pressed[27] == True:
                    pressed[27] = False
            else:
                gamestarted = False
                Menu.setmenu(60)
        else:
            self.escdown = False
            self.pre_esc = False
        
        #move everything
        self.preloop()

        #display everything
        self.renderall()

        #detect and handle collision between everything
        self.CollideDetectTankTank()
        self.CollideDetectBulletTank()
        self.CollideDetectBulletWalls()
        self.CollideDetectTankWall()
        self.CollideDetectTankBox()
        self.CollideDetectBulletBullet()
        self.CollideDetectBoomTank()
        self.CollideDetectBoomWall()
        self.CollideDetectBulletMine()

        #go to the next level if theres no enemy tanks left
        if len(self.EnemyTanks) == 0:
            self.nextlevel()

        #display cursor on the game screen
        cursor1.render(cursorpos[0],cursorpos[1]-10)

        #display the game screen on the big screen
        screen.blit(display_surface,(gamescreenx,gamescreeny))
        
    def MoveBulletIfNes(self):

        #move all bullets 
        for bullet in self.Bullets_list:
            bullet.main()

    def CollideDetectBulletWalls(self):

        #for every bullet
        for bullet in self.Bullets_list:

            #set it to not bounced yet this frame
            self.detections = 0

            #if the bullet has been fired
            if bullet.bulletfired == True:

                #if its not explosive
                if bullet.type != 2:

                    #for every wall on the bottom of an object    
                    for wall in self.wallhbot:

                        #for every wall thats not a hole
                        if wall.walltype != 2:

                            #if it hasnt detected a bounce yet this frame
                            if self.detections == 0:

                                #if its touching the wall
                                if bullet.is_collided_with(wall):

                                    #make a bounce noise
                                    sounds.play(3)

                                    #if its bounced more than allowed
                                    if bullet.NumBounce >= bullet.MaxBounce:

                                        #get rid of the bullet
                                        bullet.master.bulletsfired -=1
                                        bullet.master.totalbulletsfired -=1
                                        self.Bullets_list.remove(bullet)

                                    #if its still allowed to bounce    
                                    else:

                                        #bounce it
                                        bullet.NumBounce+=1
                                        bullet.vector.y *= -1
                                        bullet.angle =(180 - bullet.angle)
                                    
                                    #say that its bounced this frame
                                    self.detections +=1   

                    #for every wall on the top of an object                 
                    for wall in self.wallhtop:

                        #for every wall thats not a hole
                        if wall.walltype != 2:

                            #if it hasnt detected a bounce yet this frame
                            if self.detections == 0:

                                #if its touching the wall
                                if bullet.is_collided_with(wall):

                                    #make a bounce noise
                                    sounds.play(3)

                                    #if its bounced more than allowed
                                    if bullet.NumBounce >= bullet.MaxBounce:

                                        #get rid of the bullet
                                        bullet.master.bulletsfired -=1
                                        bullet.master.totalbulletsfired -=1
                                        self.Bullets_list.remove(bullet)
                                    
                                    #if its still allowed to bounce
                                    else:

                                        #bounce it
                                        bullet.NumBounce+=1
                                        bullet.vector.y *= -1
                                        bullet.angle =(180 - bullet.angle)

                                    #say that its bounced this frame    
                                    self.detections +=1

                                    
                    #for every wall on the left of an object                 
                    for wall in self.wallvleft:

                        #for every wall thats not a hole
                        if wall.walltype != 2:

                            #if it hasnt detected a bounce yet this frame
                            if self.detections == 0:

                                #if its touching the wall
                                if bullet.is_collided_with(wall):

                                    #make a bounce noise
                                    sounds.play(3)

                                    #if its bounced more than allowed
                                    if bullet.NumBounce >= bullet.MaxBounce:

                                        #get rid of the bullet
                                        bullet.master.bulletsfired -=1
                                        bullet.master.totalbulletsfired -=1
                                        self.Bullets_list.remove(bullet)
                                    
                                    #if its still allowed to bounce
                                    else:

                                        #bounce it
                                        bullet.NumBounce+=1
                                        bullet.vector.x *= -1
                                        bullet.angle =(-bullet.angle)
                                    
                                    #say that its bounced this frame 
                                    self.detections += 1

                    #for every wall on the right of an object                
                    for wall in self.wallvright:

                        #for every wall thats not a hole
                        if wall.walltype != 2:

                            #if it hasnt detected a bounce yet this frame
                            if self.detections == 0:

                                #if its touching the wall
                                if bullet.is_collided_with(wall):

                                    #make a bounce noise
                                    sounds.play(3)

                                    #if its bounced more than allowed
                                    if bullet.NumBounce >= bullet.MaxBounce:

                                        #get rid of the bullet
                                        bullet.master.bulletsfired -=1
                                        bullet.master.totalbulletsfired -=1
                                        self.Bullets_list.remove(bullet)
                                    
                                    #if its still allowed to bounce
                                    else:

                                        #bounce it
                                        bullet.NumBounce+=1
                                        bullet.vector.x *= -1
                                        bullet.angle =(-bullet.angle)
                                    
                                    #say that its bounced this frame 
                                    self.detections += 1

                #for every destructable block                    
                for wall in self.PinkBlocks:

                    #if it hasnt detected a bounce yet this frame
                    if self.detections == 0:

                        #if its touching the wall
                        if bullet.is_collided_with(wall[4]):

                            #if bullet is explosive
                            if bullet.type == 2:

                                #remove block that it hit from all lists
                                self.wallhbot.remove(wall[0])
                                self.wallhtop.remove(wall[1])
                                self.wallvleft.remove(wall[2])
                                self.wallvright.remove(wall[3])
                                self.AllWalls.remove(wall[0])
                                self.AllWalls.remove(wall[1])
                                self.AllWalls.remove(wall[2])
                                self.AllWalls.remove(wall[3])
                                self.PinkBlocks.remove(wall)
                                self.block_list_sprite.remove(wall[4])

                                #remove the bullet and cause an explosion
                                bullet.master.bulletsfired -=1
                                bullet.master.totalbulletsfired -=1
                                self.boomlist.append(BOOM(bullet.x,bullet.y))
                                self.Bullets_list.remove(bullet)

                                #remap driveable area for pathfinding
                                self.remap()

                #if bullet is explosive                
                if bullet.type == 2:
                    for wall in self.AllWalls:
                        if wall.walltype != 2:

                            #if it collides with any wall that isnt a hole
                            if bullet.is_collided_with(wall):

                                #cause an explosion and remove the bullet
                                self.boomlist.append(BOOM(bullet.x,bullet.y))
                                bullet.master.bulletsfired -=1
                                bullet.master.totalbulletsfired -=1
                                self.Bullets_list.remove(bullet)

    def CollideDetectBulletTank(self):
        for tank in self.AllTanks:
            for bullet in self.Bullets_list:
                if bullet.master != tank or bullet.NumBounce > 0:
                    if bullet.bulletfired == True:
                        if bullet.is_collided_with(tank):
                                
                            bullet.master.bulletsfired -=1
                            bullet.master.totalbulletsfired -=1
                            self.Bullets_list.remove(bullet)
                            if bullet.type == 2:
                                self.boomlist.append(BOOM(bullet.x,bullet.y))
                            try:
                                self.boomlist.append(BOOM(tank.rect.x,tank.rect.y,False))
                                if tank != self.player:
                                    drop = random.randint(0,100)
                                    if drop > 60:
                                        self.AllPowerBoxes.add(powerbox(tank.rect.x,tank.rect.y))
                                else:
                                    Menu.setmenu(30)
                                
                                self.EnemyTanks.remove(tank)
                                self.AllTanks.remove(tank)
                            except:
                                pass
                            tank.x = 9999
                            tank.y = 9999

    def CollideDetectTankBox(self):
        for tank in self.AllTanks:
            if tank == self.player:
                for box in self.AllPowerBoxes:
                    if tank.is_collided_with(box):
                        self.player.setPower()
                        self.AllPowerBoxes.remove(box)
                




    def CollideDetectTankTank(self):
        for tank in self.AllTanks:
            for tank2 in self.AllTanks:
                if tank != tank2:
                    tank.CollideWithTank(tank2)
                    tank2.CollideWithTank(tank) 
                    
    def CollideDetectTankWall(self):
        
        for tank in self.AllTanks:
            
            if tank == self.player:
                detections = 0
                for wall in self.AllWalls:
                    if abs(tank.rect.x - wall.rect.x) < 300 or abs(tank.rect.y - wall.rect.y) < 300:
                        if tank.is_collided_with(wall):
                            self.player.undo_move(wall)
                            detections += 1
                            
                        if detections == 0:
                            tank.move_up = True
                            tank.move_down = True
                            tank.move_right = True
                            tank.move_left = True
                        
                        
                    
            else:    
                detections = 0
                for wall in self.AllWalls:
                    if abs(tank.rect.x - wall.rect.x) < 300 or abs(tank.rect.y - wall.rect.y)< 300:
                        if tank.is_collided_with(wall):
                            tank.undo_move(wall)
                            detections += 1
                            tank.force_move_random()
                        if detections == 0:
                            tank.move_up = True
                            tank.move_down = True
                            tank.move_right = True
                            tank.move_left = True

    def CollideDetectBulletBullet(self):
        for bullet in self.Bullets_list:
            for bullet2 in self.Bullets_list:
                if bullet != bullet2:
                    if bullet.is_collided_with(bullet2):
                        bullet.master.bulletsfired -=1
                        bullet.master.totalbulletsfired -=1
                        if bullet.type == 2:
                            self.boomlist.append(BOOM(bullet2.x,bullet2.y))
                        try:
                            sounds.play(3)
                            self.Bullets_list.remove(bullet)
                        except:
                            pass
                        bullet2.master.bulletsfired -=1
                        bullet2.master.totalbulletsfired -=1
                        if bullet2.type == 2:
                            self.boomlist.append(BOOM(bullet.x,bullet.y))
                        self.Bullets_list.remove(bullet2)
                        
    def CollideDetectBoomTank(self): 
        for boom in self.boomlist:
            for tank in self.AllTanks:
                if boom.destructive == True:
                    self.boompos = pygame.Vector2(boom.rect.center)
                    self.tankpos = pygame.Vector2(tank.rect.center)
                    if self.boompos.distance_to(self.tankpos) < 100:
                        self.boomlist.append(BOOM(tank.rect.x,tank.rect.y,False))
                        if tank != self.player:
                            drop = random.randint(0,100)
                            if drop > 60:
                                self.AllPowerBoxes.add(powerbox(tank.rect.x,tank.rect.y))
                        else:
                            Menu.setmenu(30)
                        try:
                            self.EnemyTanks.remove(tank)
                            self.AllTanks.remove(tank)
                        except:
                            pass
                                
                        
                        tank.x = 9999
                        tank.y = 9999

    def CollideDetectBoomWall(self):
        for wall in self.PinkBlocks:
            for boom in self.boomlist:
                if boom.destructive:
                    self.boompos = pygame.Vector2(boom.rect.center)
                    self.wallpos = pygame.Vector2(wall[4].rect.center)
                    if self.boompos.distance_to(self.wallpos)< 100: 
                        self.wallhbot.remove(wall[0])
                        self.wallhtop.remove(wall[1])
                        self.wallvleft.remove(wall[2])
                        self.wallvright.remove(wall[3])
            
                        self.AllWalls.remove(wall[0])
                        self.AllWalls.remove(wall[1])
                        self.AllWalls.remove(wall[2])
                        self.AllWalls.remove(wall[3])
                        self.PinkBlocks.remove(wall)
                        
                        self.block_list_sprite.remove(wall[4])
                        self.remap()
    def CollideDetectBulletMine(self):
        for mine in self.mine_list:
            for bullet in self.Bullets_list:
                if bullet.is_collided_with(mine):
                    mine.boom = True
                    bullet.master.bulletsfired -=1
                    bullet.master.totalbulletsfired -=1
                    if bullet.type == 2:
                        self.boomlist.append(BOOM(bullet2.x,bullet2.y))
                    self.Bullets_list.remove(bullet)
                    
        
    def InFieldOfView(self):
        
        for tank in self.EnemyTanks:
            tank.canseeplayer = True
            tank.sightline = [list(tank.rect.center), list(self.player.rect.center)]
            for block in self.AllWalls:
                for wall in block.sightwalls:
                    #for tank2 in self.EnemyTanks:
                        #if tank != tank2:
                            viewblocked = self.line_intersection(wall, tank.sightline)
                            
                            if viewblocked: 
                                tank.canseeplayer = False
                                tank.shootwait = 0
                                break            
            tank.shootwait +=1
    def line_intersection(self, line1, line2): # do other thanks intercepting sight line
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           return False

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        
        if (line1[0][0] - line1[1][0]) < 0:
            a = line1[0][0]
            b = line1[1][0]
        else:
            a = line1[1][0]
            b = line1[0][0]
        if (line2[0][0] - line2[1][0]) < 0:
            c = line2[0][0]
            d = line2[1][0]
        else:
            c = line2[1][0]
            d = line2[0][0]



        if (line1[0][1] - line1[1][1]) < 0:
            e = line1[0][1]
            f = line1[1][1]
        else:
            e = line1[1][1]
            f = line1[0][1]
        if (line2[0][1] - line2[1][1]) < 0:
            g = line2[0][1]
            h = line2[1][1]
        else:
            g = line2[1][1]
            h = line2[0][1]
        
        if x >= a and x <= b and x >= c and x <= d:
            if y >= e and y <= f and y >= g and y <= h:
                return True
        return False


    def renderall(self):
        self.player.turret.render(self.player.rect.x, self.player.rect.y)
        for i in range(len(self.EnemyTanks)):
            self.EnemyTanks[i].turret.render(self.EnemyTanks[i].rect.x, self.EnemyTanks[i].rect.y)
        self.MoveBulletIfNes()
        self.AllPowerBoxes.draw(display_surface)
        self.hole_list_sprite.draw(display_surface)
        self.block_list_sprite.draw(display_surface)
        
        self.cursor_dots.render(self.player)
        self.playerscoreboard.render()
                
                
    def Get_Mine_List(self):
        return self.mine_list

    def Set_Mine_List(self, mines):
        self.mine_list = mines
    def astar(self,mappoints, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given mappoints"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)
        # Loop until you find the end
        while len(open_list)< 240 and len(open_list) > 0:
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)
            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(mappoints) - 1) or node_position[0] < 0 or node_position[1] > (len(mappoints[len(mappoints)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if mappoints[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)
                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)
    def remap(self):
        self.mappoints = []
        for i in range(0,17):
            self.mappoints.append([])
            for j in range(0,17):
                self.mappoints[i].append(0)
                if i == 16 or j == 16:
                    self.mappoints[i][j] = 1
        for block in self.block_list_sprite:
            self.mappoints[int(block.x/bw)][int(((block.y)/(bh/2))+1)] = 1


            
class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



class menutank:
    def __init__(self):
        self.x = -100
        self.y = 340
        self.colour = random.choice([red,green,yellow,blue,turquoise,purple,grey,brown,white,black])
        self.image1 = colourchange(pygame.image.load(os.path.join(path, r"images\playerrightfull.png")),self.colour)
        self.image2 = colourchange(pygame.image.load(os.path.join(path, r"images\playerrightfull2.png")),self.colour)
        
    def animate(self):
        self.x +=3
        if clock1.skinstate() == 1:
            screen.blit(self.image1, (self.x, self.y))
        else:
            screen.blit(self.image2, (self.x, self.y))
        if self.x > sw1:
            self.x = -100
class menu:
    def __init__(self, filename):
        self.prev = 0
        self.type = 1
        self.titleimage = pygame.transform.scale(pygame.image.load(os.path.join(path, r"images\title.png")),(sw1-80, 300))
        self.buttonlist = pygame.sprite.Group()
        self.font = pygame.font.Font(os.path.join(path, r"font1.ttf"), 20)
        self.levelid = 0
        if filename != None:
            self.filename = filename
        else:
            self.filename = "        "
    def setmenu(self,menutype, text = None):
        self.prev = self.type
        self.text = text
        self.type = menutype
        self.buttonlist = pygame.sprite.Group()
        self.menutanks = []
        
        if self.type == 1: # main menu
            
            self.clock = 0
            self.buttonlist.add(button(sw1/2 - 125,400,11,'Start'))
            self.buttonlist.add(button(sw1/2 -125 ,485,50,'Level Creator'))
            self.buttonlist.add(button(sw1/2 -125 ,570,30,'Options'))
            self.buttonlist.add(button(sw1/2 -125 ,655,4,'Quit'))
            
        elif self.type == 10: #error screen
            
            self.buttonlist.add(button(sw1/2 - 125,450,1,'Main Menu'))
            self.buttonlist.add(button(sw1/2 - 125,535,11,'Back'))
            
        elif self.type == 11: #custom level or career

            self.levelid = 0
            self.buttonlist.add(button(sw1/2 - 125,450,13,'Career'))
            self.buttonlist.add(button(sw1/2 -125 ,535,12,'Custom Level'))
            self.buttonlist.add(button(sw1/2 -125 ,620,1,'Back'))
            
        elif self.type == 12:# custom level select
            
            self.customlevels = self.getcustomlevels()
            if len(self.customlevels) == 0:
                self.setmenu(10, "No Custom Levels available !")
            else:
                for i in range(len(self.customlevels)):
                    
                    if i<7:
                        
                        self.buttonlist.add(button(sw1/2 - 385,75 + i*85,120+i,str(self.customlevels[i][:-4])))
                        
                    if i >= 7 and i <14:
                        
                        self.buttonlist.add(button(sw1/2 - 125,75 + i*85 - 7*85,120+i,str(self.customlevels[i][:-4])))
                        
                    if i >= 14 and i <21:
                        
                        self.buttonlist.add(button(sw1/2 + 135,75 + i*85 - 14*85,120+i,str(self.customlevels[i][:-4])))
                        
                self.buttonlist.add(button(sw1/2 -125 ,75 + 7*85,self.prev,'Back'))
            
        elif self.type == 30: # dead 
            
            self.buttonlist.add(button(sw1/2 - 125,450,1,'Main Menu'))
            self.buttonlist.add(button(sw1/2 -125 ,535,2,'Retry'))
            self.buttonlist.add(button(sw1/2 -125 ,620,4,'Quit'))

        elif self.type == 31: # win
            
            self.buttonlist.add(button(sw1/2 - 125,450,1,'Main Menu'))
            
        elif self.type == 50: # level creator menu
            
            self.buttonlist.add(button(sw1/2 - 125,400,55,'New'))
            self.buttonlist.add(button(sw1/2 -125 ,485,12,'Edit'))
            self.buttonlist.add(button(sw1/2 -125 ,570,1,'Back'))
            
        elif self.type == 54: # save level menu
            
            self.buttonlist.add(button(sw1/2 - 125,400,5400,'Yes'))
            self.buttonlist.add(button(sw1/2 -125 ,485,1,'No'))
            self.buttonlist.add(button(sw1/2 -125 ,570,55,'Back'))
            
        elif self.type == 5400:#text input
            
            self.buttonlist.add(button(sw1/2-335,200,5410,'^'))
            self.buttonlist.add(button(sw1/2-250,200,5411,'^'))
            self.buttonlist.add(button(sw1/2-165,200,5412,'^'))
            self.buttonlist.add(button(sw1/2-80,200,5413,'^'))
            self.buttonlist.add(button(sw1/2 + 5,200,5414,'^'))
            self.buttonlist.add(button(sw1/2 + 90,200,5415,'^'))
            self.buttonlist.add(button(sw1/2 + 175,200,5416,'^'))
            self.buttonlist.add(button(sw1/2 + 260,200,5417,'^'))
            self.buttonlist.add(button(sw1/2-335,285,5420,' '))
            self.buttonlist.add(button(sw1/2-250,285,5421,' '))
            self.buttonlist.add(button(sw1/2-165,285,5422,' '))
            self.buttonlist.add(button(sw1/2-80,285,5423,' '))
            self.buttonlist.add(button(sw1/2 + 5,285,5424,' '))
            self.buttonlist.add(button(sw1/2 + 90,285,5425,' '))
            self.buttonlist.add(button(sw1/2 + 175,285,5426,' '))
            self.buttonlist.add(button(sw1/2 + 260,285,5427,' '))
            self.buttonlist.add(button(sw1/2-335,370,5430,'v'))
            self.buttonlist.add(button(sw1/2-250,370,5431,'v'))
            self.buttonlist.add(button(sw1/2-165,370,5432,'v'))
            self.buttonlist.add(button(sw1/2-80,370,5433,'v'))
            self.buttonlist.add(button(sw1/2 + 5,370,5434,'v'))
            self.buttonlist.add(button(sw1/2 + 90,370,5435,'v'))
            self.buttonlist.add(button(sw1/2 + 175,370,5436,'v'))
            self.buttonlist.add(button(sw1/2 + 260,370,5437,'v'))
            self.buttonlist.add(button(sw1/2 - 255,455,5401,'Save'))
            self.buttonlist.add(button(sw1/2 + 5 ,455,55,'Cancel'))
            
            self.filenameinput = textinput(self.filename)
            
        elif self.type == 5401: # level save
            
            self.LevelCreator.save(self.filename)
            self.setmenu(1)
            
        elif self.type == 55: # level creator
            
            self.buttonlist.add(button(10 ,100,550,'Block'))
            self.buttonlist.add(button(10 ,185,551,'Breakable Block'))
            self.buttonlist.add(button(10 ,270,552,'Hole'))
            self.buttonlist.add(button(10 ,355,56,'Tank'))
            self.buttonlist.add(button(10 ,440,554,'Rubber'))
            self.buttonlist.add(button(10 ,525,54,'Exit / Save'))
            
        elif self.type == 56: # tank selector in level creator
            
            self.buttonlist.add(button(400 ,200,560,'Blue'))
            self.buttonlist.add(button(400 ,285,561,'Brown'))
            self.buttonlist.add(button(400 ,370,562,'Grey'))
            self.buttonlist.add(button(400 ,455,563,'Turquoise'))
            self.buttonlist.add(button(400 ,540,564,'Yellow'))
            self.buttonlist.add(button(670 ,200,565,'Red'))
            self.buttonlist.add(button(670 ,285,566,'Green'))
            self.buttonlist.add(button(670 ,370,567,'Purple'))
            self.buttonlist.add(button(670 ,455,568,'White'))
            self.buttonlist.add(button(670 ,540,569,'Black'))
            self.buttonlist.add(button(670 ,625,55,'Back'))

        elif self.type == 60: # Pause
            
            self.buttonlist.add(button(sw1/2 - 125,400,20,'Continue'))
            self.buttonlist.add(button(sw1/2 -125 ,485,2,'Retry'))
            self.buttonlist.add(button(sw1/2 -125 ,570,61,'Main Menu'))
            
        elif self.type == 61: # return to main confirm
            
            self.buttonlist.add(button(sw1/2 - 125,400,1,'Yes'))
            self.buttonlist.add(button(sw1/2 -125 ,485,60,'No'))
            
    def main(self):
        
        if self.type in [1,10,11,12,30,31,50,51,52,54,5400,55,56,60,61]:
            
            self.events = pygame.event.get()
            
            if self.type in [1]:
                
                screen.blit(self.titleimage,(40,40))
            if self.type == 1:
                
                self.clock  += 1
                if len(self.menutanks) <= 16:
                    
                    if self.clock > sw1/16/3:
                        
                        self.menutanks.append(menutank())
                        self.clock = 0
                        
                for tank in self.menutanks:
                    
                    tank.animate()
                
            if self.type in [6,60,54,56]:
                
                screen.blit(pauseframe,(gamescreenx,gamescreeny))
                
            self.buttonlist.draw(screen)
            for button in self.buttonlist:
                
                button.detectpress(self,self.events)
                
            if self.type == 30:
                self.text = "You Died !"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*24,70))
                self.textrect = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect.width/2,300))
                
            if self.type == 31:
                self.text = "You Won !"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*24,70))
                self.textrect = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect.width/2,300))
                
            if self.type//10 == 5:
                self.text = "Level Creator"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*30,75))
                self.textrect = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect.width/2,10))
                
            if self.type == 54:
                self.text = "Would you like to save your level before leaving?"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*20,50))
                self.textrect = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect.width/2,300))
                
            if self.type == 60:
                self.text = "Paused"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*30,75))
                self.textrect = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect.width/2,300))
                
            if self.type == 61:
                self.text = "Return to menu?"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*30,75))
                self.textrect1 = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect1.width/2,200))
                self.text2 = "All progress will be lost!"
                self.textimage2 = pygame.transform.scale(self.font.render(self.text2,0,(255,255,255)),(len(self.text2)*20,50))
                self.textrect2 = self.textimage2.get_rect()
                screen.blit(self.textimage2,(sw1/2 - self.textrect2.width/2,300))
                
            if self.type == 10:
                self.text1 = "Error!"
                self.textimage1 = pygame.transform.scale(self.font.render(self.text1,0,(255,255,255)),(200,75))
                self.textrect1 = self.textimage1.get_rect()
                screen.blit(self.textimage1,(sw1/2 - self.textrect1.width/2,200))
                
                self.textimage2 = pygame.transform.scale(self.font.render(self.text,0,(255,255,255)),(len(self.text)*12,30))
                self.textrect2 = self.textimage2.get_rect()
                screen.blit(self.textimage2,(sw1/2 - self.textrect2.width/2,300))
                

        
    def GetLevel(self,filename, editing = False):
        
        self.enemytanknum = 0
        self.spawnfound = False
        self.block_list = []
        self.enemy_list = []
        self.tankblock_list = []
        if filename == None or filename == 'Levels.csv':
            
            file = open(os.path.join(path, "Levels.csv"), mode='r')
            self.customlvl = False
            self.levelallowed = self.Check_Level('Levels.csv', self.levelid)
            
        else:
            
            file = open(os.path.join(path, 'Custom Levels',filename), mode='r')
            self.customlvl = True
            self.levelallowed = True
            
        if self.levelallowed:
            
            fileread = csv.reader(file)
            
            for row in fileread:

                if ('All' in row):
                    
                    self.block_list.append([int(row[2])*bw,int(row[3])*bh/2,int(row[4]),int(row[5])])    

                if ('Level'+str(self.levelid)) in row:
                    row[2] = float(row[2])
                    row[3] = float(row[3])
                    
                    if 'Wall' in row:
                        
                        self.block_list.append([int(row[2])*bw,int(row[3])*bh/2,int(row[4]),int(row[5]), 0])
                        
                    elif 'PinkWall' in row:
                        
                        self.block_list.append([int(row[2])*bw,int(row[3])*bh/2,int(row[4]),int(row[5]), 1])
                        
                    elif 'Hole' in row:
                        
                        self.block_list.append([int(row[2])*bw,int(row[3])*bh/2,int(row[4]),int(row[5]), 2])
                        
                    elif 'Spawn' in row:
                        
                        self.spawn = [int(row[2])*bw,int(row[3])*bh/2]
                        self.spawnfound = True
                        
                    elif 'Tank' in row:
                        row[6] = int(row[6])-10
                        found = False
                        if int(row[6]) == 1:
                            
                            self.colour = brown
                            self.speed = 0
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 100
                            self.shootwaitlimit = 100
                            found = True
                            
                        elif int(row[6]) == 2:
                            
                            self.colour = grey
                            self.speed = 2
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 50
                            self.shootwaitlimit = 50
                            found = True
                            
                        elif int(row[6]) == 3:
                            
                            self.colour = turquoise
                            self.speed = 2
                            self.bounce = 0
                            self.btype = 1
                            self.accuracy = 50
                            self.shootwaitlimit = 20
                            found = True
                            
                        elif int(row[6]) == 4:
                            
                            self.colour = yellow
                            self.speed = 2.5
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 100
                            self.shootwaitlimit = 50
                            found = True
                            
                        elif int(row[6]) == 5:
                            
                            self.colour = red
                            self.speed = 2
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 50
                            self.shootwaitlimit = 20
                            found = True
                            
                        elif int(row[6]) == 6:
                            
                            self.colour = green
                            self.speed = 0
                            self.bounce = 2
                            self.btype = 1
                            self.accuracy = 0
                            self.shootwaitlimit = 50
                            found = True
                            
                        elif int(row[6]) == 7:
                            
                            self.colour = purple
                            self.speed = 3
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 0
                            self.shootwaitlimit = 20
                            found = True
                            
                        elif int(row[6]) == 8:
                            
                            self.colour = white
                            self.speed = 2
                            self.bounce = 1
                            self.btype = 0
                            self.accuracy = 50
                            self.shootwaitlimit = 30
                            found = True
                            
                        elif int(row[6]) == 9:
                            
                            self.colour = black
                            self.speed = 3
                            self.bounce = 0
                            self.btype = 1
                            self.accuracy = 0
                            self.shootwaitlimit = 10
                            found = True
                            
                        if found:
                            self.tankblock_list.append([int(row[2])*bw,int(row[3])*bh/2,1,1,int(row[6])])
                            self.enemy_list.append([int(row[2])*bw,int(row[3])*bh/2,self.speed,self.colour,self.bounce,"enemy"+ str(self.enemytanknum),self.btype, self.accuracy, self.shootwaitlimit])
                            self.enemytanknum +=1
            if not editing:                
                if self.enemytanknum == 0 or self.spawnfound == False:
                    
                    self.setmenu(10,"This level is missing a spawn location and/or enemy tanks, and so cannot be played.")
                    self.enemy_list = []
                    self.block_list = []
                else:
                    self.setmenu(2)
            else:
                self.filename = "".join(list(filename[:-4])+[' ']*( 8- len(filename[:-4])))
                self.setmenu(55)

            
        file.close()
        
    def Check_Level(self, filename, levelid):
        
        found = False
        file = open(os.path.join(path,filename), mode='r')
        fileread = csv.reader(file, delimiter=',')
        
        for row in fileread:
            
            if ('Level'+str(levelid)) in row:
                
                found = True
                
                
        if not found:
            
            Menu.setmenu(31)
            self.levelid = 0
        return found

    
    def getcustomlevels(self):
        
        return os.listdir(os.path.join(path, 'Custom Levels'))

    
class button(pygame.sprite.Sprite):

    
    def __init__(self,x,y,buttontype,text):
        
        pygame.sprite.Sprite.__init__(self)
        self.type = buttontype
        self.x = x
        self.y = y
        self.text = text
        self.font = Menu.font
        
        if self.type in [550,551,552,56,554,54]:
            self.font = pygame.font.Font(os.path.join(path, r"font1.ttf"), 15)
            
        self.pos = None
        
        if self.type in [5420,5421,5422,5423,5424,5425,5426,5427]:
            self.pos = self.type - 5420
            
        self.setbutton()

        
    def setbutton(self):
        
        if self.pos != None:
            self.text = Menu.filename[self.pos]
            
        self.textimage1 = self.font.render(self.text,0,(255,255,255))
        self.textimage2 = self.font.render(self.text,0,(255,255,0))
        self.textrect = self.textimage1.get_rect()
        
        self.pressed = False
        
        self.button1 = unpressed_button
        self.button1pressed = pressed_button
        
        if self.type in [550,551,552,56,554,54]:
            
            self.button1 = pygame.transform.scale(self.button1,(int(gamescreenx) - 20, 75))
            self.button1pressed = pygame.transform.scale(self.button1pressed,(int(gamescreenx) - 20, 75))
            
        if self.type >= 5410 and self.type < 5440:
            
            self.button1 = unpressed_square_button
            self.button1pressed = pressed_square_button
            
        self.image = self.button1
        self.rect = self.button1.get_rect(topleft = (self.x,self.y))
        
    def detectpress(self,master,events):
        
        if self.pos != None:
            self.text = Menu.filename[self.pos]
            
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mousepos):
            self.pressed = True
            self.image = self.button1pressed
            
        if not pygame.mouse.get_pressed()[0] :
            
            if self.pressed and self.rect.collidepoint(mousepos):
                sounds.play(3)
                if self.type >= 550 and self.type < 560:
                   Menu.LevelCreator.setmode(self.type-550)
                   
                elif self.type >= 120 and self.type <= 141:
                    if Menu.prev == 11:
                        Menu.GetLevel(Menu.customlevels[self.type-120])
                    else:
                        Menu.GetLevel(Menu.customlevels[self.type-120],True)
                    
                else:
                    Menu.setmenu(self.type)
            self.image = self.button1
            self.pressed = False
            
        if self.rect.collidepoint(mousepos):
            screen.blit(self.textimage2,((self.rect.centerx-self.textrect.width/2,self.rect.centery-self.textrect.height/2)))
            
        else:
            screen.blit(self.textimage1,((self.rect.centerx-self.textrect.width/2,self.rect.centery-self.textrect.height/2)))

            
class levelcreator:
    
    def __init__(self):
        self.display_surface = pygame.Surface((sw,sh), pygame.SRCALPHA)
        self.pressed = False
        self.mode = 0
        self.tempobjectlist = []
        self.occlist = []
        self.block_list_sprite = pygame.sprite.Group()
        for i in range(0,18):
            self.occlist.append([])
            for j in range(0,18):
                self.occlist[i].append(0)
        if Menu.prev == 12:
            self.loadlevel()
        else:
            Menu.filename = "        "
                
    def main(self):
        self.display_surface.fill((255,255,255))
        self.block_list_sprite.draw(self.display_surface)
        
        for i in range(0,200):
            pygame.draw.line(self.display_surface,(0,255,0),[bw*i,0],[bw*i,2000],1)
            
        for i in range(0,200):
            pygame.draw.line(self.display_surface,(0,255,0),[0,bh*0.5*i],[2000,bh*0.5*i],1)
            
        self.create_object()
        screen.blit(self.display_surface,(gamescreenx,gamescreeny))
        self.pauseframe = self.display_surface
        
    def setmode(self, mode):
        self.mode = mode
        
    def loadlevel(self):
        for block in Menu.block_list:
            self.tempobjectlist.append([block[0]/bw,block[1]/(bh/2),block[2],block[3],block[4]])
        for tank in Menu.tankblock_list:
            self.tempobjectlist.append([tank[0]/bw,tank[1]/(bh/2),1,1,tank[4]+10])
        if Menu.spawnfound:
            self.tempobjectlist.append([int(Menu.spawn[0]/bw),int(Menu.spawn[1]/(bh/2)),1,1,10])
        self.refresh_blocklist()
    def create_object(self):
        if pygame.mouse.get_pressed()[0] and not self.pressed:
            self.pressed = True

            self.startx = self.current_x()
            self.starty = self.current_y()
            if self.startx > 15 or self.startx < 0 or self.starty > 15 or self.starty < 0:
                self.pressed = False
            
        if not pygame.mouse.get_pressed()[0] :
            if self.pressed:
                sounds.play(3)
                if self.mode in [0,2]:
                    self.endx = self.current_x()
                    self.endy = self.current_y()
                    if self.endx > 15 or self.endx < 0 or self.endy > 15 or self.endy < 0:
                        self.allowed = False
                    else:
                        self.allowed = True
                    if self.startx > self.endx:
                        temp = self.endx
                        self.endx = self.startx
                        self.startx = temp
                    if self.starty > self.endy:
                        temp = self.endy
                        self.endy = self.starty
                        self.starty = temp
                    if self.allowed:
                        for i in range(self.startx,self.endx+1):
                            for j in range(self.starty,self.endy+1):
                                if self.allowed:
                                    if self.occlist[i][j] == 0:
                                        self.allowed = True
                                        
                                    else:
                                        self.allowed = False
                    if self.allowed:
                        for i in range(self.startx,self.endx+1):
                            for j in range(self.starty,self.endy+1):
                                self.occlist[i][j] = 1
                        self.sizex = (self.endx-self.startx)
                        self.sizey = (self.endy-self.starty)
                        self.block = [self.startx,self.starty-1,self.sizex+1, self.sizey+1,self.mode]
                        for i in range(self.block[2]): #width
                            for j in range(self.block[3]): #height
                                new_block = Block(self.block[0]*bw+(i*bw),self.block[1]*bh/2+(j*(bh/2)),self.block[4],0)
                                self.block_list_sprite.add(new_block)
                        self.tempobjectlist.append(self.block)
                        self.tempobjectlist.sort(key =self.getblocky)
                elif self.mode >= 10:
                    
                    
                    if self.occlist[self.startx][self.starty] == 0:
                        self.occlist[self.startx][self.starty] = 1
                        self.block = [self.startx,self.starty, 1, 1,self.mode]
                        for i in range(self.block[2]): #width
                                for j in range(self.block[3]): #height
                                    new_block = Block(self.block[0]*bw+(i*bw),self.block[1]*bh/2+(j*(bh/2)),self.block[4],colours[self.mode-10])
                                    self.block_list_sprite.add(new_block)
                        self.tempobjectlist.append(self.block)
                        self.tempobjectlist.sort(key =self.getblocky)
                elif self.mode == 1:
                    if self.occlist[self.startx][self.starty] == 0:
                        
                        self.occlist[self.startx][self.starty] = 1
                        self.block = [self.startx,self.starty-1, 1, 1,self.mode]
                        for i in range(self.block[2]): #width
                                for j in range(self.block[3]): #height
                                    new_block = Block(self.block[0]*bw+(i*bw),self.block[1]*bh/2+(j*(bh/2)),self.block[4],0)
                                    self.block_list_sprite.add(new_block)
                        self.tempobjectlist.append(self.block)
                        self.tempobjectlist.sort(key =self.getblocky)
                elif self.mode == 4:
                        for block in self.tempobjectlist:
                            if block[4] >= 10:
                                if self.startx == block[0] and self.starty == block[1]:
                                    
                                    if self.occlist[self.startx][self.starty] == 1:
                                        self.occlist[self.startx][self.starty] = 0
                                        
                                        self.tempobjectlist.remove(block)
                                        self.refresh_blocklist()
                            elif block[4] == 1:
                                if self.startx == block[0] and self.starty == (block[1])+1:
                                    self.occlist[int(block[0])][int(block[1])+1] = 0
                                    self.tempobjectlist.remove(block)
                                    self.refresh_blocklist()
                            elif block[4] in [0,3]:            
                                if self.startx >= block[0] and self.startx <= block[0]+ block[2] and self.starty >= block[1]  and self.starty <= block[1]+ block[3] :
                                    for i in range(int(block[0]),int(block[0]+block[2])):
                                        for j in range(int(block[1]+1),int(block[1]+block[3]+1)):
                                            self.occlist[i][j] = 0
                                    self.tempobjectlist.remove(block)
                                    self.refresh_blocklist()
            self.pressed = False
    def getblocky(self, blist):
        return blist[1]
    def refresh_blocklist(self):
        self.block_list_sprite = pygame.sprite.Group()
        for block in self.tempobjectlist:

            if block[4] >= 10:
                new_block = Block(block[0]*bw,block[1]*bh/2,block[4],colours[block[4]-10])
                self.block_list_sprite.add(new_block)
                self.occlist[int(block[0])][int(block[1])] = 1
            else:
                for i in range(block[2]): #width
                    for j in range(block[3]): #height
                        new_block = Block(block[0]*bw+(i*bw),block[1]*bh/2+(j*(bh/2)),block[4],0)
                        self.block_list_sprite.add(new_block)
                        
                        self.occlist[int(block[0])+i][int(block[1])+j+1] = 1
    def current_x(self):
        self.x = cursorpos[0]//bw
        return int(self.x)
    def current_y(self):
        self.y = cursorpos[1]//(bh/2)
        return int(self.y)
    def get_type(self,types):
        if types > 10:
            return 'Tank'
        elif types == 10:
            return 'Spawn'
        elif types == 1:
            return 'PinkWall'
        elif types == 0:
            return 'Wall'
        elif types == 2:
            return 'Hole'
        
    def save(self, filename):
        file = open(os.path.join(path, 'Custom Levels', str(self.stripspaces(filename)) + '.csv'),'w')
        writer = csv.writer(file)
        for block in self.tempobjectlist:
            block.insert(0,'Level0')
            block.insert(1,self.get_type(block[5]))
            writer.writerow(block)
        file.close

    def stripspaces(self,text): 
        endpos = len(text) - 1
        while text[endpos] == " " and endpos > 0:
            endpos -= 1
            text = text[:-1]
        return text

class textinput:
    
    def __init__(self, text):
        self.display_surface = pygame.Surface((sw,sh), pygame.SRCALPHA)
        self.pressed = False
        self.text  = []
        for letter in list(text):
            self.text.append(ord(letter))
    def addpos(self, pos):
        self.text[pos] += 1
        for button in Menu.buttonlist:
            button.setbutton()
        self.newtext = []
        for letter in self.text:
            if letter > 122:
                letter = 32
            if letter < 97 and letter > 32:
                letter = 97
            self.newtext.append(chr(letter))
        Menu.filename = "".join(self.newtext)
        
    def takepos(self, pos):
        self.text[pos] -= 1
        for button in Menu.buttonlist:
            button.setbutton()
        self.newtext = []
        for letter in self.text:
            if letter < 97 and letter > 32:
                letter = 32
            if letter < 32:
                letter = 122
            self.newtext.append(chr(letter))
        Menu.filename = "".join(self.newtext)


class Sound:
    def __init__(self):
        try:
            self.boom = pygame.mixer.Sound(os.path.join(path, 'Sounds', 'boom.wav')) #explosion
            self.dieboom = pygame.mixer.Sound(os.path.join(path, 'Sounds', 'death.wav')) # explosion when player dies
            self.pap = pygame.mixer.Sound(os.path.join(path, 'Sounds', 'shoot.wav')) # when a bullet is fired
            self.pop = pygame.mixer.Sound(os.path.join(path, 'Sounds', 'bounce.wav')) # when a bullet bounces or collides with another bullet
            self.trundle = pygame.mixer.Sound(os.path.join(path, 'Sounds', 'trundle.wav')) # tanks moving
            self.sounds = [self.boom,self.dieboom,self.pap,self.pop,self.trundle]
        except:
            pass

    def play(self, sound):
        try:
            self.sounds[sound].play()
        except:
            pass
        




import cProfile
pr = cProfile.Profile()
pr.enable()


    
Menu = menu(None)
sounds = Sound()
Menu.setmenu(1)
gamestarted = False
editoropen = False
display_surface = pygame.Surface((sw,sh))
clock2 = pygame.time.Clock()
clock1 = clock()
pygame.mouse.set_visible(False)
cursor1 = cursor()
darkoverlay = pygame.Surface((sw,sh),pygame.SRCALPHA)
darkoverlay.fill((100,100,100,0))


while True:

    clock1.increment()
    mousepos = pygame.mouse.get_pos() # in relation to big
    cursorpos = [mousepos[0]-gamescreenx, mousepos[1]-gamescreeny]
    
    
        
    pressed = list(pygame.key.get_pressed())
    if Menu.type in [1,10,11,12,30,31,50]:
        editoropen = False
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
    elif Menu.type == 13:
        editoropen = False
        gamestarted = False
        screen.blit(background,(0,0))
        #load csv and check for user files
        #store file name is list
        #if userfiles give option to load them in gui
        Menu.GetLevel('Levels.csv')
        Menu.type = 21
    elif Menu.type == 2:
        editoropen = False
        gamestarted = False
        screen.blit(background,(0,0))
        #load csv and check for user files
        #store file name is list
        #if userfiles give option to load them in gui

        Menu.type = 21
    elif Menu.type == 21:
        editoropen = False
        gamestarted = True
        screen.blit(background,(0,0))
        
        GameMec = game()
        Menu.type = 0
    elif Menu.type == 20:
        editoropen = False
        gamestarted = True
        screen.blit(background,(0,0))

        Menu.type = 0
    elif Menu.type//10 == 6:
        editoropen = False
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
    elif Menu.type == 54:
        editoropen = True
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
    elif Menu.type == 5400:
        editoropen = True
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
    elif Menu.type >= 5410 and Menu.type < 5420:
        Menu.filenameinput.addpos(Menu.type-5410)
        Menu.setmenu(5400)
    elif Menu.type >= 5420 and Menu.type < 5430:
        Menu.setmenu(5400)    
    elif Menu.type >= 5430 and Menu.type < 5440:
        Menu.filenameinput.takepos(Menu.type-5430)
        Menu.setmenu(5400)
    elif Menu.type == 55:
        if editoropen == False:
                Menu.LevelCreator = levelcreator()
                editoropen = True
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.LevelCreator.main()
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
        pauseframe = Menu.LevelCreator.pauseframe
        pauseframe.blit(darkoverlay,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
    elif Menu.type == 56:
        editoropen = True
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        cursor1.render(mousepos[0],mousepos[1])
    elif Menu.type >= 560 and Menu.type < 570:
        editoropen = True
        gamestarted = False
        screen.blit(background,(0,0))
        Menu.main()
        Menu.LevelCreator.setmode(Menu.type-550)
        cursor1.render(mousepos[0],mousepos[1])
        Menu.setmenu(55)
    elif Menu.type == 4:
        pygame.quit()
        pr.disable()
        pr.print_stats(sort='time')
        quit()



    
    if gamestarted:
        GameMec.main()
        pauseframe = display_surface
        pauseframe.blit(darkoverlay,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
    #time.sleep(0)
    for event in pygame.event.get() :  
        
        if event.type == pygame.QUIT : 
            pygame.quit() 
            quit()
    
    
    pygame.display.flip()
    clock2.tick(60)

