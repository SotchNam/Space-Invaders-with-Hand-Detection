import pygame, sys
from player import Player
from alien import Alien, Extra
from random import choice, randint
from lazer import Lazer
#import pp3
from threading import Thread


class Game:
	def __init__(self,screen_width,screen_height,screen,clock):
		player_sprite = Player((screen_width/2,screen_height),screen_width,screen_height,5)
		
		self.screen_width=screen_width
		self.screen_height=screen_height
		self.screen=screen
		self.clock=clock

		self.handOK=False



		self.player = pygame.sprite.GroupSingle(player_sprite)

		self.aliens = pygame.sprite.Group()
		self.aliens_lasers= pygame.sprite.Group()
		self.alien_setup(rows=6,cols=8)
		self.alien_direction=1
		self.down_state=1

		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time= randint(400,800)

		self.lives = 5
		self.live_surf = pygame.image.load('./graphics/player.png').convert_alpha()
		self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)

		self.score =0
		self.font = pygame.font.Font("./font/Pixeled.ttf",20)

		music = pygame.mixer.Sound('./audio/music.wav')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)



	def alien_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset=70,y_offset=100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x= col_index*x_distance+x_offset
				y= row_index *y_distance+y_offset
				
				if row_index== 0 : alien_sprite= Alien("red",x,y) 
				elif 1<= row_index<=2: alien_sprite= Alien("green",x,y) 
				#if 0<= row_index<=2: alien_sprite= Alien("green",x,y) 
				else : alien_sprite= Alien("yellow",x,y) 
				self.aliens.add(alien_sprite)

	def alien_position_check(self):
		all_aliens= self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= self.screen_width:
				self.alien_direction=-1
				self.alien_down(5)
			if alien.rect.left<=0:
				self.alien_direction=1
				self.alien_down(5)
  

	def alien_down(self, distance):
		if self.aliens:
		 	for alien in self.aliens.sprites():
		 		if alien.rect.bottom>= self.screen_height-50:
		 			self.down_state=-1
		 		if alien.rect.top<= 90:
		 			self.down_state=1

		 	for alien in self.aliens.sprites():
		 		alien.rect.y += distance*self.down_state

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			lazer_sprite = Lazer(random_alien.rect.center,6) 
			self.aliens_lasers.add(lazer_sprite)
			self.laser_sound.play()

	def display_lives(self):
		for live in range(self.lives):
			x = self.live_x_start_pos*0+10 + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))


	def extra_spawn_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <=0:
			self.extra.add(Extra( choice(["right","left"]) ,self.screen_width))
			self.extra_spawn_time= randint(400,800)


	def collision_checks(self):
		if self.player.sprite.lazers:
			for lazer in self.player.sprite.lazers:
				aliens_hit= pygame.sprite.spritecollide(lazer,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					lazer.kill()

				if pygame.sprite.spritecollide(lazer,self.extra,True):
					self.score+=500
					lazer.kill()


		if self.aliens_lasers:
			for lazer in self.aliens_lasers:
				if pygame.sprite.spritecollide(lazer,self.player,False):
					lazer.kill()
					self.damaged()

		if self.aliens:
			for alien in self.aliens:
				if pygame.sprite.spritecollide(alien,self.player,False):
					alien.kill()
					self.damaged()

		if self.extra:
			if pygame.sprite.groupcollide(self.extra,self.player,False,False):
				self.damaged()


	def damaged(self):
		self.lives-=1
		self.player.cooldown_time = pygame.time.get_ticks()
		#self.player.sprite.cooldown_state= False
		self.player.sprite.cool()
		self.player.sprite.cooldown_time = pygame.time.get_ticks()


	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (400,-10))
		self.screen.blit(score_surf,score_rect)

	def victory_message(self):
		if not self.aliens.sprites():
			victory_surf = self.font.render('You won',False,'white')
			victory_rect = victory_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
			self.screen.blit(victory_surf,victory_rect)


	def hand_detected(self):
		if not self.handOK and (self.aliens.sprites()):
			handText=self.font.render("Please put your hand",False,"white")
			handText_rect= handText.get_rect(center=(self.screen_width/2,self.screen_height/2))
			self.screen.blit(handText,handText_rect)

	def runDraw(self):
		self.player.sprite.lazers.draw(self.screen)

		
		self.alien_position_check()

		self.extra.draw(self.screen)

		self.player.draw(self.screen)
		self.aliens.draw(self.screen)
		
		self.aliens_lasers.draw(self.screen)
		self.display_lives()
		self.display_score()

		self.collision_checks()
		self.victory_message()

	def runMove(self):
		if self.handOK:
			self.player.update()
			self.aliens_lasers.update()

			self.aliens.update(self.alien_direction)
			self.extra.update()
			self.extra_spawn_timer()
		else:
			self.hand_detected()

class CRT:
	def __init__(self):
		self.tv = pygame.image.load('./graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(600,600))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(600/ line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(600,y_pos),1)

	def draw(self,screen):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		screen.blit(self.tv,(0,0))


class Space(Thread):
	def __init__(self):
		self.ok = True
		screen_width = 600
		screen_height= 600
		screen = pygame.display.set_mode((screen_width, screen_height))
		clock= pygame.time.Clock()
		self.crt= CRT()
		self.games= Game(screen_width,screen_height,screen,clock)

	def start(self):
		Thread(target = self.run, args=()).start()
		return self

	def stop(self):
		sys.exit()

	def run(self):	
		pygame.init() 
		screen_width = 600
		screen_height= 600
		screen = pygame.display.set_mode((screen_width, screen_height))
		clock= pygame.time.Clock()
		game= self.games

		ALIENLAZER = pygame.USEREVENT =1
		pygame.time.set_timer(ALIENLAZER,800)

		while game.lives>=0 :
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.ok=False
					pygame.quit()
					#sys.exit()

				if event.type == ALIENLAZER and game.handOK:
					game.alien_shoot()
			if 	not game.player.sprite.close():
				self.ok=False
				pygame.quit()
				#sys.exit()

			screen.fill((30,30,30))
			game.runDraw()
			game.runMove()
			self.crt.draw(screen)
			pygame.display.flip()
			clock.tick(60) 
		self.ok=False	
		#print(game.score)



if __name__ == '__main__':
	Space().run()