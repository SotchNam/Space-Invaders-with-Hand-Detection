###module for player###
import pygame
from lazer import Lazer
	

class Player(pygame.sprite.Sprite):
	def __init__ (self,pos,constraintX,constraintY,speed):
		super().__init__()
		self.image = pygame.image.load ("./graphics/player.png").convert_alpha()
		self.rect = self.image.get_rect(midbottom =pos)
		self.speed=speed
		self.max_X = constraintX
		self.max_Y = constraintY
		self.screen= pygame.Rect((0,0,constraintX,constraintY))
		self.ready=True
		self.lazer_time=0
		self.lazer_cooldown = 600
		self.lazers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.cooldown_time =0 
		self.cooldown=300
		self.cooldown_state = True
		self.closeState= True

	def get_input (self):
		keys = pygame.key.get_pressed()


		if self.ready:
			self.shoot_lazer()
			self.ready=False
			self.lazer_time = pygame.time.get_ticks()
			self.laser_sound.play()


		if keys[pygame.K_q]:
			self.closeState=False
		
		if keys[pygame.K_RIGHT] and    self.cooldown_state:
			self.rect.x+= self.speed
		elif keys [pygame.K_LEFT] and   self.cooldown_state:
			self.rect.x -= self.speed

	def cool(self):
		self.cooldown_state= False

	def cooling(self):
		if not self.cooldown_state:
			current_time2= pygame.time.get_ticks()
			if (current_time2- self.cooldown_time ) >= self.cooldown:
				self.cooldown_state=True

	def recharge(self):
		if not self.ready:
			current_time= pygame.time.get_ticks()
			if current_time- self.lazer_time >= self.lazer_cooldown:
				self.ready=True

	def shoot_lazer(self):		
		self.lazers.add(Lazer(self.rect.clamp(self.screen).center,-2*self.speed))
		
			
	def clamp(self):
		self.rect=self.rect.clamp(self.screen)

	def close(self):
		return self.closeState

	def update (self):
		self.get_input()
		self.clamp()
		self.recharge()
		self.cooling()
		self.lazers.update()
