import pygame, random, objects, math, text_input
from pygaze.eyetracker import EyeTracker
from pygaze.libscreen import Screen,Display
from pygame.locals import*
from menu import MenuItem
disp = Display()
clock = pygame.time.Clock()

class GameSettings(pygame.font.Font):
    def __init__(self, screen, display ,bg_color=(0,0,0), font=None,
    font_size=40, avalgame=None):
        self.avalgame = avalgame
        self.screen = screen.screen
        self.canvas = screen
        self.disp = display
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.bg_color = bg_color
        pygame.font.Font.__init__(self, None, 40)


        self.textFont = pygame.font.SysFont(font,font_size)
        self.exitFont = pygame.font.SysFont(font,20)

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
                        print(self.textinput.get_text())
                        running = False


            self.screen.blit(self.buttonOk.label, self.buttonOk.position)
            self.screen.blit(self.buttonCancel.label, self.buttonCancel.position)

            x,y = eyetracker.sample()
            self.canvas.draw_circle(colour=(255,0,0),pos=(x,y), r=5 ,fill=True)

            self.disp.fill(self)
            self.disp.show()

class SetGamerId(pygame.font.Font):
    def __init__(self, screen, display ,bg_color=(0,0,0), font=None,
    font_size=40, avalgame=None):
        self.avalgame = avalgame
        self.screen = screen.screen
        self.canvas = screen
        self.disp = display
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.bg_color = bg_color
        pygame.font.Font.__init__(self, None, 40)


        self.textFont = pygame.font.SysFont(font,font_size)
        self.exitFont = pygame.font.SysFont(font,20)

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
                        print(self.textinput.get_text())
                        running = False


            self.screen.blit(self.buttonOk.label, self.buttonOk.position)
            self.screen.blit(self.buttonCancel.label, self.buttonCancel.position)

            x,y = eyetracker.sample()
            self.canvas.draw_circle(colour=(255,0,0),pos=(x,y), r=5 ,fill=True)

            self.disp.fill(self)
            self.disp.show()
