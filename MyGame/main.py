import pygame as pg
from pygame import mixer
import random as r
import math as m

pg.init()
screen = pg.display.set_mode((800,600))

#Title and Icon
pg.display.set_caption('Balloon Shooter')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

#Background Image
bgIMG = pg.image.load('bg2.jpg')

#Background music
mixer.music.load('[MP3DOWNLOAD.TO] Imagine Dragons - Bad Liar (Lyrics)-HQ.wav')
mixer.music.play(-1)

#Player
playerImg = pg.image.load('pistol.png')
playerX = 700
playerY = 30
playerY_CHG = 0

def player(x,y):
	screen.blit(playerImg,(x,y))
#Ballon
balloonImg = []
balloonX = []
balloonY = []
balloonX_chg = []
balloonY_chg = []

n_balloons = 5
for i in range(n_balloons):
	balloonImg.append(pg.image.load('balloonRed.png'))
	balloonX.append(r.randint(50,150))
	balloonY.append(r.randint(0,30))
	balloonX_chg.append(40)
	balloonY_chg.append(0.2)

def balloon(x, y, i):
	screen.blit(balloonImg[i],(x,y))

#Bullet 
bulletImg = pg.image.load('bullet2.png')
bulletX = 700
bulletY = 0
bulletX_chg = 0.9
bulletY_chg = 0
bullet_state = 'ready'


font = pg.font.Font('freesansbold.ttf',28)
score = 0
textX = 10
textY = 10

endGame = pg.font.Font('freesansbold.ttf',64)

def show_score(x, y):
	scoreV = font.render(f"Score: {score}", True, (255,0,123))
	screen.blit(scoreV,(x,y))

def game_over():
	text = endGame.render("GAME OVER",True,(255,0,0))
	screen.blit(text, (200,250))
def fire(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bulletImg,(x,y+5))

def isCollision(balloonX, balloonY, bulletX, bulletY):
	distance = m.sqrt((m.pow(balloonX - bulletX,2))+(m.pow(balloonY - bulletY,2)))
	return distance < 27

#Game loop
running = True
while running:
	#RGB BackGround color
	screen.fill((255,255,255))
	screen.blit(bgIMG, (0,0))

	for event in pg.event.get():

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_UP:
				playerY_CHG = -0.3
			elif event.key == pg.K_DOWN:
				playerY_CHG = 0.3
			elif event.key == pg.K_SPACE:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletY = playerY
					fire(bulletX, bulletY)

		if event.type == pg.KEYUP:
			if event.key == pg.K_UP or event.key == pg.K_DOWN:
				playerY_CHG = 0

		if event.type == pg.QUIT:
			running = False 

	#Boundary Check

	playerY += playerY_CHG

	if playerY <= 0:
		playerY = 0
	elif playerY >= 536:
		playerY = 536

	#Ballon
	for i in range(n_balloons):

		#Game Over Text
		if balloonX[i] >= 672:
			for j in range(n_balloons):
				balloonX[j] = 2000
			game_over()
			break
		balloonY[i] += balloonY_chg[i]
		if balloonY[i] <= 0:
			balloonY_chg[i] = 0.2
			balloonX[i] += balloonX_chg[i]
		elif balloonY[i] >= 536:
			balloonY_chg[i] = -0.2
			balloonX[i] += balloonX_chg[i]

			#Collision
		collision = isCollision(balloonX[i], balloonY[i], bulletX, bulletY)
		if collision:
			blast = mixer.Sound('mixkit-ballon-blows-up-3071.wav')
			blast.play()
			bulletX = 700
			bullet_state = 'ready'
			score += 1
			balloonX[i] = r.randint(50,120)
			balloonY[i] = r.randint(0,30)

		balloon(balloonX[i],balloonY[i],i)

	'''if balloonX[i] >= 672:
					print('Game Over.')
					balloonX[i] = 672'''

	#Bullet
	if bulletX <= 0:
		bulletX = 700
		bullet_state = 'ready'
	if bullet_state == 'fire':
		fire(bulletX,bulletY)
		bulletX -= bulletX_chg



	player(playerX,playerY)
	show_score(textX,textY)
	pg.display.update()