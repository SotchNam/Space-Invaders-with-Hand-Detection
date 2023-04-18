#Game file that imports the different modules and runs the game#
#please dont blame my young self who was inexperienced and lacked the time and skill to write good code instead of spaghetti code.
import pygame, sys
from player import Player
from alien import Alien, Extra
from random import choice, randint
from lazer import Lazer
from threading import Thread


#game class the contains its logic
class Game:
    def __init__(self,screen_width,screen_height,screen,clock):
        #initializing variables, screen, sprites, sounds, etc
        player_sprite = Player((screen_width/2,screen_height),screen_width,screen_height,5)
        
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.screen=screen
        self.clock=clock
        self.clock.tick(60)
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



    #function that takes care of spawning aliens
    def alien_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset=70,y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x= col_index*x_distance+x_offset
                y= row_index *y_distance+y_offset
                
                if row_index== 0 : alien_sprite= Alien("red",x,y) 
                elif 1<= row_index<=2: alien_sprite= Alien("green",x,y) 
                else : alien_sprite= Alien("yellow",x,y) 
                self.aliens.add(alien_sprite)

    #checks when aliens bump the sides of the screen and makes them move down accordingly
    def alien_position_check(self):
        all_aliens= self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen_width:
                self.alien_direction=-1
                self.alien_down(5)
            if alien.rect.left<=0:
                self.alien_direction=1
                self.alien_down(5)
  

    #function that moves aliens up or down, depending on their direction
    def alien_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                if alien.rect.bottom>= self.screen_height-50:
                    self.down_state=-1
                if alien.rect.top<= 90:
                    self.down_state=1

            for alien in self.aliens.sprites():
                alien.rect.y += distance*self.down_state

    #function that makes aliens shoot lazer
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            lazer_sprite = Lazer(random_alien.rect.center,6) 
            self.aliens_lasers.add(lazer_sprite)
            self.laser_sound.play()

    #draws remaining lives in the right corner of the screen 
    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos*0+10 + (live * (self.live_surf.get_size()[0] + 10))
            self.screen.blit(self.live_surf,(x,8))


    #timer that randomwly chooses when to spawn the extra alien
    def extra_spawn_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <=0:
            self.extra.add(Extra( choice(["right","left"]) ,self.screen_width))
            self.extra_spawn_time= randint(400,800)


    #function that checks for collision between aliens,player, and lazers
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


    #triggered when player collids with incoming alien lazer
    def damaged(self):
        self.lives-=1
        self.player.cooldown_time = pygame.time.get_ticks()
        self.player.sprite.cool()
        self.player.sprite.cooldown_time = pygame.time.get_ticks()

    #draws score on upper right corner
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (400,-10))
        self.screen.blit(score_surf,score_rect)

    #triggered when all normal aliens have been killed
    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won',False,'white')
            victory_rect = victory_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
            self.screen.blit(victory_surf,victory_rect)

    #triggered when out of lives
    def gameover(self):
        if self.lives<=0 :
            gameOver= self.font.render("Game Over",False,"white")
            gameOver_rect= gameOver.get_rect(center=(self.screen_width/2,self.screen_height/2))
            self.screen.blit(gameOver,gameOver_rect)

    #triggered after game end to retry, has been bypassed to automatically restart the game for showcase purposes
    def retryText(self):
        if self.lives<=0 or not self.aliens.sprites():
            #retry= self.font.render("press SPACE to retry",False,"white")
            retry= self.font.render("retrying...",False,"white")
            retry_rect= retry.get_rect(center=(self.screen_width/2,(2*self.screen_height/3)))
            self.screen.blit(retry,retry_rect)

    #triggered when no hand is detected to prompt to put hand infront of camera
    def hand_detected(self):
        if not self.handOK and (self.aliens.sprites())and self.lives>0:
            handText=self.font.render("Please put your hand",False,"white")
            handText_rect= handText.get_rect(center=(self.screen_width/2,self.screen_height/2))
            self.screen.blit(handText,handText_rect)

    #draws the different sprites and calls drawing funcs
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
        self.gameover()
        self.retryText()

    #plays the game when hand and lives are available
    def runMove(self):
        if self.handOK and self.lives>0:
            self.player.update()
            self.aliens_lasers.update()

            self.aliens.update(self.alien_direction)
            self.extra.update()
            self.extra_spawn_timer()
        else:
            self.hand_detected()

#class that draws scanlines over the screen for a retro look
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


#the game thread that runs the game
#start and stop get called in the main file to manage the thread
class Space(Thread):
    def __init__(self):
        self.ok = True
        screen_width = 600
        screen_height= 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock= pygame.time.Clock()
        clock.tick(30)
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

        while self.ok :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.ok=False
                if event.type == ALIENLAZER and game.handOK and game.lives>0:
                    game.alien_shoot()

            if  not game.player.sprite.close():
                self.ok=False
                pygame.quit()

            #restart stuff
            keys = pygame.key.get_pressed()
            if game.lives<=0:
                game.gameover()

            if game.lives<=0 or not game.aliens.sprites():
                game.__init__(screen_width,screen_height,screen,clock)
                game.lives= 5

            screen.fill((30,30,30))
            game.runDraw()
            game.runMove()
            self.crt.draw(screen)
            pygame.display.flip()
            pygame.time.wait(0)
        self.ok=False   
