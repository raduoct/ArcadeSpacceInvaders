from __future__ import division
from os import path
import pygame, random

BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
        
SCREENWIDTH=800
SCREENHEIGHT=600

#Aici sunt grupuri cu toate sprite urile din joc, grupul all sprites este pentru a desena sprite urile, celelalte grupuri servesc la coliziuni
all_sprites_list = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemies = pygame.sprite.Group()
bariere = pygame.sprite.Group()

class Erou(pygame.sprite.Sprite):
 
	def __init__(self, color, width, height, life):
		super(Erou, self).__init__()
		self.image = pygame.Surface([width, height])
 		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.width=width
		self.life = life
		self.bullet_timer= .5
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()

	def update(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			if self.rect.x>0 :
				self.rect.x -= 5
		if keys[pygame.K_d]:
			if self.rect.x<SCREENWIDTH - self.width  :
				self.rect.x += 5
		self.bullet_timer -= dt 
		if keys[pygame.K_SPACE] and self.bullet_timer <= 0:
			laser = Glont(GREEN, 5,10,self.rect.x+10, self.rect.y-10, 1)
			all_sprites_list.add(laser)
			bullets.add(laser)
			self.bullet_timer = .5  
     
class Inamic(pygame.sprite.Sprite):
 
	def __init__(self, color, width, height,x,y):
		super(Inamic, self).__init__() 
		self.image = pygame.Surface([width, height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE) 
		self.pos=pygame.math.Vector2((x,y))
		self.x=x
		self.semn = 1 
		self.vel = pygame.math.Vector2(30, 0)
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()  
	  
	def update(self, dt):
		if abs(self.x - self.pos[0])>250 : 
			self.semn = self.semn*(-1)
		self.pos = self.pos+ self.semn*self.vel * dt
		self.rect.center = self.pos

class Glont(pygame.sprite.Sprite):

	def __init__(self, color, width, height,x,y, sens):
		super(Glont,self).__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.width=width
		self.sens=sens
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()
		self.pos = pygame.math.Vector2((x,y))
		self.vel= pygame.math.Vector2(0, -150)
        
  

	def update(self, dt):
		self.pos = self.pos + self.sens * self.vel * dt
		self.rect.center = self.pos  # Update the rect pos.
		if self.rect.y < 0 or self.rect.y > SCREENHEIGHT:
			self.kill()
            
class Barrier(pygame.sprite.Sprite):
 
	def __init__(self, color, width, height,x,y):
		super(Barrier, self).__init__() 
		self.image = pygame.Surface([width, height])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()        
		self.rect.x = x
		self.rect.y = y 

def gloante_inamici(dt, timer):
	timer-= dt
	dictionar = dict()
	for enemy in enemies:
		dictionar.setdefault (enemy.rect.x,[]).append(enemy.rect.y)
	for key in dictionar:
		dictionar[key].sort(reverse = True)
	if timer <= 0:
		bullet = Glont(BLUE, 5,10, key, dictionar[key][0]+20, -1)
		all_sprites_list.add(bullet)
		bullets_enemies.add(bullet)
		timer = .5
	return timer

pygame.init()
 
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Invaders")
myfont = pygame.font.Font("freesansbold.ttf", 20) 
 
player = Erou(RED, 20, 30, 3)
player.rect.x = 380
player.rect.y = 560
all_sprites_list.add(player)
player_group.add(player)

for i in range(0, 5):
	for j in range (0,5):
		alien = Inamic(PURPLE, 10,20,300+i*60,50+j*30)
		all_sprites_list.add(alien)
		enemies.add(alien)

for k in range(0,5):
	for i in range(0,4):
		for j in range(0,4):
			bar = Barrier(YELLOW, 25, 15, 150*k+50 + i*20, 450 +j*20)
			all_sprites_list.add(bar)
			bariere.add(bar)
    
carryOn = True
bullet_enemy_timer = .5
scor = 0
nr_enem= 25
clock=pygame.time.Clock()
 
while carryOn:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			carryOn=False
        
	dt = clock.tick(60) / 1000
	bullet_enemy_timer = gloante_inamici(dt, bullet_enemy_timer)        
	hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
	for enemy, bullet_list in hits.items():
		scor += 10
		nr_enem -= 1
		if nr_enem == 0:
			carryOn=False
	hits_gloante = pygame.sprite.groupcollide(bullets_enemies, bullets, True, True)
	for be, bullet_list in hits_gloante.items():
		scor += 5
        
	pygame.sprite.groupcollide(bariere, bullets, True, True) 
	pygame.sprite.groupcollide(bariere, bullets_enemies, True, True)
	hits_erou = pygame.sprite.groupcollide(bullets_enemies, player_group, True, False)
	for enemy_bullet, player_list in hits_erou.items():
		player.life -= 1
		if player.life == 0:
			carryOn=False 
            	               
	all_sprites_list.update(dt)
	screen.fill(BLACK)
	all_sprites_list.draw(screen)
        
	scoretext = myfont.render("Score {0}".format(scor), 1, WHITE)
	screen.blit(scoretext, (5, 10))
        
	scoretext = myfont.render("Lives {0}".format(player.life), 1, YELLOW)
	screen.blit(scoretext, (700, 10))
        
	pygame.display.flip()
 
keepgoing = True        
while keepgoing:
	highscore = scor
	if path.exists("highscore.txt"):
		f = open("highscore.txt","r")
		salvat = int(f.readline().strip())
		if salvat > highscore:
			highscore=salvat

	screen.fill(BLACK)
	scoretext = myfont.render("High Score {0}".format(highscore), 1, BLUE)
	screen.blit(scoretext, (300, 300))
        
	scoretext = myfont.render("Score {0}".format(scor), 1, WHITE)
	screen.blit(scoretext, (300, 270))
                
	pygame.display.flip()
 	
	f = open("highscore.txt","w")
	f.write(str(highscore) + "\n")
 	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			keepgoing=False
 
pygame.quit() 
