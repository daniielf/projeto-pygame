import pygame, random, objects
from pygame.locals import*


clock = pygame.time.Clock()
obstacles = []
cards_list = []
monster_list = []

gameRunning = True

class GameEnd(pygame.font.Font):
    def __init__(self,screen):
        self.screen = screen
        self.width = screen.get_rect().width
        self.height = screen.get_rect().height
        self.bg_color = (0,0,0)
        pygame.font.Font.__init__(self, None, 25)
        self.text = ""
        self.textLabel = self.render(self.text, 1, (255,255,255))
        
    def endText(self):
         self.timeLabel = self.render(self.text, 1, (255,255,255))
        
class Game ():
    def __init__(self,screen):
        
        self.screen = screen
        self.width = screen.get_rect().width
        self.height = screen.get_rect().height
        self.bg_color = (255,255,255)
        #self.image
        self.player = objects.Player("image", 300 , 500, 50 , 50, 0)
     
    
    def run(self):
        bob = self.player
        end = GameEnd(self.screen)
        
         # List to hold all the sprites
        all_sprite_list = pygame.sprite.Group()

        # Make the walls. (x_pos, y_pos, width, height)
        wall_list = pygame.sprite.Group()

        wall = objects.Wall("", 0, 40, 10, 590, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)

        wall = objects.Wall("", 10, 40, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)

        wall = objects.Wall("", 10, 200, 300, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 990, 40, 10, 590, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 10, 590, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        monster_list = pygame.sprite.Group()
        
        fFood = objects.FastFood("", 400, 400, 40,40, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        bob.walls = wall_list
        all_sprite_list.add(bob)
        
        
        bob.updateValues()
        #pygame.draw.rect(self.screen, (255,0,0) ,((bob.position),(bob.collisionWidth, bob.collisionHeight)),0)
        pygame.draw.rect(self.screen, (255,0,0) ,bob.rect,0)
        for wall in obstacles:
            pygame.draw.rect(self.screen, (0,0,0), wall.rect, 0)
        
        time_decrement = pygame.USEREVENT+1
        T1 = 1000 # second
        pygame.time.set_timer(time_decrement, T1)
    
        card_generator = pygame.USEREVENT+2
        T2 = 4000 # 4 second
        pygame.time.set_timer(card_generator, T2)
        
        monster_move = pygame.USEREVENT+3
        T3 = 500 # 1,5 second
        pygame.time.set_timer(monster_move, T3)
        
        cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
        
        gameRunning = True
        while (gameRunning):
            clock.tick(60)
            
            cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
            monster_hit_list = pygame.sprite.spritecollide(bob, monster_list, False)
        
            for monster in monster_hit_list:
                #end.text = "Derrota"
                #end.endText()
                gameRunning = False
                
                
            for card in cards_hit_list:    
                bob.c_card += 1
                cards_list.remove(card)
                all_sprite_list.remove(card)
                
                
                
            for event in pygame.event.get():
                if (event.type == time_decrement):
                    bob.time -= 1
                    
                if (event.type == card_generator and len(cards_list) < 5):
                    cashGenerator = random.randint(0,100)
                    if (cashGenerator <= 10):
                        x = random.randint(50,800)
                        y = random.randint(50,400)
                        cash = objects.Cash("",x,y,20,20,2)
                        cards_list.append(cash)
                        pygame.draw.rect(self.screen, (0,255,0), cash.rect , 0)
                        all_sprite_list.add(cash)

                        
                if (event.type == monster_move):
                    direction = random.randint(0,4)
                    if (direction == 0 and fFood.rect.top + 20 >= 30):
                        fFood.rect.top -= 20
                    if (direction == 1 and fFood.rect.bottom + 20 <= 570):
                        print (fFood.rect.bottom)
                        fFood.rect.bottom += 20
                    if (direction == 2 and fFood.rect.left + 20 >= 30):
                        fFood.rect.left -= 20
                    if (direction == 3 and fFood.rect.right + 20 <= 970):
                        fFood.rect.right += 20
                    
                if (event.type == pygame.KEYDOWN):
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    if (event.key == pygame.K_ESCAPE):
                        gameRunning = False
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
                        
                    elif (event.key == pygame.K_RETURN and bob.c_card > 0):
                        bob.c_card -= 1
                        bob.cash += 15

                if (event.type == pygame.KEYUP):
                    bob.acceleration = 0
                    pygame.event.set_allowed(pygame.KEYDOWN)
            
            bob.updateValues()
            
            
            if (bob.direction == "up"):
                bob.moveUp()
            elif (bob.direction == "down"):
                bob.moveDown()
            elif (bob.direction == "left"):
                bob.moveLeft()        
            elif (bob.direction == "right"):
                bob.moveRight()        
                
                
            if bob.time <= 0:
                #end.text = "Vitoria"
                #end.endText()
                gameRunning = False

            
            
            
            all_sprite_list.update()
            self.screen.fill((255,255,255))
            all_sprite_list.draw(self.screen)
            
           
            
            self.screen.blit (bob.timeLabel, (450,0))
            # Player Interface Draw
            cash_x = 0
            cash_y = 0
            
           
            self.screen.blit (bob.cashLabel, (cash_x,cash_y))
            
            cCard_x = self.width - bob.c_cardLabel.get_rect().width - 50
            cCard_y = 0
            
            self.screen.blit (bob.c_cardLabel,(cCard_x,cCard_y))
            
            ##Display
            pygame.display.flip()
												