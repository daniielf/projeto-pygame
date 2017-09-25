#!/usr/bin/env python
from datetime import datetime

import math
import objects
import pygame
import random
import avalgame
import log
from pygame.locals import *
from pygaze import libtime  # Obter a latencia do usuario em relacao aos estimulos
from pygaze.eyetracker import EyeTracker

clock = pygame.time.Clock()
obstacles = []
cards_list = []
monster_list = []

pygame.mixer.init(44100, -16, 2, 2048)
go_sound = pygame.mixer.Sound("media/sounds/go_sound.wav")
cash_sound = pygame.mixer.Sound("media/sounds/cash_sound.wav")
card_sound = pygame.mixer.Sound("media/sounds/card_sound.wav")
card_sound.set_volume(1.0)
go_sound.set_volume(0.8)
cash_sound.set_volume(0.8)

gameRunning = True

def dist(x1, y1, x2, y2):
    result = math.sqrt(math.pow((x1 - x2 ),2) + math.pow((y1 - y2), 2))
    result = math.floor(result)
    return result

class BackGround():
    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load('media/sprites/background.png')


class GameEnd(pygame.font.Font):
    def __init__(self, screen, display ,bg_color=(0,0,0), font='media/fonts/arial.ttf', font_size=40):
        self.screen = screen.screen
        self.canvas = screen
        self.disp = display
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.bg_color = (0,0,0)
        pygame.font.Font.__init__(self, 'media/fonts/arial.ttf', 40)
        self.avalgame = avalgame.Avalgame()


        self.textFont = pygame.font.Font(font,font_size)
        self.exitFont = pygame.font.Font(font,20)

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
        self.screen.fill(self.bg_color)
        self.screen.blit(self.textLabel, (380,250))
        self.screen.blit(self.resultLabel, (380,300))
        exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
        self.screen.blit(exitLabel, (0,650))
        # self.logTheData()
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
            self.disp.fill(self)
            self.disp.show()
###injetar aqui



class Game ():
    def __init__(self,screen,display, avalgame = 0):
        self.avalgame = avalgame
        self.dataStore = log.GenerateInfo()
        self.disp = display
        self.canvas = screen
        self.screen = screen.screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.image = pygame.image.load('media/sprites/background.png')
        self.bg_color = (255,255,255)
        self.player = objects.Player("image", 300, 500, 50, 50, 0)
        self.startTime = datetime.now()

    def drawBar(self,value, posX, posY):
        progress = value * 10
        if (progress == 100):
            color = (0,200,0)
            self.avalgame.comp("C", 88)
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
        # f = open("testeFile.txt", 'w')
        # f.writelines([])
        dt = datetime.now()
        #Eye tracker configure
        eyetracker = EyeTracker(self.disp)
        eyetracker.calibrate()
        self.disp.fill(self.canvas)
        self.disp.show()
        #self.disp.mousevis = True

        eyetracker.start_recording()

        etObject = objects.EyeTracker(0, 0, 20, 20)

        ##END

        main_music = pygame.mixer.music.load("media/sounds/megalovania.wav")
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
        atm = objects.ATM("", 940, 45, 13, 35, 1)
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

        eyeTracker_time = pygame.USEREVENT+5
        T5 = 1000 # 1 seconds
        pygame.time.set_timer(eyeTracker_time, T5)

        logRecord_time = pygame.USEREVENT+6
        T6 = 1000 # 1 seconds
        pygame.time.set_timer(logRecord_time, T6)

        #gravar tempo que comeca uma fixacao
        logRecord_fixation = pygame.USEREVENT+7
        T7 = 1000 #2seconds
        pygame.time.set_timer(logRecord_fixation, T7)




        cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)

        bground = BackGround(self.screen)

        cont_blinks = 0
        gameRunning = True
        staring = False
        position = 0

        blinkCount = 0
        lastBlinkPos = (0,0)

        #comeco do game
        while (gameRunning):


            self.canvas.clear()
            self.screen.fill((255,255,255))
            self.screen.blit (self.image, (0,40))
            clock.tick(60)


            cards_hit_list = pygame.sprite.spritecollide(bob, cards_list, False)
            monster_hit_list = pygame.sprite.spritecollide(bob, monster_list, False)
            atm_hit_list = pygame.sprite.spritecollide(bob,atm_list,False)
            food_hit_list = pygame.sprite.spritecollide(bob,food_list,False)

            etSawList = pygame.sprite.spritecollide(etObject,food_list,False)



            if (len(etSawList) == 0):
                staring = False

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
                #self.avalgame.storeCreditCollection(self.startTime)

            for food in food_hit_list:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and bob.cash >= food.value):
                    bob.buyFood(food)
                    food_list.empty()
                    self.player.total_produtos += 1


            #####  FRAME EVENTS
            ## Time Decrementer
            for event in pygame.event.get():
                if (event.type == time_decrement):
                    bob.time -= 1
                    #bob.score += 1
                if (event.type == eyeTracker_time):
                    #verificar se houve fixacao
                    time = libtime.get_time()
                    getX, getY = eyetracker.sample()
                    self.dataStore.get_quadrant((getX, getY))
                    self.dataStore.start_fixation((getX, getY))

                # if(event.type == logRecord_fixation):
                #     #verificar fixacao
                #     if eyetracker.wait_for_fixation_start():
                #         pos_tup = ()
                #         start_time_fix, pos_tup = eyetracker.wait_for_fixation_start()
                #         start_time_fix = str(start_time_fix)
                #         etObject.startFixation(start_time_fix, pos_tup)

                if (event.type == logRecord_time):
                    etObject.setPosition(eyetracker.sample())
                    for food in etSawList:
                        self.dataStore.start_staring(food.food_type)

                # if (event.type == MOUSEBUTTONDOWN):
                #     start_time = eyetracker.wait_for_event(3)
                #     time_end = eyetracker.wait_for_event(4)
                #     cont_blinks += 1
                    # self.dataStore.start_blinking(str(cont_blinks), start_time, time_end)

                if (event.type == MOUSEBUTTONDOWN):
                    start_time = eyetracker.wait_for_event(3)
                    time_end = eyetracker.wait_for_event(4)
                #     cont_blinks += 1
                    self.dataStore.start_blinking(str(cont_blinks), start_time, time_end)

                    tracker_pos = eyetracker.sample()
                    if (tracker_pos != lastBlinkPos):
                        self.dataStore.start_blinkingTest(lastBlinkPos, blinkCount)
                        lastBlinkPos = tracker_pos
                        blinkCount = 1
                    else:
                        blinkCount += 1

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
                    if (cashGenerator <= 100):
                        x = random.randint(50,800)
                        y = random.randint(50,400)
                        cash = objects.Cash("", x, y, 20, 20, 2)
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
                            self.player.cashTotal +=15

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

            self.screen.blit(bob.scoreLabel,(1000 - bob.scoreLabel.get_rect().width - 50, 0))

            ##BARS

            self.screen.blit(bob.carboLabel, (55, 610))
            self.screen.blit(bob.vegLabel, (30,640))
            self.screen.blit(bob.protLabel, (565,610))
            self.screen.blit(bob.doceLabel, (500,640))

            self.progressBars(bob)


            ##Display
            #pygame.display.flip()
            self.disp.fill(self.canvas)
            self.disp.show()


        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("media/sounds/crimson.wav")
        pygame.mixer.music.play()

        pyramidCompletion = 0.0
        if (self.player.doce == 10):
            pyramidCompletion += 2.5
        if (self.player.proteina == 20):
            pyramidCompletion += 2.5
        if (self.player.vegetal == 30):
            pyramidCompletion += 2.5
        if (self.player.carbohidrato == 40):
            pyramidCompletion += 2.5

        self.avalgame.storePyramidCompletion(self.startTime, valor_AEEJ=pyramidCompletion)

        foodTotal=0
        if (0 < self.player.total_produtos <= 5):
            foodTotal = 1
        elif ( 5 < self.player.total_produtos <= 10):
            foodTotal = 2
        elif (self.player.total_produtos > 10):
            foodTotal = 3
        self.avalgame.storeFoodQuantity(self.startTime, valor_AEEJ=foodTotal)

        if self.player.cashTotal == 0:
            averageScore = 0
        else:
            averageScore = float(float(self.player.total_produtos)/float(self.player.cashTotal))*100

        self.avalgame.storeAverageScore(self.startTime, valor_AEEJ=averageScore)

        self.dataStore.start_blinkingTest(lastBlinkPos, blinkCount)
        self.dataStore.log_gen.recordBlinkLog(self.dataStore.blink_log, 'blink-', 4, self.avalgame._playerCode)
        self.dataStore.log_gen.recordLog(self.dataStore.blink_log2, 'blink2-', 4, self.avalgame._playerCode)
        self.dataStore.log_gen.recordLog(self.dataStore.staring_log, 'products-', 3, self.avalgame._playerCode)
        self.dataStore.log_gen.recordLog(self.dataStore.quadrant_log, 'quadrants', 2, self.avalgame._playerCode)
        self.dataStore.log_gen.recordLog(self.dataStore.position_log, 'fixation-', 1, self.avalgame._playerCode)

        ge = GameEnd(self.canvas, self.disp)

        ge.defScore(bob.score)
        ge.defResult(bob.score)
        #ge.storeData(etObject.log)
        #ge.storeData2(etObject.log2)
        #ge.storeDataBlink(etObject.log_blink)
        #ge.storeDataFixation(etObject.log_fixation)

        ge.run()
        #pygame.display.update()
