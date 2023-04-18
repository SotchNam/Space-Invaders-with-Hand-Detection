import space
from handDet import HandDet
from threading import Thread
import pygame

converter=600/640
state=True

handThread = HandDet()
handThread.start()
pygame.init()

game=space.Space()
game.start()



while state:
    if handThread.handOK:
        game.games.player.sprite.rect.x=600-handThread.x*converter
    handThread.state=game.ok
    state=game.ok
    game.games.handOK=handThread.handOK

game.stop()
handThread.stop()
pygame.quit()
