# Source File Name: Bacterium_04.py
# Author's Name: Jacob Meikle
# Last Modified By: Jacob Meikle
# Date Last Modified: July 8, 2013
""" 
  Program Description:  This is a side-scroller game where the player controls a single bacteria in the blood
      stream and must infect as many red blood cells as possible while avoiding white blood cells.
      
  Version: 0.4 -  *Added sound.
                  *Added a game-end screen.
                  
  Version: 0.3 -  *Added White blood cells.
                  *Implemented pixel-perfect collisions for white blood cells.              
                  *You can now lose the game.  
      
      
  Version: 0.2 -  *Changed movement style of bacteria.
                  *Added a cursor.               
                  *Added Red Blood cells.                      

  Version: 0.1 -  *Start screen.
                  *Bacteria object that follows the mouse.               
                  *Scrolling background implemented.
"""
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 600))

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/cursor.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255)) 

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex,mousey)
      

class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bacterium.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.image.set_colorkey((255, 255, 255)) 
        self.rect.center = (200, 320)
        self.rect.inflate(-50,-50)
        
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndInfect = pygame.mixer.Sound("assets/infect.wav")
            self.sndDie = pygame.mixer.Sound("assets/die.wav")
            self.sndMusic = pygame.mixer.Sound("assets/music.wav")
            self.sndMusic.play(-1)

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        
        #buffer of 10 px to stop up or down movement
        if mousey > self.rect.centery + 5 or mousey < self.rect.centery - 5:
            if mousey > self.rect.centery:
                #moving down
                self.rect.centery += 1
                pygame.transform.rotate(self.image,10)
            else:
                #moving up
                self.rect.centery += -1
                pygame.transform.rotate(self.image,20)
     
              
class RedCell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/blood_cell.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        self.infected = False
        self.dy = -2
    
    def update(self):
        self.rect.centerx += self.dy
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.rect.centery = random.randrange(0, screen.get_height())
        self.rect.centerx = random.randrange(screen.get_width(), screen.get_width()*3)
        self.infected = False
        self.image = pygame.image.load("assets/blood_cell.gif")
        
    def infect(self):
        self.image = pygame.image.load("assets/infected_blood_cell.gif")
        self.infected = True
        

class WhiteCell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/white_blood_cell.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()
        self.dy = 0
        self.dx = -2 

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.right < 0:
            self.reset()
    
    def reset(self):
        self.rect.left = random.randrange(screen.get_width(), screen.get_width()*3) 
        self.rect.centery = random.randrange(0, screen.get_height())


    
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
        self.rect.left = 0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "lives: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("~~Bacterium~~")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    bacteria = Bacteria()
    
    cursor = Cursor()
    
    redCells = [ RedCell() for i in range(8)]
    
    whiteCells = [ WhiteCell() for i in range(6)]

    bloodStream = BloodStream()
    
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(bloodStream, redCells, bacteria, cursor)
    enemySprites = pygame.sprite.Group(whiteCells)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(68)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        #check collisions
        
        #blood cells (prevent cell stacking)
        for thiscell in redCells:
            for cell in redCells:
        
                if thiscell.rect.colliderect(cell.rect) and cell != thiscell:
                    cell.reset()
                    
        #white cells (prevent cell stacking) 
        for thiscell in whiteCells:
            for cell in whiteCells:
    
                if thiscell.rect.colliderect(cell.rect) and cell != thiscell:
                    cell.reset()
                    
        #bacteria
        for cell in redCells:
        
            if bacteria.rect.colliderect(cell.rect):
                if cell.infected == False:
                    bacteria.sndInfect.play()
                    scoreboard.score += 100
                    cell.infect()
            

        #white blood cell collision
        #check if sprites collide
        if pygame.sprite.spritecollide(bacteria, enemySprites, False):
                   
            hitWhites = pygame.sprite.spritecollide(bacteria, enemySprites, False, pygame.sprite.collide_mask)
            if hitWhites:
                bacteria.sndDie.play()
                scoreboard.lives -= 1
                if scoreboard.lives <= 0:
                    keepGoing = False
                for theCell in hitWhites:
                    theCell.reset()
        
        friendSprites.update()
        enemySprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        enemySprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()

    bacteria.sndMusic.stop()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score

def gameReport(score):
    pygame.display.set_caption("~~Bacterium~~")

    bacteria = Bacteria()
    bloodStream = BloodStream()
    
    allSprites = pygame.sprite.Group(bloodStream, bacteria)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Your Score Is: %d" % score ,
    "Good Job!",
    "Click to replay, or Esc to exit."

    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(66)
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
        
    #end music
    bacteria.sndMusic.stop()

    pygame.mouse.set_visible(True)
    return donePlaying


#Instructions Screen    
def instructions():
    pygame.display.set_caption("~~Bacterium~~")

    bacteria = Bacteria()
    bloodStream = BloodStream()
    
    allSprites = pygame.sprite.Group(bloodStream, bacteria)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Bacterium.",
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
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(66)
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
        
    #stop music
    bacteria.sndMusic.stop()

    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions()
        if not donePlaying:
            score = game()
            donePlaying = gameReport(score)


if __name__ == "__main__":
    main()
    
    
