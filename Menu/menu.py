import pygame, sys, math

pygame.init()

running = True


class MainMenu():
    def __init__(self, screen, bg_color=(0,0,0)):
 
        self.screen = screen
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
    def run(self):
        running = True
        while running:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    running = False
 
            # Redraw the background
            self.screen.fill(self.bg_color)
            pygame.display.flip()
            
#### Running
if __name__ == "__main__":
    screen  = pygame.display.set_mode((500,500), 0 ,32)
    pygame.display.set_caption('Game Menu')
    gm = MainMenu(screen)
    gm.run()

#while (running):
#    
#    for event in pygame.event.get():
#        if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
#            running = false
            
       