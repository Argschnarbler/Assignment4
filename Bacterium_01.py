# Source File Name: Bacterium_01.py
# Author's Name: Jacob Meikle
# Last Modified By: Jacob Meikle
# Date Last Modified: June 25, 2013
""" 
  Program Description:  This is a side-scroller game where the player controls a single bacteria in the blood
      stream and must infect as many red blood cells as possible while avoiding white blood cells.
                        

  Version: 0.1 -  *Start screen.
                  *Bacteria object that follows the mouse.               
                  *Scrolling background implemented.
"""
    
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bacterium.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255)) 
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)

class BloodStream(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bg.jpg")
        self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.dx = 1
        self.reset()
        
    def update(self):
        self.rect.left -= self.dx
        if self.rect.left <= -3200:
            self.reset() 
    
    def reset(self):
        print 'reset'
        self.rect.left = 0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "lives: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("~~Bacterium~~")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    bacteria = Bacteria()

    bloodStream = BloodStream()
    
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(bloodStream, bacteria)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        friendSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    

    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("~~Bacterium~~")

    bacteria = Bacteria()
    bloodStream = BloodStream()
    
    allSprites = pygame.sprite.Group(bloodStream, bacteria)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Bacterium.     Last score: %d" % score ,
    "Instructions:  You are a single bacterium,",
    "infecting the blood stream.",
    "",
    "Touch red blood cells to infect them.",
    "Beware of white blood cells,",    
    "They will eat you.",
    "Steer with the mouse.",
    "",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()

    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
