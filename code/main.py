import pygame, sys
from render import Frame
from levels import Levels
from settings import *
from utilities import *
class Game:
    def __init__(self):
        if DEBUG:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.display = pygame.Surface((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        # self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Demonic Doors')
        self.clock = pygame.time.Clock()
        # self.player = Player()sw
        self.levels = Levels() #Initalizes tile map
        self.frame = Frame(self.levels)

    def run(self): 

        while True:
            # self.player.update()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.frame.mouse_click = True
                else:
                    self.frame.mouse_click = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.frame.entities.player.move('up')
                    if event.key == pygame.K_s:
                        self.frame.entities.player.move('down')
                    if event.key == pygame.K_a:
                        self.frame.entities.player.move('left')
                    if event.key == pygame.K_d:
                        self.frame.entities.player.move('right')
                    if event.key == pygame.K_ESCAPE:
                        self.frame.menu_open = not self.frame.menu_open
                        if self.frame.menu_open:
                            
                            self.frame.crosshair.set_crosshair('pointer', (5, 5))
                        else:
                            self.frame.crosshair.set_crosshair('aimer', (5, 5))
                    if event.key == pygame.K_F1:
                        self.frame.tilemap = self.levels.level_2()
                    if event.key == pygame.K_F2:
                        self.frame.tilemap = self.levels.level_1()
                    if event.key == pygame.K_F3:
                        self.frame.tilemap = self.levels.level_3()
                    if event.key == pygame.K_F4:
                        self.frame.tilemap = self.levels.level_4()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.frame.entities.player.stop('up')
                    if event.key == pygame.K_s:
                        self.frame.entities.player.stop('down')
                    if event.key == pygame.K_a:
                        self.frame.entities.player.stop('left')
                    if event.key == pygame.K_d:
                        self.frame.entities.player.stop('right')
                        
            if DEBUG:
                self.frame.render(self.screen)
            else:
                self.frame.render(self.display)
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
    
    