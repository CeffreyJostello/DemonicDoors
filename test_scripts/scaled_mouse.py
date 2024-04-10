import string
import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
screen_rect = screen.get_rect()
clock = pg.time.Clock()

# the surface we draw our stuff on
some_surface = pg.Surface((320, 240))
some_surface_rect = some_surface.get_rect()

# just something we want to check for mouse hovering
click_me = pg.Surface((100, 100))
click_me_rect = click_me.get_rect(center=(100, 100))

hover = False
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            done = True

    # draw some stuff on our surface
    some_surface.fill(pg.Color('gray12'))
    click_me.fill(pg.Color('dodgerblue') if not hover else pg.Color('red'))
    some_surface.blit(click_me, click_me_rect)
    # scale it
    scaled_surface = pg.transform.scale(some_surface, screen_rect.size)
    # draw it on the window
    screen.blit(scaled_surface, (0, 0))

    pos = list(pg.mouse.get_pos())
    # take the mouse position and scale it, too
    ratio_x = (screen_rect.width / some_surface_rect.width)
    ratio_y = (screen_rect.height / some_surface_rect.height)
    scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)

    # use collidepoint as usual
    hover = click_me_rect.collidepoint(scaled_pos)

    pg.display.flip()
    clock.tick(60)

pg.quit()