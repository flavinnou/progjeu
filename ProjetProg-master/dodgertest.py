import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 900
WINDOWHEIGHT = 600
WINDOWHEIGHTWINDOWWIDTH, WINDOWHEIGHTWINDOWHEIGHT= WINDOWWIDTH /2 , WINDOWHEIGHT/2 ##pour fond défilant define display surface
AREA = WINDOWWIDTH*WINDOWHEIGHT ## pour fond défilant define display surface
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)


FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return


# faire bulletRect pour les hitboxes de la balle qui touche, ensuite créer une bullet qui serra un baddies
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

BACKGROUND = pygame.image.load("background.png").convert() ### background pour le fond défilant on le met là car il faut le pygame.init en dessus
a=0

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
font2= pygame.font.SysFont("Courier",75)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
bulletImage = pygame.image.load("gift.png")
#bulletRect = pygameImage.get_rect()
playerImage = pygame.image.load('perenoel.jpeg')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('pinguin.jpeg')

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Santawars', font2, windowSurface, (WINDOWWIDTH / 3.5), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.68) - 50, (WINDOWHEIGHT / 3) + 200)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
### fonction fond défilant
def events():
    for event in pygame.event.get():
        if event.type==QUIT: ### j'ai essayé d'enlever qqch
            pygame.quit()
            sys.exit()

#create projectile class for the bullets in game
class projectile(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = 3
        self.vel = 8

    def draw(self, win):
        pygame.draw.circle(win, (self.x,self.y), self.radius)
        #je le mets ici pour m'inspirer plus tard
        #newBaddie = {
            #'rect': pygame.Rect((WINDOWWIDTH - baddieSize), random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize,
                            #    baddieSize),
           # 'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
        #    'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
         #   }
def redrawGameWindow():
    win.blit(bg, (0,0))
    playerImage.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
bullets = []
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH -900, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.

        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect((WINDOWWIDTH - baddieSize), random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(-b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(-5, 0)
            elif slowCheat:
                b['rect'].move_ip(1, 0)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWWIDTH:
                baddies.remove(b)
        #shoot the bullets
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullets.append(
                projectile(round(playerRect.x + playerRect.width // 2), round(playerRect.y + playerRect.height // 2) , 1))
        # Draw the game world on the window.
        events() ##met le fond de la fenêtre

        rel_x = a % BACKGROUND.get_rect().width
        windowSurface.blit(BACKGROUND, (rel_x - BACKGROUND.get_rect().width, 0))
        if rel_x < WINDOWWIDTH:
            windowSurface.blit(BACKGROUND, (rel_x, 0))
        a -= 1


        mainClock.tick(FPS)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update() ##attention tjrs garder à la fin des image que l'on importe comme cela fait qu'une fois le display update

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()