from random import randint
from time import time, sleep
from math import sin, cos, radians
from pygame import init, display, draw, event, KEYDOWN, K_ESCAPE, QUIT, mouse, FULLSCREEN
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(1)

class Main:
    screensize = int(screensize * .75)
    def __init__(self):
        self.screensize = int(screensize * .75)
        self.tick_rate = 100
        self.window = None
        self.caption = 'sparks v1.0'

    def init(self):
        init()
        self.window = display.set_mode([self.screensize]*2)
        display.set_caption(self.caption)
        self.window.fill([0]*3)

class Sparks:
    min_size = 3
    max_size = 5
    min_lifetime = 10
    max_lifetime = 50
    def __init__(self):
        self.list = []
        self.speed = 5
        self.window = None
        self.occupancy = 3000

    def add_one(self):
        spark = Spark()
        spark.init()
        self.list += [spark]

    def add_many(self, n):
        for _ in range(n):
            self.add_one()

    def move(self):
        for spark in self.list:
            spark.e_pos[0] += spark.dx * self.speed
            spark.e_pos[1] += spark.dy * self.speed

            if spark.ttm == 0:
                spark.s_pos[0] += spark.dx * self.speed
                spark.s_pos[1] += (spark.dy - 0.01*spark.length) * self.speed
            else:
            	spark.ttm -= 1
            
            spark.lifetime[1] -= 1
            spark.dy += 0.01

    def clear(self):
        new_list = []
        for spark in self.list:
            if spark.lifetime[1] != 0:
                new_list += [spark]
        self.list = new_list

    def draw(self):
        for spark in self.list:
            draw.line(self.window, spark.color, spark.s_pos, spark.e_pos, 1)

    def ready(self):
        n = 0
        for spark in self.list:
            n += spark.length
        
        return True if n < self.occupancy else False

class Spark:
    def __init__(self):
        self.s_pos = []
        self.e_pos = []
        self.dx, self.dy = 0, 0
        self.length = 0
        self.ttm = 0
        self.lifetime = [0, 0]
        self.color = []

    def init(self):
        pos = mouse.get_pos()
        self.s_pos = [pos[0], pos[1]]
        angle = radians(randint(0, 3600)/10)
        self.dx, self.dy = cos(angle), sin(angle)
        self.e_pos = [self.s_pos[0] + self.dx, self.s_pos[1] + self.dy]
        self.length = randint(Sparks.min_size, Sparks.max_size)
        self.ttm = self.length
        lifetime = int(self.length * randint(Sparks.min_lifetime, Sparks.max_lifetime) / 10)
        self.lifetime = [lifetime, lifetime]
        r = randint(204, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        g = (r + b) / 2
        self.color = [r, g, b]

main = Main()
sparks = Sparks()
main.init()
window = main.window
sparks.window = main.window

while True:
    dt = lambda x = time() : time() - x

    while sparks.ready():
        sparks.add_one()

    window.fill([0]*3)
    sparks.move()
    sparks.draw()
    sparks.clear()

    for _event in event.get():
        if _event.type == KEYDOWN or _event.type == QUIT:
            if _event.key == K_ESCAPE or _event.type == QUIT:
                quit()

    sleep(max(0, 1/main.tick_rate - dt()))
    display.flip()
