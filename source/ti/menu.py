#!/usr/bin/env python
# from psychopy import *
import game
import pygame
import avalgame
import text_input
from pygaze.eyetracker import EyeTracker
from pygaze.libscreen import Screen, Display
from pygame.display import list_modes
print list_modes()

pygame.init()
disp = Display()
clock = pygame.time.Clock()
### Definitions
######  Resolution
#win_size = pygame.display.Info()
#windowSize = pygame.display.set_mode((win_size.current_w, win_size.current_h), pygame.FULLSCREEN)  # Change as you want (MUST RESPECT DISPLAY DIMENSIONS)
windowSize = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
running = True


version = "v1.00"
avalgame = avalgame.Avalgame()	


class GameSettings(pygame.font.Font):
    def __init__(self, screen, display ,bg_color=(0,0,0), font='media/fonts/arial.ttf',
    font_size=40, avalgame=None):
        self.avalgame = avalgame
        self.screen = screen.screen
        self.canvas = screen
        self.disp = display
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.bg_color = bg_color
        pygame.font.Font.__init__(self, font, 40)


        self.textFont = pygame.font.Font(font,font_size)
        self.exitFont = pygame.font.Font(font,20)

        self.text = "Pontuacao: "
        self.result = "Resultado: "

        self.buttonOk = MenuItem("Ok", 100)
        self.buttonCancel = MenuItem("Cancelar", 100)

        self.dataToLog = []

    def defScore(self, score):
        self.text += str(score)
        self.textLabel = self.textFont.render(self.text, 1, (255,255,255))

    def storeData(self,array):
        self.dataToLog = array

    def logTheData(self):
        for data in self.dataToLog:
            self.log.write([data])

    def run(self):
        eyetracker = EyeTracker(disp)
        eyetracker.calibrate()

        running = True

        self.textinput =text_input.TextInput(text_color=(255, 255, 255),
        cursor_color=(255, 255, 255), literal_number=True)
        if self.avalgame._code is not None:
            self.textinput.input_string = str(self.avalgame._code)
            self.textinput.cursor_position = len(str(self.avalgame._code))

        self.text1 = self.textFont.render("Configuracoes", 1, (255,255,255))
        self.text2 = self.textFont.render("Codigo do jogo", 1, (255,255,255))
        #pygame.display.update()
        self.screen.fill(self.bg_color)
        self.screen.blit (self.text1, (380,250))
        self.screen.blit (self.text2, (380,300))
        exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
        self.screen.blit (exitLabel, (0,650))
        self.logTheData()
        self.buttonOk.set_position(380,400)
        self.buttonCancel.set_position(450,400)

        while (running):
            clock.tick(60)
            self.screen.fill(self.bg_color)
            self.screen.blit (self.text1, (380,250))
            self.screen.blit (self.text2, (380,300))
            exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
            self.screen.blit (exitLabel, (0,650))

            events = pygame.event.get()

            self.textinput.update(events)
            self.screen.blit(self.textinput.get_surface(), (380, 350))
            pygame.display.update()

            if self.buttonOk.is_mouse_over(pygame.mouse.get_pos()):
                self.buttonOk.set_font_color((255, 0, 0))
                if ((1,0,0) == pygame.mouse.get_pressed()):
                    if self.textinput.get_text() != '':
                        self.avalgame.install( True, int(self.textinput.get_text()))
                    else:
                        self.avalgame.install( False, 0)

                    running = False
            else:
                self.buttonOk.set_font_color((255, 255, 255))

            if self.buttonCancel.is_mouse_over(pygame.mouse.get_pos()):
                self.buttonCancel.set_font_color((255, 0, 0))
                if ((1,0,0) == pygame.mouse.get_pressed()):
                    running = False
            else:
                self.buttonCancel.set_font_color((255, 255, 255))

            for event in events:
                if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        #print(self.textinput.get_text())
                        running = False


            self.screen.blit(self.buttonOk.label, self.buttonOk.position)
            self.screen.blit(self.buttonCancel.label, self.buttonCancel.position)

            x,y = eyetracker.sample()
            self.canvas.draw_circle(colour=(255,0,0),pos=(x,y), r=5 ,fill=True)

            self.disp.fill(self)
            self.disp.show()


class SetGamerId(pygame.font.Font):
    def __init__(self, screen, display ,bg_color=(0,0,0), font='media/fonts/arial.ttf',
    font_size=40, avalgame= None):
        self.avalgame = avalgame
        self.screen = screen.screen
        self.canvas = screen
        self.disp = display
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.bg_color = bg_color
        pygame.font.Font.__init__(self, None, 40)
        


        self.textFont = pygame.font.Font(font,font_size)
        self.exitFont = pygame.font.Font(font,20)

        self.buttonOk = MenuItem("Ok", 100)
        self.buttonCancel = MenuItem("Cancelar", 100)

        self.dataToLog = []

    def defScore(self, score):
        self.text += str(score)
        self.textLabel = self.textFont.render(self.text, 1, (255,255,255))

    def storeData(self,array):
        self.dataToLog = array

    def logTheData(self):
        for data in self.dataToLog:
            self.log.write([data])

    def run(self):
        eyetracker = EyeTracker(disp)
        eyetracker.calibrate()

        running = True

        self.textinput =text_input.TextInput(text_color=(255, 255, 255),
        cursor_color=(255, 255, 255), literal_number=True)

        self.text2 = self.textFont.render("Matricula do Jogador", 1, (255,255,255))
        #pygame.display.update()
        self.screen.fill(self.bg_color)

        self.screen.blit (self.text2, (380,300))
        exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
        self.screen.blit (exitLabel, (0,650))
        self.logTheData()
        self.buttonOk.set_position(380,400)
        self.buttonCancel.set_position(450,400)

        while (running):
            clock.tick(60)
            self.screen.fill(self.bg_color)

            self.screen.blit (self.text2, (380,300))
            exitLabel = self.exitFont.render("ESC para sair", 1, (255,255,255))
            self.screen.blit (exitLabel, (0,650))

            events = pygame.event.get()

            self.textinput.update(events)
            self.screen.blit(self.textinput.get_surface(), (380, 350))
            pygame.display.update()

            if self.buttonOk.is_mouse_over(pygame.mouse.get_pos()):
                self.buttonOk.set_font_color((255, 0, 0))
                if ((1,0,0) == pygame.mouse.get_pressed()):
                    if self.textinput.get_text() != '':
                        self.avalgame.initial( int(self.textinput.get_text()))
                        running = False
            else:
                self.buttonOk.set_font_color((255, 255, 255))

            if self.buttonCancel.is_mouse_over(pygame.mouse.get_pos()):
                self.buttonCancel.set_font_color((255, 0, 0))
                if ((1,0,0) == pygame.mouse.get_pressed()):
                    running = False
            else:
                self.buttonCancel.set_font_color((255, 255, 255))

            for event in events:
                if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        #print(self.textinput.get_text())
                        running = False


            self.screen.blit(self.buttonOk.label, self.buttonOk.position)
            self.screen.blit(self.buttonCancel.label, self.buttonCancel.position)

            x,y = eyetracker.sample()
            self.canvas.draw_circle(colour=(255,0,0),pos=(x,y), r=5 ,fill=True)

            self.disp.fill(self)
            self.disp.show()

class MenuItem(pygame.font.Font):
    def __init__(self, text, index, font='media/fonts/arial.ttf', font_size=30,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.index = index
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def is_mouse_over(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (
                posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


class MainMenu():
    def __init__(self, screen, bg_color=(0, 0, 0), font='media/fonts/arial.ttf', font_size=30, font_color=(255, 255, 255)):
        self.canvas = screen
        self.screen = screen.screen
        self.scr_width = screen.screen.get_rect().width
        self.scr_height = screen.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font, font_size)
        self.font_color = font_color
        self.items = []

        self.lang = "en"
        self.labels = ["Start", "Settings", "Exit"]
        self.langLabel = "Pt-BR"

        self.titleFont = pygame.font.Font(font, font_size * 2)
        self.title = self.titleFont.render("PyGame", 1, font_color)

        self.versionFont = pygame.font.Font(font, 20)
        self.version = self.versionFont.render(version, 1, font_color
                                               )
        self.langButton = MenuItem(self.langLabel, 100)
        self.langButton.set_position(0, self.scr_height - self.langButton.height)
        self.langButton.index = 2

    def reloadItems(self):
        self.items = []
        self.items.append(self.langButton)
        for index, item in enumerate(self.labels):
            menu_item = MenuItem(item, index)
            t_h = len(self.labels) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 4) + (index * 20) + index * menu_item.height
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def run(self):
        f = open("testeFile.txt", 'w')
        f.writelines(["ENTROU NO JOGO\n"])
        f.close()
        eyetracker = EyeTracker(disp)
        eyetracker.calibrate()
        disp.fill(screen)
        disp.show()

        self.reloadItems()
        running = True
        main_music = pygame.mixer.music.load("media/sounds/crimson.wav")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play()

        while running:
            self.canvas.clear()
												
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    running = False

            # Redraw the background
            self.screen.fill(self.bg_color)
            # display.show()
            # Draw Menu Title

            title_x = self.scr_width / 2 - self.title.get_rect().width / 2  # screen.get_rect().width/2 - self.title.get_rect().width/2
            title_y = self.scr_height / 10  # .get_rect().height/10

            self.screen.blit(self.title, (title_x, title_y))

            # Menu Options

            for item in self.items:
                if item.is_mouse_over(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    if ((1, 0, 0) == pygame.mouse.get_pressed()):
                        if (item.index == 0):
                            print "loading "

                            if avalgame.isEnabled():
                                playercode = SetGamerId(self.canvas,disp, avalgame=avalgame)
                                self.canvas.clear()
                                playercode.run()
                                print ("playercode START")
                                if avalgame._done:
                                    startGame = game.Game(self.canvas, disp, avalgame=avalgame)
                                    self.canvas.clear()
                                    startGame.run()
                                    print ("GAME START")

                            else:
                                startGame = game.Game(self.canvas, disp)
                                self.canvas.clear()
                                startGame.run()
                                print ("GAME START")
                        elif (item.index == 1):
                            print "settings"
                            settingsGame = GameSettings(self.canvas, disp, avalgame=avalgame)
                            self.canvas.clear()
                            settingsGame.run()
                            print ("settings START")
                        elif (item.index == 2):
                            print ("Saindo do jogo")
                            # log.close()
                            running = False
                        elif (item.index == 3):
                            if (self.lang == "pt"):
                                self.langButton.text = "Pt-BR"
                                self.labels = ["Start", "Settings", "Exit"]
                                self.lang = "en"
                                self.reloadItems()
                                pygame.mouse.set_pos(self.screen.get_rect().width / 2,
                                                     self.screen.get_rect().height / 2 - 30)
                            else:
                                self.langButton.text = "En-US"
                                self.labels = ["Iniciar", "Configuracoes", "Sair"]
                                self.lang = "pt"
                                self.reloadItems()
                                pygame.mouse.set_pos(self.screen.get_rect().width / 2,
                                                     self.screen.get_rect().height / 2 - 30)
                else:
                    item.set_font_color((255, 255, 255))

                self.screen.blit(item.label, item.position)

            # Draw version
            version_x = self.screen.get_rect().width - self.version.get_rect().width
            version_y = self.screen.get_rect().height - self.version.get_rect().height
            self.screen.blit(self.version, (version_x, version_y))

            # Draw languageButton

            self.screen.blit(self.langButton.label, self.langButton.position)

            ############ DISPLAY ##############
            # pygame.display.flip()
            x, y = eyetracker.sample()

            self.canvas.draw_circle(colour=(255, 0, 0), pos=(x, y), r=5, fill=True)
            disp.fill(self)
            disp.show()


#### Running
if __name__ == "__main__":
    screen = Screen()
    gm = MainMenu(screen)
    gm.run()
