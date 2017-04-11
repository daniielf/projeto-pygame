import pygame, sys, math, game

pygame.init()

### Definitions
windowSize = (1000,600)  #Change as you want (MUST RESPECT DISPLAY DIMENSIONS)
running = True

version = "v0.5"



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
    def __init__(self, screen, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        
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
        self.langButton.set_position(0,self.screen.get_rect().height - self.langButton.height)
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
        self.reloadItems()
        running = True
        
        while running:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    running = False
 
            # Redraw the background
            self.screen.fill(self.bg_color)
        
            # Draw Menu Title
            
            title_x = self.screen.get_rect().width/2 - self.title.get_rect().width/2
            title_y = self.screen.get_rect().height/10
            
            self.screen.blit (self.title, (title_x ,title_y))
             
            # Menu Options
            
            for item in self.items:
                if item.is_mouse_over(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    if ((1,0,0) == pygame.mouse.get_pressed()):
                        if (item.index == 0):
                            print "loading"
                            startGame = game.Game(self.screen)
                            startGame.run()
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
#                if (self.langButton.is_mouse_over(pygame.mouse.get_pos())):
#
#                    self.langButton.set_font_color((255,0,0))
#
#                    if ((1,0,0) == pygame.mouse.get_pressed()):
#                        if (self.lang == "pt"):
#                            self.langButton.text = "Pt-BR"
#                            self.labels = ["Start","Exit"]
#                            self.lang = "en"
#                            self.reloadItems()
#                            pygame.mouse.set_pos(self.screen.get_rect().width/2 , self.screen.get_rect().height/2)
#                        else:
#                            self.langButton.text = "En-US"
#                            self.labels = ["Iniciar","Sair"]
#                            self.lang = "pt"
#                            self.reloadItems()
#                            pygame.mouse.set_pos(self.screen.get_rect().width/2 , self.screen.get_rect().height/2)
#
#                else:
#                    self.langButton.set_font_color((255,255,255))
            
            ############ DISPLAY ##############
            pygame.display.flip()
            
            
#### Running
if __name__ == "__main__":
    screen  = pygame.display.set_mode(windowSize, 0 ,32)
    pygame.display.set_caption('Game Menu')
    gm = MainMenu(screen)
    pygame.display.set_caption('PyMarket')
    gm.run()
    print ("GAME START")

#while (running):
#    
#    for event in pygame.event.get():
#        if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
#            running = false
            
       