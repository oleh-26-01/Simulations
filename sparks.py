from random import randint
from time import time, sleep
from math import sin, cos, radians
from pygame import init, display, draw, event, mouse, font
from pygame import KEYDOWN, K_ESCAPE, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(1)
screensize = [screensize, int(screensize * .75)]


class Main:
    def __init__(self):
        self.tick_rate = 100
        self.window = None
        self.caption = 'sparks v1.0'
        self.c_font = None
        self.p_font = None

    def init(self):
        init()
        self.window = display.set_mode(screensize)
        display.set_caption(self.caption)
        self.window.fill([0] * 3)


class Sparks:
    def __init__(self):
        self.min_size = 3
        self.max_size = 5
        self.min_lifetime = 10
        self.max_lifetime = 50
        self.list = []
        self.speed = 5
        self.occupancy = 1000
        self.g = .01
        self.color_set = 0

    def add_one(self):
        spark = Spark()

        pos = mouse.get_pos()
        spark.s_pos = [min(pos[0], screensize[1]), pos[1]]
        angle = radians(randint(0, 3600) / 10)
        spark.dx, spark.dy = cos(angle), sin(angle)
        spark.e_pos = [spark.s_pos[0] + spark.dx, spark.s_pos[1] + spark.dy]
        spark.length = abs(randint(self.min_size, self.max_size))
        spark.ttm = spark.length
        lifetime = int(spark.length * abs(randint(self.min_lifetime, self.max_lifetime)) / 10)
        spark.lifetime = [lifetime, lifetime]
        spark.color = self.color()
        self.list += [spark]

    def add_many(self, n):
        for _ in range(n):
            self.add_one()

    def move(self):
        for spark in self.list:
            spark.e_pos[0] += spark.dx
            spark.e_pos[1] += spark.dy

            if spark.ttm == 0:
                spark.s_pos[0] += spark.dx
                spark.s_pos[1] += (spark.dy - self.g * spark.length)
            else:
                spark.ttm -= 1

            spark.lifetime[1] -= 1
            spark.dy += self.g

    def clear(self):
        new_list = []
        for spark in self.list:
            if spark.lifetime[1] > 0:
                new_list += [spark]
        self.list = new_list

    def draw(self):
        for spark in self.list:
            draw.line(window, spark.color, spark.s_pos, spark.e_pos, 1)

    def ready(self):
        n = 0
        for spark in self.list:
            n += spark.length

        return True if n < self.occupancy else False

    def update(self):
        self.min_size = panels.list[0][2]
        self.max_size = panels.list[1][2]
        self.min_lifetime = panels.list[2][2]
        self.max_lifetime = panels.list[3][2]
        self.occupancy = panels.list[4][2]
        main.tick_rate = panels.list[5][2]
        self.g = panels.list[6][2]
        self.color_set = panels.list[7][2]
        self.min_size, self.max_size = min(self.min_size, self.max_size), max(self.min_size, self.max_size)
        self.min_lifetime, self.max_lifetime = min(self.min_lifetime, self.max_lifetime), max(self.min_lifetime,
                                                                                              self.max_lifetime)

    def color(self):
        color = [
            [randint(204, 255), randint(0, 255), randint(0, 255), [0, 1, 2]],
            [randint(0, 255), randint(204, 255), randint(0, 255), [0, 1, 2]],
            [randint(0, 255), randint(0, 255), randint(204, 255), [0, 1, 2]],
            [randint(204, 255), randint(0, 255), randint(0, 255), [1, 2, 0]],
            [randint(0, 255), randint(204, 255), randint(0, 255), [1, 2, 0]],
            [randint(0, 255), randint(0, 255), randint(204, 255), [1, 2, 0]],
            [randint(204, 255), randint(0, 255), randint(0, 255), [2, 0, 1]],
            [randint(0, 255), randint(204, 255), randint(0, 255), [2, 0, 1]],
            [randint(0, 255), randint(0, 255), randint(204, 255), [2, 0, 1]]
        ][self.color_set]
        color[color[3][0]] = int((color[color[3][1]] + color[color[3][2]]) / 2)
        color = color[:3]
        return color


class Spark:
    def __init__(self):
        self.s_pos = []
        self.e_pos = []
        self.dx, self.dy = 0, 0
        self.length = 0
        self.ttm = 0
        self.lifetime = [0, 0]
        self.color = []


class Panels:
    def __init__(self):
        self.list = []
        self.class_sparks = None
        self.c_font = None
        self.p_font = None
        self.font_color = [255] * 3

    def init(self):
        self.c_font = font.SysFont(None, 24)
        self.p_font = font.SysFont('Fixedsys', 12)
        self.list += [['Min. size', [1, 100], 3]]
        self.list += [['Max. size', [1, 100], 5]]
        self.list += [['Min. lifetime', [1, 100], 10]]
        self.list += [['Max. lifetime', [1, 100], 50]]
        self.list += [['Occupancy', [1, 3000], 1000]]
        self.list += [['Speed', [1, 100], 100]]
        self.list += [['Gravity', [0, .1], .01]]
        self.list += [['Color set', [0, 8], 0]]

    def draw(self):
        x, y = screensize[1], 0
        draw.rect(window, [20] * 3, [screensize[1], 0, int(screensize[0]), screensize[1]])
        for i in range(len(self.list)):
            panel = self.list[i]
            text = self.c_font.render(panel[0] + ': ' + str(panel[2]), True, self.font_color)
            window.blit(text, (x + 20, y + i * 50 + 20))
            draw.line(window, [60] * 3, [x + 20, y + i * 50 + 50], [screensize[0] - 20, y + i * 50 + 50], 3)
            cxp = x + 20 + panel[2] / panel[1][1] * (screensize[0] - screensize[1] - 40)
            draw.circle(window, [180] * 3, [cxp, y + i * 50 + 50], 10)

    def update(self):
        pos = mouse.get_pos()
        for i in range(len(self.list)):
            y = i * 50 + 50
            if abs(pos[1] - y) <= 10:
                ds = (pos[0] - screensize[1] - 20) / (screensize[0] - screensize[1] - 40)
                n = self.list[i][1][1] * ds
                n = int(n) if i != 6 else round(n, 3)
                n = max(self.list[i][1][0], n) if n < self.list[i][1][0] else n
                n = min(self.list[i][1][1], n) if n > self.list[i][1][1] else n
                self.list[i][2] = n


main = Main()
sparks = Sparks()
panels = Panels()

main.init()
window = main.window
panels.init()

ttu = False
while True:
    dt = lambda x=time(): time() - x

    while sparks.ready():
        sparks.add_one()

    window.fill([0] * 3)
    sparks.move()
    sparks.draw()
    sparks.clear()
    panels.draw()

    for _event in event.get():
        if _event.type == KEYDOWN or _event.type == QUIT:
            if _event.key == K_ESCAPE or _event.type == QUIT:
                quit()
        if _event.type == MOUSEBUTTONDOWN:
            ttu = True
        if _event.type == MOUSEBUTTONUP:
            ttu = False

    if ttu:
        panels.update()
        sparks.update()

    if main.tick_rate < 100:
        sleep(max(0, 1 / main.tick_rate - dt()))
    display.flip()
