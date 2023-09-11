#https://docs.google.com/presentation/d/1nbeOqqNQZudiuhMxtnAk-Trmosu43tN4/edit?usp=sharing&ouid=108733967580930712585&rtpof=true&sd=true
# open app->instructions->get start->given-no of chance
# or time limit or certain goal->then simply game over
# and tell results-kind of winners, or scores->
# then some rewards(additional)->replay
# import pygame
# pygame.init()
# screen=pygame.display.set_mode((1280,720))
# running=True
# speed=[2,2]
# player_pos=pygame.Vector2(0,0)
# ball=pygame.image.load("dore.gif")r
# ballrect=ball.get_rect()
# while running:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             running=False
#
#     ballrect=ballrect.move(speed)
#
#     if ballrect.left<0 or ballrect.right>1280:
#         speed[0]=-speed[0]
#     if ballrect.top < 0 or ballrect.bottom > 720:
#         speed[1] = -speed[1]
#     # pygame.draw.circle(screen,'black',player_pos,40)
#
#     # fill()
#     # we erase the screen by filling it with a black RGB color.If you have never worked with animations this may seem strange.
#     # You may be asking "Why do we need to erase anything, why don't we just move the ball on the screen?" That is not quite the
#     # way computer animation works.Animation is nothing more than a series of single images, which when displayed in sequence do a very good
#     # job of fooling the human eye into seeing motion.The screen is just a single image that the user sees.If we did not take the time to erase
#     # the ball from the screen, we would actually see a "trail" of the ball as we continuously draw the ball in its new positions.
#     screen.fill("purple" )
#
#     # blit()
#     # Pygame has a display Surface. This is basically an image that is visible on the screen, and the image is made up of pixels. The main way you change these pixels is by calling the blit() function.
#     # This copies the pixels from one image onto another.
#     # This is the first thing to understand. When you blit an image onto the screen, you are simply changing the color of the pixels on the screen. Pixels aren't added or moved,
#     # we just change the colors of the pixels already on the screen. These images you blit to the screen are also Surfaces in pygame, but they are in no way connected to the display Surface.
#     # When they are blitted to the screen they are copied into the display, but you still have a unique copy of the original.
#     # With this brief description. Perhaps you can already understand what is needed to "move" an image.
#     # We don't actually move anything at all. We simply blit the image in a new position. But before we draw the image in the new position, we'll need to "erase" the old one. Otherwise the image will be visible in two places on the screen. By rapidly erasing the image and redrawing it in a new place, we achieve the "illusion" of movement.
#     screen.blit(ball,ballrect)
#
#     keys=pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         speed=[0,0]
#     if keys[pygame.K_s]:
#         speed=[1,1]
#     # if keys[pygame.K_a]:
#     #     player_pos.x-=300*dt
#     # if keys[pygame.K_d]:
#     #     player_pos.x+=300*dt
#
#     pygame.display.flip()
#
#
# pygame.quit()

# animation->is just a number of single images.one by one in speed screen changes.
# image is made of pixels..so to change an image to another, we just change color of pixels.
# none of pixels add or move or remove. for changing color of pixel we have to color a pixel from the old one
# (means its original color)then color another pixel.
# Blit:-assigning pixel   -blitting assigns the color of pixels in our image.


import pygame
import random #for generating random numbers
import sys
from pygame.locals import * # basic pygame imports

#global var
fps=32
screen_w=320
screen_h=580
screen=pygame.display.set_mode((screen_w,screen_h))
ground_y=screen_h*0.85
game_sprites={}
game_sounds={}
Player='flappy bird/Flappy-bird.jpg'
Back_ground='flappy bird/background.png'
Pipe='flappy bird/pipe_edited.jpg'
clock = pygame.time.Clock()

def welcome():
    '''
    show welcome screen
    '''
    base_x=0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

            else:
                screen.blit(game_sprites['message'], (0,0))
                screen.blit(game_sprites['base'], (base_x,ground_y))
                pygame.display.update()
                clock.tick(fps)


def maingame():
    score=0
    playerx = int(screen_w / 3)
    playery = int(screen_h - game_sprites['player'].get_height()) / 2
    base_x=0

    #create two positions of pipe
    pipepos1=newpipe()
    pipepos2=newpipe()
    upperpipe=[
        {'x':screen_w+500,'y':pipepos1[0]['y']},
        {'x':screen_w+500+screen_w,'y':pipepos2[0]['y']}
    ]
    lowerpipe = [
        {'x': screen_w + 500, 'y': pipepos1[1]['y']},
        {'x': screen_w + 500 + screen_w, 'y': pipepos2[1]['y']}
    ]
    pipevelx=-4
    playervel_y=-9
    playeracc_y=1
    player_min=-8
    player_max=10

    playerflap=-8 #velocity while flapping
    flapp = False #it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN and (event.key==K_UP or event.key==K_SPACE):
                if playery>0:
                    flapp=True
                    playervel_y=playerflap

        crashtest=iscolide(playerx,playery,upperpipe,lowerpipe)

        #if player crashed
        if crashtest:
            return

        #check for score
        playermidpos=playerx+ game_sprites['player'].get_width()/2
        for pipe in upperpipe:
            pipemidpos=pipe['x']+game_sprites['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"your score is {score}")

        if playervel_y<player_max and not flapp:
            playervel_y+=playeracc_y

        if flapp:
            flapp=False
        player_h=game_sprites['player'].get_height()
        playery=playery+min(playervel_y,ground_y-playery-player_h)

        #move pipes to the left
        for upper,lower in zip(upperpipe,lowerpipe):
            upper['x']+=pipevelx
            lower['x']+=pipevelx

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if  0<upperpipe[0]['x']<5:
            newpi=newpipe()
            upperpipe.append({'x':screen_w+200,'y':newpi[0]['y']})
            lowerpipe.append({'x':screen_w+200,'y':newpi[1]['y']})

        # if the pipe is out of the screen, remove it
        if upperpipe[0]['x']<-game_sprites['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)

        #lets blit our sprites now
        screen.blit(game_sprites['back_ground'],(0,0))
        for upper, lower in zip(upperpipe, lowerpipe):
            screen.blit(game_sprites['pipe'][0], (upper['x'],upper['y']))
            screen.blit(game_sprites['pipe'][1], (lower['x'], lower['y']))
        screen.blit(game_sprites['base'], (base_x,ground_y))
        screen.blit(game_sprites['player'], (playerx,playery))

        mydigit=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigit:
            width+=game_sprites['numbers'][digit].get_width()
        xoff=(screen_w-width)/2
        for digit in mydigit:
            screen.blit(game_sprites['numbers'][digit],(xoff,screen_h*0.12))
            xoff+=game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        clock.tick(fps)

def iscolide(playerx,playery,upperpipe,lowerpipe):
    if playery>ground_y-25 or playery<0:
        return True

    for pipe in upperpipe:
        pipe_h= game_sprites['pipe'][0].get_height()
        if (playery<pipe_h+pipe['y'] and abs(playerx-pipe['x'])<game_sprites['pipe'][0].get_width()):
            return True

    for pipe in lowerpipe:
        if (playery+game_sprites['player'].get_height()>pipe['y'] and abs(playerx-pipe['x'])<game_sprites['pipe'][0].get_width()):
            return True

    return False



def newpipe():
    '''
    generate position of upper pipe and lower pipe
    '''

    offset = int(screen_h / 3)
    ph=game_sprites['pipe'][0].get_height()
    pipex=screen_w+200
    lower_y=offset+random.randrange(0,int(screen_h-game_sprites['base'].get_height()-1.2*offset))
    upper_y=ph-lower_y+offset
    pipe=[
        {
            'x':pipex,'y':-upper_y  #upper pipe
        },
        {
            'x': pipex, 'y': lower_y #lower pipe
        }
    ]
    return pipe

if __name__=="__main__":
    #let's start
    pygame.init()

    pygame.display.set_caption("Flappy bird by Poo")
    game_sprites['numbers']=(
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
    game_sprites['message']=pygame.image.load('flappy bird/welcome page.jpg').convert_alpha()
    game_sprites['base'] = pygame.image.load('flappy bird/base.jpg').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load('flappy bird/pipe_edited.jpg').convert_alpha(),180),
        pygame.image.load('flappy bird/pipe_edited.jpg').convert_alpha()
    )
    #game sounds
    game_sounds['regular']=pygame.mixer.Sound('flappy bird/Prop Plane Fly.mp3')
    game_sounds['hit']=pygame.mixer.Sound('flappy bird/Face Hit Series.mp3')

    game_sprites['back_ground']=pygame.image.load('flappy bird/background.png').convert()
    game_sprites['player'] = pygame.image.load(Player).convert_alpha()

    while True:
        welcome() #shows welcome screen until user press a button
        maingame()
