import pygame

font = None
font_size = 25
gameRunning = True
clock = pygame.time.Clock()
obstacles = []
walls = []

class GameObject (pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y , width, height, obj_type):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        
        self.objType = obj_type
        self.acceleration = 0
        self.direction = ""
        
        
class Player (GameObject, pygame.font.Font):
    def __init__(self, image, pos_x, pos_y, width, height, obj_type):
        GameObject.__init__(self,image,pos_x, pos_y ,width,height,0)
        self.image.fill((255,0,0))
        self.cash = 0
        self.c_card = 0
        self.rect = pygame.Rect (500,300, 50,50)
        pygame.font.Font.__init__(self, font, font_size)
        
        self.walls = walls
        
        self.cashLabel = self.render(str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))
        
    def moveUp(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.top -= self.acceleration
        for wall in block_hit_list:
            if self.rect.top < wall.rect.bottom:
                self.rect.top = wall.rect.bottom
            else:
                self.rect.top -= self.acceleration
       
        
    def moveDown(self): 
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.bottom += self.acceleration
        #print len(block_hit_list)
        for wall in block_hit_list:
            if self.rect.bottom > wall.rect.top: 
                self.rect.bottom = wall.rect.top
            else:    
                self.rect.bottom += self.acceleration
        
    def moveLeft(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.left -= self.acceleration
        for wall in block_hit_list:
            if self.rect.left < wall.rect.right:
                self.rect.left = wall.rect.right              
            else:
                self.rect.left -= self.acceleration
        
    def moveRight(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.right += self.acceleration
        for wall in block_hit_list:
            if self.rect.right > wall.rect.left:
                self.rect.right = wall.rect.left
            else:
                self.rect.right += self.acceleration
        
        
    def updateValues(self):
        self.cashLabel = self.render(str(self.cash),1,(0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))
        

class Wall (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x,pos_y,width,height,1)
        
        obstacles.append(self)
        #self.image = pygame.Surface([width,height])
        
    
        
        
class Game ():
    def __init__(self,screen):
        
        self.screen = screen
        self.width = screen.get_rect().width
        self.hieght = screen.get_rect().height
        self.bg_color = (255,255,255)
        #self.image
        self.player = Player("image", 300 , 500, 50 , 50, 0)

        
        
    
    def run(self):
        bob = self.player
        
         # List to hold all the sprites
        all_sprite_list = pygame.sprite.Group()

        # Make the walls. (x_pos, y_pos, width, height)
        wall_list = pygame.sprite.Group()

        wall = Wall("", 0, 40, 10, 590, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)

        wall = Wall("", 10, 40, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)

        wall = Wall("", 10, 200, 300, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        
        wall = Wall("", 990, 40, 10, 590, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        
        wall = Wall("", 10, 590, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        
        bob.walls = wall_list
        all_sprite_list.add(bob)
        
        
        self.player.updateValues()
        #pygame.draw.rect(self.screen, (255,0,0) ,((bob.position),(bob.collisionWidth, bob.collisionHeight)),0)
        pygame.draw.rect(self.screen, (255,0,0) ,bob.rect,0)
        for wall in obstacles:
            pygame.draw.rect(self.screen, (0,0,0), wall.rect, 0)
        
        
        
        gameRunning = True
        while (gameRunning):
            clock.tick(60)
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    
                    if (event.key == pygame.K_ESCAPE):
                        gameRunning = False
                    elif (event.key == pygame.K_z): 
                        bob.cash += 1 
                        bob.updateValues()
                        bob.rect.x = 480
                        bob.rect.y = 280
                    elif (event.key == pygame.K_UP):
                        bob.acceleration = 5
                        bob.direction = "up"
                       
                    elif (event.key == pygame.K_DOWN):
                        bob.acceleration = 5
                        bob.direction = "down"
                        
                    elif (event.key == pygame.K_LEFT):
                        bob.acceleration = 5
                        bob.direction = "left"
                        
                    elif (event.key == pygame.K_RIGHT):
                        bob.acceleration = 5    
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
            all_sprite_list.update()
            self.screen.fill((255,255,255))
            all_sprite_list.draw(self.screen)
            
            #print len(pygame.sprite.spritecollide(bob, bob.walls, False))
            
            # Player Interface Draw
            cash_x = 0
            cash_y = 0
            
            self.screen.blit (self.player.cashLabel, (cash_x,cash_y))
            
            cCard_x = self.width - self.player.c_cardLabel.get_rect().width
            cCard_y = 0
            
            self.screen.blit (self.player.c_cardLabel,(cCard_x,cCard_y))
            
            ##Display
            pygame.display.flip()