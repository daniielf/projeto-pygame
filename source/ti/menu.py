#from psychopy import *
import pygame, sys, math, game
from pygaze.libscreen import Screen,Display
from pygaze.eyetracker import EyeTracker
from pygaze import liblog  # Criar logs de saida com os resultados do experimento
from pygaze import libinput  # Obter interacao do usuario atraves do mouse e teclado
from pygaze import libtime  # Obter a latencia do usuario em relacao aos estimulos
pygame.init()


disp = Display()
### Definitions
windowSize = (1366,768)  #Change as you want (MUST RESPECT DISPLAY DIMENSIONS)
running = True

version = "v1.00"


class MenuItem(pygame.font.Font):
    def __init__(self, text, index, font=None, font_size=30,
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
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False
    
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

class MainMenu():
    def __init__(self, screen, bg_color=(0,0,0), font=None, font_size=30,font_color=(255, 255, 255)):
        self.canvas = screen
        self.screen = screen.screen
        self.scr_width = screen.screen.get_rect().width
        self.scr_height = screen.screen.get_rect().height
        
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        

        self.lang = "en"
        self.labels = ["Start","Exit"]
        self.langLabel = "Pt-BR"
        
        self.titleFont = pygame.font.SysFont(font,font_size*2)
        self.title = self.titleFont.render ("PyGame", 1, font_color)
        
        self.versionFont = pygame.font.SysFont(font, 20)
        self.version = self.versionFont.render (version, 1, font_color
                                               )
        self.langButton = MenuItem(self.langLabel, 100)
        self.langButton.set_position(0,self.scr_height - self.langButton.height)
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
        eyetracker = EyeTracker(disp)
        eyetracker.calibrate()
								
				# PREENCHIMENTO DO DISPLAY
        disp.fill(screen)
				# MOSTRAR DISPLAY
        disp.show()
        
        self.reloadItems()
        running = True
        main_music = pygame.mixer.music.load("../media/sounds/crimson.wav")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play()
        
        while running:
						# LIMPAR TELA
            self.canvas.clear()
												

            self.clock.tick(50)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    running = False

									
            self.screen.fill(self.bg_color)
            
            title_x = self.scr_width/2 - self.title.get_rect().width/2 #screen.get_rect().width/2 - self.title.get_rect().width/2
            title_y = self.scr_height/10 #.get_rect().height/10
            
            self.screen.blit (self.title, (title_x ,title_y))
             
            # Menu Options
            
            for item in self.items:
                if item.is_mouse_over(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    if ((1,0,0) == pygame.mouse.get_pressed()):
                        if (item.index == 0):
                            print "loading"
                            startGame = game.Game(self.canvas, disp)
                            self.canvas.clear()
                            startGame.run()
                            print ("GAME START")
                        elif (item.index == 1):
                            print ("Saindo do jogo")
                            running = False
                        elif (item.index == 2):
                            if (self.lang == "pt"):
                                self.langButton.text = "Pt-BR"
                                self.labels = ["Start","Exit"]
                                self.lang = "en"
                                self.reloadItems()
                                pygame.mouse.set_pos(self.screen.get_rect().width/2, self.screen.get_rect().height/2 - 30)
                            else:
                                self.langButton.text = "En-US"
                                self.labels = ["Iniciar","Sair"]
                                self.lang = "pt"
                                self.reloadItems()
                                pygame.mouse.set_pos(self.screen.get_rect().width/2, self.screen.get_rect().height/2 - 30)
                else:
                    item.set_font_color((255, 255, 255))
                    
                self.screen.blit(item.label, item.position)
      
								
            # Draw version
            version_x = self.screen.get_rect().width - self.version.get_rect().width
            version_y = self.screen.get_rect().height - self.version.get_rect().height         
            self.screen.blit (self.version, (version_x,version_y))
            
            # Draw languageButton
            
            self.screen.blit (self.langButton.label, self.langButton.position)
            
            ############ DISPLAY ##############
            #pygame.display.flip()
            x,y = eyetracker.sample()
            
            self.canvas.draw_circle(colour=(255,0,0),pos=(x,y), r=5 ,fill=True)
            disp.fill(self)
            disp.show()


        
#### Running
if __name__ == "__main__":
    
    ## CRIAcaoO DE TELA
    screen = Screen()
    gm = MainMenu(screen)
    gm.run()


     
       