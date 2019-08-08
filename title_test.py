```python
import pygame as pg
WIDTH = 1920
HEIGHT = 1080
FPS = 30
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE)
pg.display.set_caption("Test Fade")
clock = pg.time.Clock()
title_image = pg.image.load("img/skyrealm.png").convert()
title_image = pg.transform.scale(title_image, (WIDTH, HEIGHT))

waiting = True
i = 0
while waiting:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    title_image.set_alpha(i) 
    screen.blit(title_image, (0, 0))
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            waiting = False
            pg.quit()
    i += 1
    if i > 255:
        i = 255
```
