import pygame

font = None
font_size = 25
gameRunning = True

class Player(pygame.font.Font):
    def __init__(self):
        self.cash = 0
        self.c_card = 0
        
        pygame.font.Font.__init__(self, font, font_size)
        
        
        self.cashLabel = self.render(str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))
        
    def updateValues(self):
        self.cashLabel = self.render(str(self.cash),1,(0,0,0))
        self.c_cardLabel = self.render(str(self.c_card),1,(0,0,0))


class Game ():
    def __init__(self,screen):
        
        self.screen = screen
        self.width = screen.get_rect().width
        self.hieght = screen.get_rect().height
        self.bg_color = (255,255,255)
        #self.image
        self.player = Player()
        
    
    def run(self):
        self.player.updateValues()
        gameRunning = True
        while (gameRunning):
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        gameRunning = False
                    if (event.key == pygame.K_z): 
                        self.player.cash += 1
                        print (str(self.player.cash))
                        self.player.updateValues()
                
                
                
            self.screen.fill(self.bg_color)
            
            # Player Interface Draw
            cash_x = 0
            cash_y = 0
            
            self.screen.blit (self.player.cashLabel, (cash_x,cash_y))
            
            cCard_x = self.width - self.player.c_cardLabel.get_rect().width
            cCard_y = 0
            
            self.screen.blit (self.player.c_cardLabel,(cCard_x,cCard_y))
            
            ##Display
            pygame.display.flip()