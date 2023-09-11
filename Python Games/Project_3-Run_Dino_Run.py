# welcome page
# -welcome image
# -msg
#
# start-
# by space key
#
# stop-
# on collide with cactus
#     show-
#     -written game over
#     -an arrow
#
# restart-
# space key or tap anywhere in given boundry
#
# score-
# 1.maximum score remember it from previous
# 2.distance in x
#
# sound-
# press space keyword
# out
#
# screen
# -background
# -dinosaur
# -cactus
# -bird
# -Hi score image


#not jumping
#score increasing only when pressing space
#obs are coming at same place, without gap

import pygame
import random
import sys
from pygame.locals import*

#global variable
screen_w=797
screen_h=448
screen=pygame.display.set_mode((screen_w,screen_h))
fps=32
clock=pygame.time.Clock()
game_sprites={}


def welcome():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN and event.key == K_SPACE:
                return

            else:
            # blitting
                screen.blit(game_sprites['welcome'], (0,0))
                screen.blit(game_sprites['msg'], (0,120))
                pygame.display.update()
                clock.tick(fps)

def main():
    score=0
    playerx=50
    playery=250
    p=0
    cac=[
        {'x':screen_w+200,'y':180},
        {'x':screen_w+200+screen_w,'y':180}
    ]

    obsvelx = -8
    playervel_y=-12
    playeracc_y=1
    player_min=-15
    player_max=10

    player_flap=-15
    flap = False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN and event.key==K_SPACE:
                if playery>0:
                    playervel_y=player_flap
                    flap=True

        crash=crash_test(playerx,playery,cac)
        #if player crash
        if crash:
           print(f"your score is {score}")
           return

        if playervel_y<player_max and not flap:
            playervel_y+=playeracc_y

        if flap:
            flap=False
        player_h=game_sprites['dino'].get_height()
        playery=playery+min(playervel_y,250-playery-player_h)



        #move cactus to left
        for cactus in cac:
            cactus['x']+=obsvelx

        #add new obs in cactus
        # if 0<cac[0]['x']<5:
        #     cac.append({'x':screen_w+200,'y':180})

        #if obs go out of screen
        if cac[0]['x']<=-game_sprites['cactus'][p].get_width():
            cac.pop(0)
            cac.append({'x': screen_w + random.randrange(400,600), 'y': 180})
            p = random.randrange(0, 4)


        #blitting
        screen.blit(game_sprites['background'],(0,0))
        screen.blit(game_sprites['dino'], (playerx,playery))
        for pos in cac:
            screen.blit(game_sprites['cactus'][p],(pos['x'],pos['y']))
        score+=1

        #max_score=score
        mystr=[int(m) for m in list(str(score))]
        width=0
        for my in mystr:
            width+=game_sprites['numbers'][my].get_width()
        x=(screen_w-width)/2
        for my in mystr:
            screen.blit(game_sprites['numbers'][my],(x,100))
            x+=game_sprites['numbers'][my].get_width()
        pygame.display.update()
        clock.tick(fps)

def crash_test(playerx,playery,cac):
    for cactus in cac:
        if playerx+game_sprites['dino'].get_width()>=cactus['x'] and cactus['y']<=playery+game_sprites['dino'].get_height():
            return True

    return False

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("dinosaur and Poonam")
    game_sprites['welcome']=pygame.image.load("dino game\wel.jpg").convert_alpha()
    game_sprites['msg']=pygame.image.load("dino game\dinogame.jpg").convert_alpha()
    game_sprites['background'] = pygame.image.load("dino game\sackground.png").convert()
    game_sprites['dino'] = pygame.image.load("dino game\dino.jpg").convert_alpha()
    game_sprites['cactus'] = (
        pygame.image.load("dino game\cactus_1.jpg").convert_alpha(),
        pygame.image.load("dino game\cactus_2.jpg").convert_alpha(),
        pygame.image.load("dino game\cactus_3.jpg").convert_alpha(),
        pygame.image.load("dino game\cactus_4.jpg").convert_alpha()
    )
    game_sprites['numbers'] = (
        pygame.image.load('flappy bird/0.jpg').convert_alpha(),
        pygame.image.load('flappy bird/1.jpg').convert_alpha(),
        pygame.image.load('flappy bird/2.jpg').convert_alpha(),
        pygame.image.load('flappy bird/3.jpg').convert_alpha(),
        pygame.image.load('flappy bird/4.jpg').convert_alpha(),
        pygame.image.load('flappy bird/5.jpg').convert_alpha(),
        pygame.image.load('flappy bird/6.jpg').convert_alpha(),
        pygame.image.load('flappy bird/7.jpg').convert_alpha(),
        pygame.image.load('flappy bird/8.jpg').convert_alpha(),
        pygame.image.load('flappy bird/9.jpg').convert_alpha()
    )
    game_sprites['kite'] = pygame.image.load("dino game\kite.jpg").convert_alpha()
    while True:
        welcome()
        main()


