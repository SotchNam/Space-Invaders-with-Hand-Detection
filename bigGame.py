import space2
from pp3 import HandDet
from threading import Thread
import pygame

handThread = HandDet()
handThread.start()
pygame.init()


def passer(game,hand):
    game.game.player.rect.x=hand.x
    game.y=hand.y


#gameThread= space2.Space().start()

game=space2.Space()

#Thread(target = passer, args=(game,handThread)).start()

converter=600/640

game.start()


state=True
#print(game.ok)

while state:
    #print(handThread.x)
    if handThread.handOK:
        game.games.player.sprite.rect.x=600-handThread.x*converter
    handThread.state=game.ok
    state=game.ok
    #print(game.ok)
    game.games.handOK=handThread.handOK
game.stop()
handThread.stop()
#handThread.state=False


#gameThread = space2

#gameThread.start(target=run)










"""
handThread=Thread(target=pp3.run())
gameThread=Thread(target=space2.bigRun())

handThread.start()
gameThread.start()

state=True
while state:
    if keyboard.read_key() == "q":
        state=False
        break

handThread.stop()
gameThread.stop()

#pp3.main()
"""
