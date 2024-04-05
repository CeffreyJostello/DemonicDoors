import pygame, sys
from render import Frame
from levels import Levels
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        pygame.display.set_caption('Demonic Doors')
        self.clock = pygame.time.Clock()
        # self.player = Player()
        self.levels = Levels() #Initalizes tile map
        self.frame = Frame(self.levels)

    def run(self): 

        while True:
            # self.player.update()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
                        pass


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.frame.entities.player.stop('up')
                    if event.key == pygame.K_s:
                        self.frame.entities.player.stop('down')
                    if event.key == pygame.K_a:
                        self.frame.entities.player.stop('left')
                    if event.key == pygame.K_d:
                        self.frame.entities.player.stop('right')

            self.frame.render(self.display)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
