import pygame
from pygame.locals import*

font = None
font_size = 25
walls = []
obstacles = []
cards_list = []

class GameObject (pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y , width, height, obj_type):
        
        pygame.sprite.Sprite.__init__(self)
        
        
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        
        self.obj_type = obj_type
        self.acceleration = 0
        self.direction = ""
        
        
class Player (GameObject, pygame.font.Font):
    def __init__(self, image, pos_x, pos_y, width, height, obj_type):
        GameObject.__init__(self,image,pos_x, pos_y ,width,height,0)
        self.image = pygame.image.load('../media/bob_cima.png')
        self.cash = 0
        self.c_card = 0
        self.time = 180
        
        self.rect = pygame.Rect (500,300, 30,30)
        pygame.font.Font.__init__(self, font, font_size)
        
        self.walls = walls
        
        self.timeLabel = self.render("Tempo:" + str(self.time), 1, (0,0,0))
        self.cashLabel = self.render("Dinheiro:" + str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render("Cartoes:" + str(self.c_card),1,(0,0,0))
        
    def moveUp(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/bob_cima.png')
        self.rect.top -= self.acceleration
        for wall in block_hit_list:
            if self.rect.top - 10 < wall.rect.bottom:          
                self.rect.top = wall.rect.bottom
            else:
                self.rect.top -= self.acceleration
       
        
    def moveDown(self): 
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        
        self.image = pygame.image.load('../media/bob_baixo.png')
        self.rect.bottom += self.acceleration
        #print len(block_hit_list)
        for wall in block_hit_list:
            if self.rect.bottom + 10> wall.rect.top:          
                self.rect.bottom = wall.rect.top
            else:    
                self.rect.bottom += self.acceleration          
        
    def moveLeft(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/bob_esquerda.png')
        self.rect.left -= self.acceleration
        for wall in block_hit_list:
            if self.rect.left - 10 < wall.rect.right:            
                self.rect.left = wall.rect.right              
            else:
                self.rect.left -= self.acceleration
        
    def moveRight(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/bob_direita.png')
        self.rect.right += self.acceleration
        for wall in block_hit_list:
            if self.rect.right + 10> wall.rect.left:          
                self.rect.right = wall.rect.left
            else:
                self.rect.right += self.acceleration
        
        
    def updateValues(self):
        self.timeLabel = self.render("Tempo:" + str(self.time), 1, (0,0,0))
        self.cashLabel = self.render("Dinheiro:" + str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render("Cartoes:" + str(self.c_card), 1, (0,0,0))
        

class Wall (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x,pos_y,width,height,obj_type)
        if (obj_type == 8):
            self.image = pygame.image.load('../media/gondula-x.png')
        elif (obj_type == 9):
            self.image = pygame.image.load('../media/gondula-y.png')
        
        #obstacles.append(self)
        #self.image = pygame.Surface([width,height])
        

        
class Cash (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x ,pos_y , width, height, 2)
        
        self.image.fill((0,255,0))
        #cards_list.append(self)
    

class FastFood (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x,pos_y, width, height, obj_type)
        
        self.image = pygame.image.load('../media/steve.png')
        self.rect = pygame.Rect (pos_x, pos_y, 32,40)
        self.movingPositive = True
        #self.image = pygame.image.load('../media/bob_cima.png')
        