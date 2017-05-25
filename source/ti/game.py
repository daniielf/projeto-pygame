import pygame, random, objects, math
from pygame.locals import*


clock = pygame.time.Clock()
obstacles = []
cards_list = []
monster_list = []

pygame.mixer.init(44100, -16, 2, 2048)
go_sound = pygame.mixer.Sound("../media/sounds/go_sound.wav")
cash_sound = pygame.mixer.Sound("../media/sounds/cash_sound.wav")
card_sound = pygame.mixer.Sound("../media/sounds/card_sound.wav")
card_sound.set_volume(1.0)
go_sound.set_volume(0.8)
cash_sound.set_volume(0.8)

gameRunning = True

def dist(x1, y1, x2, y2):
    result = math.sqrt( math.pow((x1 - x2 ),2) + math.pow((y1 - y2), 2))
    result = math.floor(result)
    return result

class BackGround():
    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load('../media/sprites/background.png')

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
        if (score < 3):
            self.result += " ruim :("
        elif (score <= 3 and score <= 7):
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
            self.screen.blit (exitLabel, (0,650))
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
        self.image = pygame.image.load('../media/sprites/background.png')
        self.bg_color = (255,255,255)
        self.image
        self.player = objects.Player("image", 300 , 500, 50 , 50, 0)
        
    def drawBar(self,value, posX, posY):
        progress = value * 10
        if (progress == 100):
            color = (0,200,0)
        elif (progress > 70):
            color = (150,180,0)
        elif (progress > 50):
            color = (165,165,0)
        elif (progress > 30):
            color = (180,150,0)
        else:
            color = (200,0,0)
            
        
        pygame.draw.rect(self.screen, color, (posX, posY, progress, 20))
            
     
    def progressBars(self, player):
        progressCarbo = (player.carbohidrato/4)
        progressVege =  (player.vegetal/3)
        progressProte = (player.proteina/2)
        progressDoce =  (player.doce/1)
        
        self.drawBar(progressCarbo, 190, 610)
        self.drawBar(progressVege, 190, 640)
        self.drawBar(progressProte, 660, 610)
        self.drawBar(progressDoce, 660, 640)
        
    
    def run(self):
        main_music = pygame.mixer.music.load("../media/sounds/megalovania.wav")
        pygame.mixer.music.play()
        
        pygame.mixer.music.set_volume(0.6)
        
        bob = self.player
        
         # List to hold all the sprites
        all_sprite_list = pygame.sprite.Group()

        # Make the walls. (x_pos, y_pos, width, height)
        wall_list = pygame.sprite.Group()
        
        # List of Foods
        food_list = pygame.sprite.Group()

        wall = objects.Wall("", 0, 40, 10, 560, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)

        wall = objects.Wall("", 10, 40, 980, 10, 1)
        wall_list.add(wall)
        all_sprite_list.add(wall)
        obstacles.append(wall)
        
        wall = objects.Wall("", 990, 40, 10, 560, 1)
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
        
        ## ATM 
        atm_list = pygame.sprite.Group()
        atm = objects.ATM("",940, 45, 13, 35, 1)
        atm_list.add(atm)
        all_sprite_list.add(atm)
        
        
        ## Monsters
        monster_list = pygame.sprite.Group()
        
        fFood = objects.FastFood("", 850, 400, 30, 30, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        fFood2 = objects.FastFood("", 500, 130, 30, 30, 3)
        monster_list.add(fFood2)
        all_sprite_list.add(fFood2)
        
        fFood = objects.FastFood("", 270, 100, 30, 30, 3)
        monster_list.add(fFood)
        all_sprite_list.add(fFood)
        
        fFood = objects.FastFood("", 220, 450, 30, 30, 3)
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
        
        food_time = pygame.USEREVENT+4
        T4 = 8000 # 8 seconds
        pygame.time.set_timer(food_time, T4)
        
        cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
        
        bground = BackGround(self.screen)
        
        
        gameRunning = True
        
        while (gameRunning):
            self.screen.fill((255,255,255))
            self.screen.blit (self.image, (0,40))
            clock.tick(60)
            
            cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
            monster_hit_list = pygame.sprite.spritecollide(bob, monster_list, False)
            atm_hit_list = pygame.sprite.spritecollide(bob,atm_list,False)
            food_hit_list = pygame.sprite.spritecollide(bob,food_list,False)
            
            
            
            
          		          
            for atm in atm_hit_list:
                if(bob.direction == "up"):
                    bob.rect.top = atm.rect.bottom
                elif (bob.direction == "right"):
                    bob.rect.right = atm.rect.left
                elif (bob.direction == "left"):
                    bob.rect.left = atm.rect.right
        
            for monster in monster_hit_list:
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.Sound.play(go_sound)
                pygame.time.delay(3500)

                gameRunning = False
                
                
            for card in cards_hit_list:    
                bob.c_card += 1
                pygame.mixer.Sound.play(card_sound)
                cards_list.remove(card)
                all_sprite_list.remove(card)
                
            for food in food_hit_list:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and bob.cash >= food.value):
                    bob.buyFood(food)
                    food_list.empty()
                
            #####  FRAME EVENTS      
            ## Time Decrementer    
            for event in pygame.event.get():
                if (event.type == time_decrement):
                    bob.time -= 1
                    #bob.score += 1
                 
                
                if (event.type == food_time):
                    food_list.empty()
                    newFood1 = objects.Food(5, "vegetal")
                    food_list.add(newFood1)
                    
                    newFood2 = objects.Food(5, "carbohidrato")
                    food_list.add(newFood2)
                    
                    newFood3 = objects.Food(5, "doce")
                    food_list.add(newFood3)
                    
                    newFood4 = objects.Food(5, "proteina")
                    food_list.add(newFood4)
                    
                ## Credit Card Generator
                if (event.type == card_generator and len(cards_list) < 2):
                    cashGenerator = random.randint(0,100)
                    if (cashGenerator <= 35):
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
                    elif (event.key == pygame.K_RETURN):
                        if (dist(bob.rect.x,bob.rect.y,atm.rect.x, atm.rect.y) <= 65 and bob.c_card >= 1):
                            pygame.mixer.Sound.play(cash_sound)
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
            food_list.draw(self.screen)
            
            
            self.screen.blit (bob.timeLabel, (450,0))
            
            # Player Interface Draw
            cash_x = 0
            cash_y = 20
            
           
            self.screen.blit (bob.cashLabel, (cash_x,cash_y))
            
            cCard_x = 0
            cCard_y = 0
            
            self.screen.blit (bob.c_cardLabel,(cCard_x,cCard_y))
            
            self.screen.blit(bob.scoreLabel,(self.width - bob.scoreLabel.get_rect().width - 50, 0))
            
            ##BARS
            
            self.screen.blit(bob.carboLabel, (55, 610))
            self.screen.blit(bob.vegLabel, (30,640))
            self.screen.blit(bob.protLabel, (565,610))
            self.screen.blit(bob.doceLabel, (500,640))
            
            self.progressBars(bob)
            
            ##Display
            pygame.display.flip()
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("../media/sounds/crimson.wav")
        pygame.mixer.music.play()
        
        ge = GameEnd(self.screen)
        ge.defScore(bob.score)
        ge.defResult(bob.score)
        ge.run()
        #pygame.display.update()