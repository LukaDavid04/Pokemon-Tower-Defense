from math import *
from pygame import *
import pygame.gfxdraw as gfxdraw
from random import *
from tkinter import *
import os, pickle, threading, itertools

#--------------------Setup--------------------#

font.init()
comicFont=font.SysFont("Power Clean", 20)
levelFont=font.SysFont("Power Clean",30)
mixer.pre_init(44100, -16, 1, 512)
mixer.init()
init()
w,h = 700,650
os.environ['SDL_VIDEO_WINDOW_POS'] = '525,25'
screen=display.set_mode((w,h))
screenRect = screen.get_rect()

#--------------------Colours--------------------#

RED=(255,0,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BABYBLUE=(0,191,255)
ORANGE=(255,140,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(222,222,222)
PINK=(255,100,100)

enemy_colors = [RED, BLUE, GREEN, PINK, YELLOW]

#--------------------Music--------------------#

index=0                                                 ## Index number for the background song playlist
BSG1="audio/JME.mp3"                                    ## Background songs
BSG2="audio/PokeTheme.mp3"
#BSG3="audio/SickBeats.mp3"
#BSG4="audio/Stormzy_Shut-Up.mp3"
# BSG5="audio/"
# BSG6="audio/"
# BSG7="audio/"
BackGPlaylist=[]                                        ## Playlist for background music
BackGPlaylist.append(BSG1)                              ## Adding the songs to the playlist
BackGPlaylist.append(BSG2)
#BackGPlaylist.append(BSG3)
#BackGPlaylist.append(BSG4)
# BackGPlaylist.append(BSG5)
# BackGPlaylist.append(BSG6)
# BackGPlaylist.append(BSG7)
shuffle(BackGPlaylist)                                  ## Shuffles the songs in the playlist
song=BackGPlaylist[index]                               ## Lining up the index with the shuffled songs
#mixer.music.load(song)                                  ## Loading and playing of the background music

END_MUSIC_EVENT=USEREVENT+0                             ## Ends the background music
mixer.music.set_endevent(END_MUSIC_EVENT)

#--------------------Convenience---------------------#

MONEY=0
HP=1
MP=2

#--------------------Map points--------------------#

Map1Points=[[0,87],[162,87],[162,320],[420,320],[420,165],[628,165],[628,315]] #Points on the map where the enemies turn 
Map2Points=[[40,110],[40,220],[235,220],[235,430],[647,430],[647,165]]
Map3Points=[[223,0],[223,480],[615,480],[615,175]]
startR=False

mPoints=[Map1Points,Map2Points,Map3Points]

#--------------------Map 1 enemy waves--------------------#

RDMP1E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,48],[75,55],[80,65],[90,68],[100,72],[100,80],[110,80],[1,1000]]
RDMP1M=[[20,10],[25,15],[40,20],[40,25],[50,30],[60,38],[60,42],[65,45],[75,52],[80,64],[95,68],[110,72],[110,80],[110,90],[1,1000]]
RDMP1H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
nextRD=[RDMP1E,RDMP1M,RDMP1H]

#--------------------Map 2 enemy waves--------------------#

RDMP2E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,48],[75,55],[80,65],[90,68],[100,72],[100,80],[110,80],[1,1000]]
RDMP2M=[[20,10],[25,15],[40,20],[40,25],[50,30],[60,38],[60,42],[65,45],[75,52],[80,64],[95,68],[110,72],[110,80],[110,90],[1,1000]]
RDMP2H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
nextRD2=[RDMP2E,RDMP2M,RDMP2H]

#--------------------Map 3 enemy waves--------------------#

RDMP3E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,48],[75,55],[80,65],[90,68],[100,72],[100,80],[110,80],[1,1000]]
RDMP3M=[[20,10],[25,15],[40,20],[40,25],[50,30],[60,38],[60,42],[65,45],[75,52],[80,64],[95,68],[110,72],[110,80],[110,90],[1,1000]]
RDMP3H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
nextRD3=[RDMP3E,RDMP3M,RDMP3H]

#--------------------List of enemy waves of all maps--------------------#

Next=[nextRD,nextRD2,nextRD3]


#--------------------Varaibles for selected map--------------------#

money=0
hp=0
mp=0

#--------------------Different resource values for difficulty levels--------------------#

MapOneInGamesE=[500,100,0]
MapOneInGamesM=[550,80,0]
MapOneInGamesH=[650,50,0]
MP1inGames=[MapOneInGamesE,MapOneInGamesM,MapOneInGamesH]

MapTwoInGamesE=[500,100,0]
MapTwoInGamesM=[550,70,0]
MapTwoInGamesH=[650,40,0]
MP2inGames=[MapTwoInGamesE,MapTwoInGamesM,MapTwoInGamesH]

MapThreeInGamesE=[700,100,0]
MapThreeInGamesM=[650,50,0]
MapThreeInGamesH=[600,20,0]
MP3inGames=[MapThreeInGamesE,MapThreeInGamesM,MapThreeInGamesH]

#--------------------Inactive enemies--------------------#

WAITenemies=[]
dex=0   # index for the wave function
lvl=0

#--------------------Pokeball loading gif--------------------#

loadingPics = []

for i in range(30):
    pic = image.load('Gif tings/frame_' + str(i) + '_delay-0.03s.png')
    loadingPics.append(transform.scale(pic, (pic.get_width()//2, pic.get_height()//2)))

def loadingAnimation(): 
    # Itertools makes the for loop run infinitly
    for c in itertools.cycle(loadingPics):
        if doneLoading:
            break
        screen.fill(WHITE)
        tmpRect = c.get_rect()
        tmpRect.center = w - 100, h - 100
        screen.blit(c, tmpRect)
        display.flip()
        time.wait(20)

#--------------------Load images into program while gif is running--------------------#

def loadImages():
    global MapGood, MapOneMask, MapGood2, MapTwoMask, PKBack, PKLogo, PKTLogo, base1, startpic
    global startHOVER, optionspic, optionsHOVER, Psy, back, backHOVER, knowhow, knowhowHOVER, play, nextS, sounds, pokeball, roundGO, b1, s1, c1
    global bu1, p1, pi1, lvlscreen, MapGood3, MapThreeMask , base2, base3, instructions, victory

    #--------------------Map images--------------------#

    MapGood=image.load("maps/MapGood1.png").convert()
    MapOneMask=image.load("maps/Mask1.png") 

    MapGood2=image.load("maps/MapGood2.png").convert()
    MapTwoMask=image.load("maps/Mask2.png")

    MapGood3=image.load("maps/MapGood3.png").convert()
    MapThreeMask=image.load("maps/Mask3.png")

    #--------------------Menu screen images--------------------#

    PKBack=image.load("images/load.jpg").convert_alpha()
    PKBack=transform.scale(PKBack,(700,466))
    PKLogo=image.load("images/pokemonlogo.png").convert_alpha()
    PKLogo=transform.scale(PKLogo,(500,184))
    PKTLogo=image.load("images/logoTD.png").convert_alpha()

    base1=image.load("images/base.png").convert_alpha()
    base2=image.load("images/base2.png").convert_alpha()
    base3=image.load("images/base3.png").convert_alpha()

    startpic=image.load("images/start_load.png").convert_alpha()
    startHOVER=image.load("images/hoverSTART.png").convert_alpha()
    optionspic=image.load("images/options.png").convert_alpha()
    optionsHOVER=image.load("images/hoverOPTIONS.png").convert_alpha()

    Psy=image.load("images/psy.jpg").convert_alpha()
    back=image.load("images/back.png").convert_alpha()
    backHOVER=image.load("images/hoverBACK.png").convert_alpha()
    knowhow=image.load("images/instructBUT.png").convert_alpha()
    knowhowHOVER=image.load("images/hoverINSTRUCT.png").convert_alpha()

    play=image.load("images/play.png").convert_alpha()
    play=transform.scale(play,(70,70))
    nextS=image.load("images/ff.png").convert_alpha()
    nextS=transform.scale(nextS,(70,70))
    sounds=image.load("images/sounds.png").convert_alpha()
    sounds=transform.scale(sounds,(115,115))

    #--------------------Game screen images------------------#

    pokeball=image.load("images/pokeball.png")
    pokeball=transform.scale(pokeball,(50,50)).convert_alpha()
    roundGO=image.load("images/round.png")

    b1 = image.load("images/bulba.png")
    b1 = transform.scale(b1,(45,45))
    s1 = image.load("images/squir.png")
    s1 = transform.scale(s1,(45,45))
    c1 = image.load("images/charmander.png")
    c1 = transform.scale(c1,(45,45))
    bu1 = image.load("images/butter.png")
    bu1 = transform.scale(bu1,(45,45))
    p1 = image.load("images/pika.png")
    p1 = transform.scale(p1,(45,45))
    pi1 = image.load("images/pidge.png")
    pi1 = transform.scale(pi1,(45,45))

    lvlscreen=image.load("images/lvlscreen.jpg")
    instructions=image.load("images/instruction.png")
    victory=image.load("images/LaFin.jpg")
    time.wait(2000)                 # so the user can see the loading animation

#---------------------Threading---------------------#

# https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
doneLoading = False
l = threading.Thread(target=loadImages)
l.start()
t = threading.Thread(target=loadingAnimation)
t.start()
while not doneLoading:
    if not l.isAlive():
        doneLoading = True

#--------------------Pictures of maps, masks, and backgrounds-------------------#   

Maps=[MapGood,MapGood2,MapGood3]
Masks=[MapOneMask,MapTwoMask,MapThreeMask]
Bases=[base1,base2,base3]

#--------------------Selected tower--------------------#

selected_tower = None

#-------------------Tower sprites-------------------------#

CharPics=[]
for i in range(2):
    CharPics.append(image.load("images/char/"+str(i)+".png"))

CharPics2=[]
for i in range(2):
    CharPics2.append(image.load("images/char2/"+str(i)+".png"))

CharPics3=[]
for i in range(2):
    CharPics3.append(image.load("images/char3/"+str(i)+".png"))

BulbPics=[]
for i in range(2):
    BulbPics.append(image.load("images/bulb/"+str(i)+".png"))

BulbPics2=[]
for i in range(2):
    BulbPics2.append(image.load("images/bulb2/"+str(i)+".png"))

BulbPics3=[]
for i in range(2):
    BulbPics3.append(image.load("images/bulb3/"+str(i)+".png"))

SquirtPics=[]
for i in range(2):
    SquirtPics.append(image.load("images/squirt/"+str(i)+".png"))

SquirtPics2=[]
for i in range(2):
    SquirtPics2.append(image.load("images/squirt2/"+str(i)+".png"))

SquirtPics3=[]
for i in range(2):
    SquirtPics3.append(image.load("images/squirt3/"+str(i)+".png"))

PidgePics=[]
for i in range(2):
    PidgePics.append(image.load("images/pidge/"+str(i)+".png"))

PidgePics2=[]
for i in range(2):
    PidgePics2.append(image.load("images/pidge2/"+str(i)+".png"))

PidgePics3=[]
for i in range(2):
    PidgePics3.append(image.load("images/pidge3/"+str(i)+".png"))

PikaPics=[]
for i in range(2):
    PikaPics.append(image.load("images/pika/"+str(i)+".png"))

PikaPics2=[]
for i in range(2):
    PikaPics2.append(image.load("images/pika2/"+str(i)+".png"))

ButterPics=[]
for i in range(2):
    ButterPics.append(image.load("images/butter/"+str(i)+".png"))

ButterPics2=[]
for i in range(2):
    ButterPics2.append(image.load("images/butter2/"+str(i)+".png"))

#--------------------Enemy sprites--------------------#

RatatPics=[]
for i in range(2):
    RatatPics.append(transform.flip(image.load("images/ratat/"+str(i)+".png"), True, False))

RatatPics2=[]
for i in range(2):
    RatatPics2.append(transform.flip(image.load("images/ratat2/"+str(i)+".png"), True, False))

EkansPics=[]
for i in range(2):
    EkansPics.append(transform.flip(image.load("images/ekans/"+str(i)+".png"), True, False))

#--------------------Attack sprites--------------------#

FirePics=[]
for i in range(5):
    FirePics.append(transform.scale(image.load("images/fire/"+str(i)+".png"),(20,20)))

WaterPics=[]
WaterPics.append(transform.scale(image.load("images/waterball.png"),(20,20)))
for i in range(0,360,20):
    WaterPics.append(transform.rotate(WaterPics[0],i))

TornadoPics=[]
for i in range(6):
     TornadoPics.append(transform.scale(image.load("images/tornado/"+str(i)+".png"),(30,30)))

LeafPics=[]
LeafPics.append(transform.scale(image.load("images/leaf.png"),(20,20)))
for i in range(0,360,20):
    LeafPics.append(transform.rotate(LeafPics[0],i))

PowderPics=[]
for i in range(10):
    PowderPics.append(transform.scale(image.load("images/powder/"+str(i)+".png"),(100,100)))

BoltPics=[]
BoltPics.append(transform.scale(image.load("images/bolt.png"),(20,20)))
for i in range(0,360,20):
    BoltPics.append(transform.rotate(BoltPics[0],i))

#################### ALL OF THE FUNCTIONS ####################

#---------------------Wave generator--------------------#

def wave(num,health):
    for i in range(num): #number of waves
        CurrentMapPoints=mPoints[mapchoice]
        WAITenemies.append(enemy(CurrentMapPoints[0],health,5))
        waveRD=num

#-----------------------Shot mechanics and animations------------------------#

class shot: #shot class

    def __init__(self,x,y,vx,vy,kind): #init function only runs once
        self.x,self.y=x,y #position
        self.vx,self.vy=vx,vy #velocity
        self.image=Surface((6,6),SRCALPHA) #surface to draw the shot on
        self.image.fill((255,255,255,0)) #needs a f
        self.rect=self.image.get_rect() #need a rectangle to check collision
        self.frameDelay=10 
        self.frame=0
        self.kind=kind

    def animate(self):
        
        if self.kind=="CHAR":
            screen.blit(FirePics[self.frame],self.rect)
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
            self.frame+=1
            if self.frame==5: 
                self.frame=0

        if self.kind=="SQUIRT":
            screen.blit(WaterPics[self.frame],self.rect)
            self.frameDelay-=1
            if self.frameDelay==0:
                self.frameDelay=10
            self.frame+=1
            if self.frame==len(WaterPics)-1: 
                self.frame=0

        if self.kind=="BULBA":
            screen.blit(LeafPics[self.frame],self.rect)
            self.frameDelay-=1
            if self.frameDelay==0:
                self.frameDelay=10
            self.frame+=1
            if self.frame==len(LeafPics)-1: 
                self.frame=0

        if self.kind=="BUTTER":
            screen.blit(PowderPics[self.frame],self.rect)
            self.frameDelay-=1
            if self.frameDelay==0:
                self.frameDelay=10
            self.frame+=1
            if self.frame==10: 
                self.frame=0

        if self.kind=="PIKA":
            screen.blit(BoltPics[self.frame],self.rect)
            self.frameDelay-=1
            if self.frameDelay==0:
                self.frameDelay=10
            self.frame+=1
            if self.frame==len(BoltPics)-1:
                self.frame=0

        if self.kind=="PIDGE":
            screen.blit(TornadoPics[self.frame],self.rect)
            self.frameDelay-=1
            if self.frameDelay==0:
                self.frameDelay=10
            self.frame+=1
            if self.frame==6: 
                self.frame=0

    def move(self):
        self.x+=self.vx
        self.y+=self.vy
        self.rect.center=self.x,self.y
        screen.blit(self.image,self.rect)
        if not screenRect.colliderect(self.rect): #if the shot leaves the screen
            shots.remove(self)

    def is_collided_with(self,bads): #is used to delete the shot once it collides with the enemy
        for i in bads:
            if self.rect.colliderect(i.rect): #http://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
                return i  #returns the enemy the shot collided with

        return False
  
#--------------------Fade effect---------------------#

def black(screenCopy):
    alphaSurf = Surface((w, h), SRCALPHA)
    for i in range(0, 256, 2):
        screen.blit(screenCopy, (0,0))
        alphaSurf.fill((0,0,0,i))
        screen.blit(alphaSurf, (0,0))
        display.flip()

#--------------------Tower mechanics--------------------#

class tower:
    def __init__(self,pos,area,damage,kind):
        self.placex,self.placey=pos
        self.radius=area #area they can shoot
        self.damage=damage #damage each tower deals
        self.kind=kind #which pokemon
        self.image=c1
        self.rect=self.image.get_rect()
        self.rect.center=self.placex,self.placey
        self.target_enemy=None
        self.evolution=1
        self.frameDelay=10
        self.frame=0
        self.attackDelay=9
        self.attackCounter=0
        self.target="first"

    #--------------------Finding distance between enemy and tower--------------------#

    def findClose(self,enemies):
        BadDist=[]
        for e in enemies:
            self.dist=hypot(self.rect.centerx-e.placex,self.rect.centery-e.placey) #distance between enemy and tower
            BadDist.append(self.dist) #list of all the distances

        if len(BadDist)>0: #avoids checking the min of an empty list
            if min(BadDist)<=self.radius: #closest enemy needs to be in the tower range
                close_enemy=enemies[BadDist.index(min(BadDist))] #works cause the lists are related
                return close_enemy
        return None

    #---------------------First enemy in line--------------------#

    def findFirst(self,enemies):
        for e in enemies:
            if hypot(self.rect.centerx-e.placex,self.rect.centery-e.placey)<=self.radius:
                return e

    #--------------------Strongest enemy---------------------#

    def findStrong(self,enemies):
        healthList=[]
        for e in enemies:
            if hypot(self.rect.centerx-e.placex,self.rect.centery-e.placey)<=self.radius: #finds the health of enemies within range
                healthList.append(e.health)
        if len(healthList)>0:
            strongest=max(healthList) #finds the enemy with the greatest health
            for i in enemies:
                if i.health==strongest:
                    return i    

    #---------------------Shooting--------------------#
                    
    def attack(self,enemies):

        if self.target == "close":
            self.target_enemy=self.findClose(enemies) #need the self because you defined the function in the class

        elif self.target == "first":
            self.target_enemy=self.findFirst(enemies)  

        elif self.target=="strong":
            self.target_enemy=self.findStrong(enemies)    

        if self.evolution==2: #radius size increases after upgrading
            self.radius=150

        if self.evolution==3:
            self.radius=200

        if self.target_enemy!=None: #controls rate of attack
            self.attackDelay-=1

            if self.target_enemy.health>0: #only attacks the enemy if its "alive"
                speed = 10
                angle=atan2(self.target_enemy.placey-self.placey,self.target_enemy.placex-self.placex) #angle between the close enemy and the tower

                #--------------------Attacks of different Pokemon--------------------#

                if self.kind=="CHAR":
                    if self.attackDelay==0:
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"CHAR")) #shoots by adding a shot to the shots set
                        self.target_enemy.health-=self.damage #does damage

                if self.kind=="PIDGE":
                    if self.attackDelay==0:
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"PIDGE"))
                        self.target_enemy.health-=self.damage

                if self.kind=="PIKA":
                    if self.attackDelay == 0:
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"PIKA"))
                        self.target_enemy.health-=self.damage

                if self.kind=="SQUIRT":
                    if self.attackDelay==0:
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"SQUIRT"))
                        self.target_enemy.health-=self.damage

                if self.kind=="BULBA":
                    if self.attackDelay==0:
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"BULBA"))
                        self.target_enemy.health-=self.damage

                if self.kind=="BUTTER":
                    if self.attackDelay==0:
                        print(self.target_enemy.speed)
                        self.target_enemy.speed-=1 #reduces enemy speed
                        if self.target_enemy.speed<=2:
                            self.target_enemy.speed=2
                        shots.append(shot(self.rect.centerx,self.rect.centery,cos(angle)*speed,sin(angle)*speed,"BUTTER"))
                        
            #---------------------Controls rate of attack--------------------#                

            if self.attackDelay <= 0:
                if self.evolution==2:
                    self.attackDelay=6
                if self.evolution==3:
                    self.attackDelay=3
                else:
                    self.attackDelay=8

        #--------------------Upgrading animations--------------------#

        if self.kind=="CHAR":
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0
            if self.evolution==1:
                self.image=CharPics[self.frame]
            if self.evolution==2:
                self.image=CharPics2[self.frame]
            if self.evolution==3:
                self.image=CharPics3[self.frame]

            ###???

            if self.target_enemy != None and self.rect.centerx < self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)

            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)

        if self.kind=="SQUIRT":

            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0
            if self.evolution==1:
                self.image=SquirtPics[self.frame]
            if self.evolution==2:
                self.image=SquirtPics2[self.frame]
            if self.evolution==3:
                self.image=SquirtPics3[self.frame]

            if self.target_enemy != None and self.rect.centerx < self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)

            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)  

        if self.kind=="PIDGE":
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0

            if self.evolution==1:
                self.image=PidgePics[self.frame]
            if self.evolution==2:
                self.image=PidgePics2[self.frame]
            if self.evolution==3:
                self.image=PidgePics3[self.frame]

            if self.target_enemy != None and self.rect.centerx < self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)
            
            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)  

        if self.kind=="BULBA":
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0

            if self.evolution==1:
                self.image=BulbPics[self.frame]
            if self.evolution==2:
                self.image=BulbPics2[self.frame]
            if self.evolution==3:
                self.image=BulbPics3[self.frame]

            if self.target_enemy != None and self.rect.centerx < self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)

            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)

        if self.kind=="BUTTER":
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0

            if self.evolution==1:
                self.image=ButterPics[self.frame]
            if self.evolution>=2:
                self.image=ButterPics2[self.frame]

            if self.target_enemy != None and self.rect.centerx > self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)

            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)  
            
        if self.kind=="PIKA":
            self.frameDelay-=1                         # count down to zero
            if self.frameDelay==0:                     # then advance frame like normal
                self.frameDelay=10
                self.frame+=1
                if self.frame==2: 
                    self.frame=0

            if self.evolution==1:
                self.image=PikaPics[self.frame]

            if self.evolution>=2:
                self.image=PikaPics2[self.frame]

            if self.target_enemy != None and self.rect.centerx < self.target_enemy.rect.centerx:
                self.image = transform.flip(self.image, True, False)

            self.rect=self.image.get_rect()
            self.rect.center=self.placex,self.placey
            screen.blit(self.image, self.rect)  

#--------------------Enemy class--------------------#

class enemy:

    def __init__(self,pos,health,speed): #enemy class, you need to put the location and health 
        self.placex,self.placey=pos #pass the location when you call the function
        self.health=health #how much health each individual enemy has
        self.total_health=health
        self.dx,self.dy=0,0
        self.seg=0
        self.evolution=1
        self.frameDelay=10
        self.frame=0
        self.speed=speed
        if self.health<=10:
            self.images = RatatPics
        elif self.health<= 20:
            self.images = RatatPics2
        else:
            self.images = EkansPics

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    #---------------------Finds the path the enemies follow based on given points--------------------#

    def findPath(self,path):
        global hp
        self.path=path
        x2=self.path[self.seg][0]
        y2=self.path[self.seg][1]
        dist=hypot(self.placex-x2,self.placey-y2)
        if dist<=3 and self.seg<len(self.path)-1:
            self.seg+=1
        if dist<=1 and self.path[self.seg] == self.path[-1]:
            bads.remove(self)
            hp-=1
        dist=max(1,dist)
        self.dx=self.speed*(x2-self.placex)/dist
        self.dy=self.speed*(y2-self.placey)/dist

    #--------------------Draws enemies--------------------#

    def draw(self):
        global mPoints, mapchoice
        self.CurrentMapPoints=mPoints[mapchoice]
        self.findPath(self.CurrentMapPoints)
        self.placex+=self.dx #movement
        self.placey+=self.dy #movement

        self.frameDelay-=1                         # count down to zero
        if self.frameDelay==0:                     # then advance frame like normal
            self.frameDelay=10
            self.frame+=1
            if self.frame==2: 
                self.frame=0

        self.image = self.images[self.frame]
        self.rect.center=self.placex,self.placey #centers image

        self.rect = self.image.get_rect()
        self.rect.center = self.placex, self.placey
        screen.blit(self.image,self.rect)
        draw.rect(screen,GREEN,(self.rect.x,self.rect.bottom+20,self.rect.width/self.total_health*self.health,10)) #HP bar

#--------------------List of active shots-------------------#

shots=[]

#--------------------List of active enemies--------------------#

bads=[]

#--------------------More setup--------------------#

unleash=0 #controls the unleashing of enemy waves (is the number of ticks when the user clicks the round start button)
offset=0 #scrolling offset on level select screen
mapchoice=0 #which map is chosen
roundFIN=0 #used for giving money each round
roundFINCASH=300 #amount of money given each round
paused = False
towers=[]
#mixer.music.play()
if paused:
    mixer.music.pause()

running = True
mode = "Menu Screen"
tool = "none"
optionRET = "Load" # Flag for whether the user will return to the game or load screen
MapOneRect = draw.rect(screen,GREEN,(0,0,700,500))

clock=time.Clock()
roundSTART=0
ticTok = time.Clock()

#--------------------WHILE RUNNING LOOP--------------------#

while running:
    click = False
    for evt in event.get():
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button == 1:
                click = True
            if evt.button == 4: #scroll down
                if mode == "levels":
                    offset-= 40
            if evt.button == 5: #scroll up 
                if mode == "levels":
                    offset+= 40  
        if evt.type==KEYDOWN:
            if evt.key==K_ESCAPE:
                if mode == 'Game Mode 1' and tool!='none':
                    tool = 'none'
                else:
                    running=False
        if evt.type==END_MUSIC_EVENT and evt.code==0:       ## Stops the music
            index+=1
            if index==len(BackGPlaylist):                   ## Resets the playlist
                index=0
            song=BackGPlaylist[index]
            mixer.music.load(song)
            mixer.music.play()
        if evt.type==QUIT:
            running=False

    mx,my=mouse.get_pos()
    mb   =mouse.get_pressed()
    
    screen.fill(0)
    t=time.get_ticks()-unleash

    #--------------------Menu screen--------------------#

    if mode == "Menu Screen":
        screen.fill(WHITE)
        screen.blit(PKBack,(0,114))
        screen.blit(PKLogo,(100,5))
        screen.blit(PKTLogo,(180,160))

        START=screen.blit(startpic,(20,530))
        OPTIONS=screen.blit(optionspic,(360,530))

        if START.collidepoint(mx,my): 
            screen.blit(startHOVER,(20,530))
            if click:
                mode = "levels"

        if OPTIONS.collidepoint(mx,my):
            screen.blit(optionsHOVER,(360,530))
            if click:
                mode = "Options Mode 1"

    #--------------------Level selection screen--------------------#

    elif mode == "levels":
        if offset < 0:
            offset = 0 #doesn't scroll past the picture
        if offset > 1275:
            offset = 1275 #doesn't scroll past the picture

        screen.blit(lvlscreen,(0-offset,0))

        tool = "none"

        #--------------------Difficulty selection buttons--------------------#

        easy=levelFont.render("Easy",True,(BLACK))
        med=levelFont.render("Medium",True,(BLACK))
        hard=levelFont.render("Hard",True,(BLACK))

        lvls=draw.rect(screen,YELLOW,(250-offset,450,200,50))
        screen.blit(easy,(328-offset,465,200,50))

        lvls2=draw.rect(screen,ORANGE,(250-offset,510,200,50))
        screen.blit(med,(314-offset,525,200,50))

        lvls3=draw.rect(screen,RED,(250-offset,570,200,50))
        screen.blit(hard,(328-offset,585,200,50))

        M2lvls=draw.rect(screen,YELLOW,(900-offset,450,200,50))
        screen.blit(easy,(978-offset,465,200,50))

        M2lvls2=draw.rect(screen,ORANGE,(900-offset,510,200,50))
        screen.blit(med,(964-offset,525,200,50))

        M2lvls3=draw.rect(screen,RED,(900-offset,570,200,50))
        screen.blit(hard,(978-offset,585,200,50))

        M3lvls=draw.rect(screen,YELLOW,(1530-offset,450,200,50))
        screen.blit(easy,(1608-offset,465,200,50))

        M3lvls2=draw.rect(screen,ORANGE,(1530-offset,510,200,50))
        screen.blit(med,(1594-offset,525,200,50))

        M3lvls3=draw.rect(screen,RED,(1530-offset,570,200,50))
        screen.blit(hard,(1608-offset,585,200,50))

        #--------------------Level selection--------------------#

        if lvls.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=0
            mapchoice=0
            CURRENTIG = MP1inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]



        if lvls2.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=1
            mapchoice=0
            CURRENTIG = MP1inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]


        if lvls3.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=2
            mapchoice=0
            CURRENTIG = MP1inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]


        if M2lvls.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=0
            mapchoice=1
            CURRENTIG = MP2inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

        if M2lvls2.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=1
            mapchoice=1
            CURRENTIG = MP2inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

        if M2lvls3.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=2
            mapchoice=1
            CURRENTIG = MP2inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

        if M3lvls.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=0
            mapchoice=2
            CURRENTIG = MP3inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

        if M3lvls2.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=1
            mapchoice=2
            CURRENTIG = MP3inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

        if M3lvls3.collidepoint(mx,my) and click:
            mode="Game Mode 1"
            lvl=2
            mapchoice=2
            CURRENTIG = MP3inGames[lvl]
            money=CURRENTIG[MONEY]
            hp=CURRENTIG[HP]
            mp=CURRENTIG[MP]

    #--------------------Options menu--------------------#

    elif mode == "Options Mode 1":
        tool = "none"
        screen.fill(WHITE)
        screen.blit(Psy,(120,50))
        backrect=screen.blit(back,(490,10))
        playR=screen.blit(play,(20,50))
        nextR=screen.blit(nextS,(100,50))
        instructo=screen.blit(knowhow,(35,130))
        screen.blit(sounds,(160,27))

        if instructo.collidepoint(mx,my):
            screen.blit(knowhowHOVER,(35,130))
            if click:
                mode = "Instruction screen"
        
        if backrect.collidepoint(mx,my):
            screen.blit(backHOVER,(490,10))
            if click:
                if optionRET == "Load": 
                    mode = "Menu Screen"
                if optionRET == "Game":
                    mode = "Game Mode 1"

        if nextR.collidepoint(mx,my) and click:
            index+=1 #next song
            if index==len(BackGPlaylist):
                index=0
                song=BackGPlaylist[index]
                mixer.music.load(song)
                mixer.music.play()
            song=BackGPlaylist[index]
            mixer.music.load(song)
            mixer.music.play()

        if playR.collidepoint(mx,my) and click:
            if paused==True:
                mixer.music.unpause()
                paused=False
            elif paused==False:
                mixer.music.pause()
                ped=True

    #--------------------Instructions screen--------------------#

    elif mode == "Instruction screen":
        screen.fill(WHITE)
        screen.blit(instructions,(0,0))
        backrect2=screen.blit(back,(490,10))
        if backrect2.collidepoint(mx,my):
            screen.blit(backHOVER,(490,10))
            if click:
                mode = "Options Mode 1"

    #--------------------Actual gameplay--------------------#

    elif mode == "Game Mode 1":

        optionRET = "Game"

        CurrentMap=Maps[mapchoice]
        CurrentMask=Masks[mapchoice]
        CurrentBase=Bases[mapchoice]
        nextRDS=Next[mapchoice]
        OrigLength=Next[mapchoice]

        screen.blit(CurrentMap,(0,0))
        screen.blit(CurrentBase,(0,512))

        #--------------------In-game menu graphics--------------------#

        BULBA = screen.blit(pokeball,(20,520))
        screen.blit(b1,(22,522))
        SQUIRT = screen.blit(pokeball,(80,520))
        screen.blit(s1,(82,522))
        CHAR = screen.blit(pokeball,(140,520))
        screen.blit(c1,(142,522))
        BUTTER = screen.blit(pokeball,(20,580))
        screen.blit(bu1,(22,582))
        PIKA = screen.blit(pokeball,(80,580))
        screen.blit(p1,(82,582))
        PIDGE = screen.blit(pokeball,(140,580))
        screen.blit(pi1,(142,582))
        
        draw.rect(screen,GREY,(200,520,200,110),0)
        roundG=screen.blit(roundGO,(515,520))
        
        R1=draw.rect(screen,RED,(410,520,100,14),0)
        R2=draw.rect(screen,RED,(410,539,100,14),0)
        R3=draw.rect(screen,RED,(410,558,100,14),0)
        R4=draw.rect(screen,RED,(410,577,100,14),0)
        R5=draw.rect(screen,RED,(410,596,100,14),0)
        gameOP=draw.rect(screen,RED,(410,615,100,14),0)

        #--------------------In-game menu text--------------------#

        text=levelFont.render("Money: "+str(money), True, (BLACK))
        screen.blit(text,(525,592))
        text1=levelFont.render("Round: "+str(dex), True, (BLACK))
        screen.blit(text1,(525,573))
        text2=levelFont.render("HP: "+str(hp), True, (BLACK))
        screen.blit(text2,(525,610))
        text3=comicFont.render("UPGRADE", True, (BLACK))
        screen.blit(text3,(427,520))
        text4=comicFont.render("CLOSE", True, (BLACK))
        screen.blit(text4,(437,540))
        text5=comicFont.render("FIRST", True, (BLACK))
        screen.blit(text5,(440,559))
        text6=comicFont.render("STRONG", True, (BLACK))
        screen.blit(text6,(430,578))
        text7=comicFont.render("OPTIONS", True, (BLACK))
        screen.blit(text7,(427,615))
        text8=comicFont.render("SELL TOWER", True, (BLACK))
        screen.blit(text8,(416,596))

        #--------------------Gameplay--------------------#

        if len(WAITenemies)>0 and startR: # When the user can release the enemies
            unleash+=1
            if unleash%30==0:
                bads.append(WAITenemies.pop(0)) #transfer waiting enemies to active enemy list

        if roundG.collidepoint(mx,my):
            gogogo=levelFont.render("LET'S GO!!!",True,(BLACK))
            screen.blit(gogogo,(240,565))
            if click:
                startR=True
                nextRDS=Next[mapchoice]
                if dex < len(nextRDS[lvl]): # Finds which level and map the enemies list coresponds to, and if it's not empty
                    difficle = nextRDS[lvl]
                    Wx=difficle[dex][0]
                    Wy=difficle[dex][1]
                    wave(Wx,Wy)
                    dex+=1
                    roundFINCASH*=1.05 # Increases the money per round   
                    roundFIN+=1
        if dex == len(OrigLength[lvl]):
            if len(bads)==0 and len(WAITenemies)==0:
                for t in towers:
                    if t.target_enemy == None:
                        shots=[]
                        towers=[]
                        bads = []
                        WAITenemies = []
                        shots = []
                        black(screenCopy)
                        mode="Victory"

        if gameOP.collidepoint(mx,my): #open options menu
            opTEXT=comicFont.render("Open options menu",True,(BLACK))
            screen.blit(opTEXT,(200,565))
            if click:
                mode = "Options Mode 1"
        
        if startR==True:
            for e in bads:
                e.draw() #draws enemies on screen
                if e.health<=0:
                    bads.remove(e) #removes defeated enemies
                    money+=10 #+10 money per enemy defeated

            if len(bads)==0 and len(WAITenemies)==0: #if you survive a round
                if hp>0:
                    startR=False
                    if roundFIN>0:
                        money+=int(roundFINCASH) #monetary reward

        #--------------------Tower selection--------------------#

        if CHAR.collidepoint(mx,my): #Charmander tower
            charTEXT=comicFont.render("Charmander",True,(BLACK))
            charTEXT2=comicFont.render("Cost: 250 ",True,(BLACK))
            charTEXT3=comicFont.render("Evolves into:",True,(BLACK))
            charTEXT4=comicFont.render("Charmeleon and Charizard",True,(BLACK))
            charTEXT5=comicFont.render("Upgrade cost: 500",True,(BLACK))
            charTEXT6=comicFont.render("Attack: Flame Burst",True,(BLACK))
            screen.blit(charTEXT,(200,533))
            screen.blit(charTEXT6,(200,548))
            screen.blit(charTEXT2,(200,562))
            screen.blit(charTEXT3,(200,578))
            screen.blit(charTEXT4,(200,593))
            screen.blit(charTEXT5,(200,608))
            if click and money >= 250:
                tool = "CHAR"

        if SQUIRT.collidepoint(mx,my): #Squirtle tower
            squirtTEXT=comicFont.render("Squirtle",True,(BLACK))
            squirtTEXT2=comicFont.render("Cost: 200",True,(BLACK))
            squirtTEXT3=comicFont.render("Evolves into:",True,(BLACK))
            squirtTEXT4=comicFont.render("Wartortle and Blastoise",True,(BLACK))
            squirtTEXT5=comicFont.render("Upgrade cost: 500",True,(BLACK))
            squirtTEXT6=comicFont.render("Attack: Bubblebeam",True,(BLACK))
            screen.blit(squirtTEXT,(200,533))
            screen.blit(squirtTEXT6,(200,548))
            screen.blit(squirtTEXT2,(200,562))
            screen.blit(squirtTEXT3,(200,578))
            screen.blit(squirtTEXT4,(200,593))
            screen.blit(squirtTEXT5,(200,608))
            if click and money >= 200:
                tool = "SQUIRT"

        if BULBA.collidepoint(mx,my): #Bulbasaur tower
            bulbaTEXT=comicFont.render("Bulbasaur",True,(BLACK))
            bulbaTEXT2=comicFont.render("Cost: 200",True,(BLACK))
            bulbaTEXT3=comicFont.render("Evolves into:",True,(BLACK))
            bulbaTEXT4=comicFont.render("Ivysaur and Venusaur",True,(BLACK))
            bulbaTEXT5=comicFont.render("Upgrade cost: 500",True,(BLACK))
            bulbaTEXT6=comicFont.render("Attack: Razor Leaf",True,(BLACK))
            screen.blit(bulbaTEXT,(200,533))
            screen.blit(bulbaTEXT6,(200,548))
            screen.blit(bulbaTEXT2,(200,562))
            screen.blit(bulbaTEXT3,(200,578))
            screen.blit(bulbaTEXT4,(200,593))
            screen.blit(bulbaTEXT5,(200,608))
            if click and money >= 200:
                tool = "BULBA"

        if PIKA.collidepoint(mx,my): #Pikachu tower
            pikaTEXT=comicFont.render("Pikachu",True,(BLACK))
            pikaTEXT2=comicFont.render("Cost: 250",True,(BLACK))
            pikaTEXT3=comicFont.render("Evolves into:",True,(BLACK))
            pikaTEXT4=comicFont.render("Raichu",True,(BLACK))
            pikaTEXT5=comicFont.render("Upgrade cost: 500",True,(BLACK))
            pikaTEXT6=comicFont.render("Attack: Thunderbolt",True,(BLACK))
            screen.blit(pikaTEXT,(200,533))
            screen.blit(pikaTEXT6,(200,548))
            screen.blit(pikaTEXT2,(200,562))
            screen.blit(pikaTEXT3,(200,578))
            screen.blit(pikaTEXT4,(200,593))
            screen.blit(pikaTEXT5,(200,608))
            if click and money >= 250:
                tool = "PIKA"

        if BUTTER.collidepoint(mx,my): #Butterfree tower
            butterTEXT=comicFont.render("Butterfree",True,(BLACK))
            butterTEXT2=comicFont.render("Cost: 250",True,(BLACK))
            butterTEXT3=comicFont.render("Does not evolve",True,(BLACK))
            butterTEXT4=comicFont.render("Upgrade cost: 500",True,(BLACK))
            butterTEXT5=comicFont.render("Attack: Sleep Powder",True,(BLACK))
            screen.blit(butterTEXT,(200,533))
            screen.blit(butterTEXT5,(200,548))
            screen.blit(butterTEXT2,(200,562))
            screen.blit(butterTEXT3,(200,578))
            screen.blit(butterTEXT4,(200,593))
            if click and money >= 200:
                tool = "BUTTER"

        if PIDGE.collidepoint(mx,my): #Pidgey tower
            pidgeTEXT=comicFont.render("Pidgey",True,(BLACK))
            pidgeTEXT2=comicFont.render("Cost: 250",True,(BLACK))
            pidgeTEXT3=comicFont.render("Evolves into:",True,(BLACK))
            pidgeTEXT4=comicFont.render("Pidgeotto and Pidgeot",True,(BLACK))
            pidgeTEXT5=comicFont.render("Upgrade cost: 500",True,(BLACK))
            pidgeTEXT6=comicFont.render("Attack: Twister",True,(BLACK))
            screen.blit(pidgeTEXT,(200,533))
            screen.blit(pidgeTEXT6,(200,548))
            screen.blit(pidgeTEXT2,(200,562))
            screen.blit(pidgeTEXT3,(200,578))
            screen.blit(pidgeTEXT4,(200,593))
            screen.blit(pidgeTEXT5,(200,608))
            if click and money >= 250:
                tool = "PIDGE"

        #--------------------Placing towers--------------------#

        if tool == "CHAR":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my)) #gets colour of mask at mouse
                if CURR!=(0,0,255) and money>=250:
                    screen.blit(CharPics[0],(mx-CharPics[0].get_width()//2,my-CharPics[0].get_height()//2))
                    if CURR == (255,255,255,255)and click: #checks if placement of tower is possible
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 35)
                        tool="none"
                        money-=250
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200)) #draw red circle if placement not possible

        if tool == "SQUIRT":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my))
                if CURR!=(0,0,255)and money>=200:
                    screen.blit(SquirtPics[0],(mx-SquirtPics[0].get_width()//2,my-SquirtPics[0].get_height()//2))
                    if CURR == (255,255,255,255)and click:
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 35)
                        tool="none"
                        money-=200
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200))

        if tool == "BULBA":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my))
                if CURR!=(0,0,255)and money>=200:
                    screen.blit(BulbPics[0],(mx-BulbPics[0].get_width()//2,my-BulbPics[0].get_height()//2))
                    if CURR == (255,255,255,255)and click:
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 35)
                        tool="none"
                        money-=200
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200))

        if tool == "PIKA":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my))
                if CURR!=(0,0,255) and money>=250:
                    screen.blit(PikaPics[0],(mx-PikaPics[0].get_width()//2,my-PikaPics[0].get_height()//2))
                    if CURR == (255,255,255,255)and click:
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 35)
                        tool="none"
                        money-=250
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200))

        if tool == "BUTTER":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my))
                if CURR!=(0,0,255) and money>=250:
                    screen.blit(ButterPics[0],(mx-ButterPics[0].get_width()//2,my-ButterPics[0].get_height()//2))
                    if CURR == (255,255,255,255)and click:
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 40)
                        tool="none"
                        money-=250
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200))

        if tool == "PIDGE":
            if MapOneRect.collidepoint(mx,my):
                CURR = CurrentMask.get_at((mx,my))
                if CURR!=(0,0,255) and money>=250:
                    screen.blit(PidgePics[0],(mx-PidgePics[0].get_width()//2,my-PidgePics[0].get_height()//2))
                    if CURR == (255,255,255,255) and click: 
                        towers.append(tower((mx,my),100,2,tool))
                        draw.circle(CurrentMask, (0,0,255), (mx,my), 35)
                        tool="none"
                        money-=250
                else:
                    gfxdraw.filled_circle(screen,mx,my,25,(245,10,0,200))

        if tool == "none":
            if click:
                if Rect(CurrentMask.get_rect()).collidepoint(mx,my):        #Jerry helped here
                    found_tower=False
                for t in towers:
                    if t.rect.collidepoint((mx,my)) and MapOneRect.collidepoint(mx,my):
                        selected_tower = t
                        found_tower=True 
                    if not found_tower:
                        selected_tower = None

        if selected_tower!=None: #if no tower is selected, display radius
            gfxdraw.filled_circle(screen,selected_tower.rect.centerx,selected_tower.rect.centery,selected_tower.radius,GREY+(100,))
        
        #--------------------Upgrading towers--------------------#

        if R1.collidepoint(mx,my):
            UPtext=comicFont.render("Upgrade the currently",True,(BLACK))
            UPtext2=comicFont.render("selected tower",True,(BLACK))
            screen.blit(UPtext,(200,562))
            screen.blit(UPtext2,(200,578))
            if click:
                if selected_tower != None:
                    if money>500 and selected_tower.evolution!=3:
                        selected_tower.evolution+=1
                        money-=500
                        if selected_tower.evolution>3:
                            selected_tower.evolution=3 

        #--------------------Selling towers--------------------#

        if R5.collidepoint(mx,my):
            SELLtext=comicFont.render("Sell the currently selected",True,(BLACK))
            SELLtext2=comicFont.render("tower",True,(BLACK))
            screen.blit(SELLtext,(200,562))
            screen.blit(SELLtext2,(200,578))
            if click:
                if selected_tower != None:
                    draw.circle(CurrentMask,(WHITE),(selected_tower.rect.centerx,selected_tower.rect.centery),35)
                    towers.remove(selected_tower)
                    money+=175
                    screen.blit(CurrentMap,(0,0))

                    selected_tower = None

        #--------------------Other tower options--------------------#

        if R2.collidepoint(mx,my):
            TARtext=comicFont.render("Target closest foe to tower",True,(BLACK))
            screen.blit(TARtext,(200,562))
            if selected_tower != None and click:
                selected_tower.target="close" #selected tower targets closest enemy

        if R3.collidepoint(mx,my):
            FIRtext=comicFont.render("Target frontmost foe within",True,(BLACK))
            FIRtext2=comicFont.render("range",True,(BLACK))
            screen.blit(FIRtext,(200,562))
            screen.blit(FIRtext2,(200,578))
            if selected_tower != None and click:
                selected_tower.target="first" #selected tower targets first enemy

        if R4.collidepoint(mx,my):
            STRtext=comicFont.render("Target strongest foe within",True,(BLACK))
            STRtext2=comicFont.render("range",True,(BLACK))
            screen.blit(STRtext,(200,562))
            screen.blit(STRtext2,(200,578))
            if selected_tower != None and click:
                selected_tower.target="strong" #selected tower targets strongest enemy

        #--------------------Attacking, shots moving, and animation--------------------#

        for t in towers:
            t.attack(bads)
            for s in shots:
                s.move()
                s.animate()
                if t.target_enemy!=None and s.is_collided_with(bads): #if shot collides with enemy
                    shots.remove(s)

    #--------------------If you lose the game--------------------#


        if hp<1: #resets/removes all values
            black(screenCopy)   # fade out  
            screen.blit(CurrentMap,(0,0))
            screen.blit(CurrentMask,(0,0))
            towers = [] 
            bads = []
            WAITenemies = []
            shots = []
            mode = 'Menu Screen'
            hp=CURRENTIG[lvl]
            money=CURRENTIG[lvl]
            dex=0
            roundFIN=0
            roundFINCASH=300
            offset = 0
            RDMP1E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
            RDMP1M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
            RDMP1H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
            RDMP2E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
            RDMP2M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
            RDMP2H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
            RDMP3E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
            RDMP3M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
            RDMP3H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]


    #---------------------If you win the game---------------------#

    elif mode == "Victory":
        towers = [] 
        screen.blit(victory,(0,0))
        vic=draw.rect(screen,RED,(450,250,100,20))
        ENDtext=comicFont.render("End Game",True,(BLACK))
        screen.blit(ENDtext,(470,250))
        bads = []
        WAITenemies = []
        shots = []
        hp=CURRENTIG[lvl]
        money=CURRENTIG[lvl]
        dex=0
        roundFIN=0
        roundFINCASH=300
        offset = 0
        RDMP1E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
        RDMP1M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
        RDMP1H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
        RDMP2E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
        RDMP2M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
        RDMP2H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
        RDMP3E=[[20,8],[25,12],[35,18],[40,25],[50,30],[60,34],[60,38],[60,45],[75,50],[80,60],[90,65],[100,70],[100,80],[1,100],[1,1000]]
        RDMP3M=[[20,10],[25,17],[40,20],[40,25],[50,30],[60,35],[60,40],[65,45],[75,50],[80,60],[95,65],[110,70],[110,80],[1,100],[1,1000]]
        RDMP3H=[[20,20],[25,22],[45,25],[40,34],[50,40],[60,35],[60,45],[75,45],[80,55],[90,60],[95,75],[110,75],[120,80],[1,100],[1,1000]]
        if vic.collidepoint(mx,my) and click:
            mode="Menu Screen"
            
            
    ticTok.tick(60)    
    display.flip()
    display.set_caption("FPS: " + str(ticTok.get_fps()))
    screenCopy = screen.copy()
quit()
