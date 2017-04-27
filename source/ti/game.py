import pygame, random, objects
from pygame.locals import*


clock = pygame.time.Clock()
obstacles = []
cards_list = []
monster_list = []

pygame.mixer.init(44100, -16, 2, 2048)
go_sound = pygame.mixer.Sound("../media/go_sound.wav")
go_sound.set_volume(0.3)

gameRunning = True

class BackGround():
    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load('../media/background.png')

class GameEnd(pygame.font.Font):
    def __init__(self, screen, bg_color=(0,0,0), font=None, font_size=40):
        self.screen = screen
        self.width = screen.get_rect().width
        self.height = screen.get_rect().height
        self.bg_color = (0,0,0)
        pygame.font.Font.__init__(self, None, 40)
        
        
        self.textFont = pygame.font.SysFont(font,font_size)
        self.exitFont = pygame.font.SysFont(font,20)
        
        self.text = "Pontuacao: "  
        self.result = "Resultado: "
        
        
    def defScore(self, score):
        self.text += str(score)
        self.textLabel = self.textFont.render(self.text, 1, (255,255,255))
        
    def defResult(self, score):
        if (score < 50):
            self.result += " ruim :("
        elif (score <= 50 and score < 80):
            self.result += " bom :)"
        else:
            self.result += " otimo :D"
            
        self.resultLabel = self.textFont.render(self.result, 1, (255,255,255))
            
    def run(self):
        running = True
        #pygame.display.update()
        while (running):
            clock.tick(60)
            self.screen.fill(self.bg_color)
            self.screen.blit (self.textLabel, (380,250))
            self.screen.blit (self.resultLabel, (380,300))
            exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
            self.screen.blit (exitLabel, (0,580))
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        running = False
            pygame.display.flip()
        
class Game ():
    def __init__(self,screen):
        
        self.screen = screen
        self.width = screen.get_rect().width
        self.height = screen.get_rect().height
        self.image = pygame.image.load('../media/background.png')
        self.bg_color = (255,255,255)
        self.image
        self.player = objects.Player("image", 300 , 500, 50 , 50, 0)
     
    
    def run(self):
        main_music = pygame.mixer.music.load("../media/megalovania.mp3")
        pygame.mixer.music.play()
        
        bob = self.player
        
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
        
        wall = objects.Wall("", 990, 40, 10, 590, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 10, 590, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        
        ## Gondulas
        wall = objects.Wall("", 100, 200, 226, 40, 8)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 100, 400, 226, 40, 8)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 620, 200, 226, 40, 8)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 620, 400, 226, 40, 8)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 450, 220, 40, 226, 9)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        
        ## Monsters
        monster_list = pygame.sprite.Group()
        
        fFood = objects.FastFood("", 850, 400, 30, 30, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        fFood2 = objects.FastFood("", 500, 130, 30, 30, 3)
        monster_list.add(fFood2)
        all_sprite_list.add(fFood2)
        
        fFood = objects.FastFood("", 100, 100, 30, 30, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        fFood = objects.FastFood("", 270, 450, 30, 30, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        fFood = objects.FastFood("", 450, 470, 30, 30, 4)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        ##
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
        T3 = 100 # 0,1 second
        pygame.time.set_timer(monster_move, T3)
        
        cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
        
        bground = BackGround(self.screen)
        
        
        gameRunning = True
        
        while (gameRunning):
            self.screen.fill((255,255,255))
            self.screen.blit (self.image, (0,40))
            clock.tick(60)
            
            cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
            monster_hit_list = pygame.sprite.spritecollide(bob, monster_list, False)
            
        
            for monster in monster_hit_list:
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.Sound.play(go_sound)
                pygame.time.delay(1500)

                gameRunning = False
                
                
            for card in cards_hit_list:    
                bob.c_card += 1
                cards_list.remove(card)
                all_sprite_list.remove(card)
                
            #####  FRAME EVENTS      
            ## Time Decrementer    
            for event in pygame.event.get():
                if (event.type == time_decrement):
                    bob.time -= 1
                 
                ## Credit Card Generator
                if (event.type == card_generator and len(cards_list) < 5):
                    cashGenerator = random.randint(0,100)
                    if (cashGenerator <= 10):
                        x = random.randint(50,800)
                        y = random.randint(50,400)
                        cash = objects.Cash("",x,y,20,20,2)
                        cards_list.append(cash)
                        pygame.draw.rect(self.screen, (0,255,0), cash.rect , 0)
                        all_sprite_list.add(cash)

                ## Monster Movement        
                if (event.type == monster_move):
                    for monster in monster_list:
                        monsterCollision = pygame.sprite.spritecollide(monster, wall_list, False)
                        if(monster.movingPositive):
                            if (len(monsterCollision) == 0):
                                if monster.obj_type == 4:
                                    monster.rect.left -= 15
                                else:
                                    monster.rect.top -= 15
                            else:
                                if monster.obj_type == 4:
                                    monster.rect.right += 15
                                    monster.movingPositive = False
                                else:
                                    monster.rect.bottom += 15
                                    monster.movingPositive = False
                        else:
                            if (len(monsterCollision) == 0):
                                if monster.obj_type == 4:
                                    monster.rect.right += 15
                                else:
                                    monster.rect.bottom += 15
                            else:
                                if monster.obj_type == 4:
                                    monster.rect.left -= 15
                                    monster.movingPositive = True
                                else:
                                    monster.rect.top -= 15
                                    monster.movingPositive = True
                    
                   
                ## Player Input
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
  
            
            #self.screen.fill((255,255,255))
           
            all_sprite_list.update()
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
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("../media/crimson.mp3")
        pygame.mixer.music.play()
        
        ge = GameEnd(self.screen)
        ge.defScore(bob.cash)
        ge.defResult(bob.cash)
        ge.run()
        #pygame.display.update()