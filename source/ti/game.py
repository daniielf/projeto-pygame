import pygame

font = None
font_size = 25
gameRunning = True
clock = pygame.time.Clock()


class GameObject (pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y , width, height, obj_type):
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.collisionWidth = width
        self.collisionHeight = height
        
        self.objType = obj_type
        self.acceleration = 0
        self.direction = ""
        
        
class Player (GameObject, pygame.font.Font):
    def __init__(self, image, pos_x, pos_y, width, height, obj_type):
        GameObject.__init__(self,image,pos_x, pos_y ,width,height,0)

        self.cash = 0
        self.c_card = 0
        
        pygame.font.Font.__init__(self, font, font_size)
        
        
        self.cashLabel = self.render(str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))
        
    def moveUp(self):
        self.pos_y -= self.acceleration
       
        
    def moveDown(self):
        self.pos_y += self.acceleration
        
    def moveLeft(self):
        self.pos_x -= self.acceleration
        
    def moveRight(self):
        self.pos_x += self.acceleration
        
        
    def updateValues(self):
        self.cashLabel = self.render(str(self.cash),1,(0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))
        
    


class Game ():
    def __init__(self,screen):
        
        self.screen = screen
        self.width = screen.get_rect().width
        self.hieght = screen.get_rect().height
        self.bg_color = (255,255,255)
        #self.image
        self.player = Player("image", 15 , 15, 50 , 50, 0)
        
    
    def run(self):
        bob = self.player
        self.player.updateValues()
        #pygame.draw.rect(self.screen, (255,0,0) ,((bob.position),(bob.collisionWidth, bob.collisionHeight)),0)
        pygame.draw.rect(self.screen, (255,0,0) ,(bob.pos_x,bob.pos_y,40,40),0)
        gameRunning = True
        while (gameRunning):
            clock.tick(15)
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        gameRunning = False
                    elif (event.key == pygame.K_z): 
                        bob.cash += 1 
                        bob.updateValues()
                    elif (event.key == pygame.K_UP):
                        bob.acceleration = 20
                        bob.direction = "up"
                        print ("up")
                    elif (event.key == pygame.K_DOWN):
                        bob.acceleration = 20
                        bob.direction = "down"
                        print ("down")
                    elif (event.key == pygame.K_LEFT):
                        bob.acceleration = 20
                        bob.direction = "left"
                        print ("left")
                    elif (event.key == pygame.K_RIGHT):
                        bob.acceleration = 20
                        bob.direction = "right"
                if (event.type == pygame.KEYUP):
                    bob.acceleration = 0
            
            
            if (bob.direction == "up"):
                bob.moveUp()
                
            elif (bob.direction == "down"):
                bob.moveDown()
            elif (bob.direction == "left"):
                bob.moveLeft()        
            elif (bob.direction == "right"):
                bob.moveRight()        
                
            ##print (bob.direction)
            #pygame.draw.rect(self.screen, (255,0,0) ,((bob.position),(bob.collisionWidth, bob.collisionHeight)),0)
            self.screen.fill(self.bg_color)
            pygame.draw.rect(self.screen, (255,0,0), (bob.pos_x,bob.pos_y, bob.collisionWidth, bob.collisionHeight),0)
                
            
            
            # Player Interface Draw
            cash_x = 0
            cash_y = 0
            
            self.screen.blit (self.player.cashLabel, (cash_x,cash_y))
            
            cCard_x = self.width - self.player.c_cardLabel.get_rect().width
            cCard_y = 0
            
            self.screen.blit (self.player.c_cardLabel,(cCard_x,cCard_y))
            
            ##Display
            pygame.display.flip()