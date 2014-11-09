__author__ = 'tom'

from glob import glob
from os.path import join, dirname
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
import random
import time


class DefenseGame(Widget):
    """
    Root widget of the game. Controls game information and creation of new attackers.
    This class was based on the Game class from my first project.
    """

    base = ObjectProperty(None)
    message = StringProperty("")
    last_time = NumericProperty(0)
    kill_count = NumericProperty(0)

    play = True
    accel = 0.9
    attackers = []

    rat_run_e = []
    rat_run_w = []
    rat_run_n = []
    rat_run_s = []

    rat_fall_e = []
    rat_fall_w = []
    rat_fall_n = []
    rat_fall_s = []

    def pop_attacker(self):
        """
        This method creates three new attackers each time it is called and puts them into a list and adds them to
        the root widget.
        """
        tot = len(self.attackers)
        for i in range(len(self.attackers), len(self.attackers) + 3):
            tot += 1
            attacker = Attacker()
            attacker.total = tot
            attacker.set_start_pos()
            self.attackers.append(attacker)
            self.add_widget(attacker)

    def on_touch_down(self, touch):
        """
        Checks for a touch event happening on all attackers. When a touch occurs the attacker is stopped the kill count
        is incremented and the state of the attacker is changed.
        """
        for attack in self.attackers:
            if attack.pos[0] <= touch.x <= (attack.pos[0] + attack.width) and \
                    attack.pos[1] <= touch.y <= (attack.pos[1] + attack.height):
                attack.state = 1
                attack.velocity = (0, 0)
                self.kill_count += 1

    def start_attackers(self):
        """
        This method calculates the direction and speed to travel for attackers and increments the acceleration factor.
        Parts of this method were taken from my first project.
        """
        self.accel += 0.1
        for attack in self.attackers:
            dif_x = self.base.pos[0] - attack.pos[0]
            dif_y = self.base.pos[1] - attack.pos[1]
            attack.velocity = Vector(dif_x, dif_y).normalize() * self.accel

            if abs(dif_x) >= abs(dif_y) and dif_x <= 0:
                attack.direct = 0
            if abs(dif_x) >= abs(dif_y) and dif_x <= 0:
                attack.direct = 1
            if abs(dif_x) <= abs(dif_y) and dif_y >= 0:
                attack.direct = 2
            if abs(dif_x) <= abs(dif_y) and dif_y <= 0:
                attack.direct = 3

    def update(self, dt):
        """
        While the play variable is true this method calculates when to create new attackers and moves them. It also
        times the animations for the attackers. Part of this method was taken from the in class animation example.
        """
        if self.play:
            if time.time() - self.last_time > 3:
                self.pop_attacker()
                self.start_attackers()
                self.last_time = time.time()
            for attack in self.attackers:
                attack.move()
                if self.base.collide_widget(attack):
                    attack.velocity = (0, 0)
                    self.play = False
            for attack in self.attackers:
                if attack.state == 0:
                    if attack.delay < 10:
                        attack.delay += 1
                    else:
                        attack.delay = 0
                        if attack.imageNum >= len(self.rat_run_e):
                            attack.imageNum = 0
                        if attack.direct == 0:
                            attack.source = self.rat_run_e[attack.imageNum]
                        if attack.direct == 1:
                            attack.source = self.rat_run_w[attack.imageNum]
                        if attack.direct == 2:
                            attack.source = self.rat_run_n[attack.imageNum]
                        if attack.direct == 3:
                            attack.source = self.rat_run_s[attack.imageNum]
                        attack.imageNum += 1
                if attack.state == 1:
                    if attack.delay < 10:
                        attack.delay += 1
                    else:
                        if attack.fallImage > 11:
                            self.remove_widget(attack)
                            self.attackers.remove(attack)
                        else:
                            if attack.direct == 0:
                                attack.source = self.rat_fall_e[attack.fallImage]
                            if attack.direct == 1:
                                attack.source = self.rat_fall_w[attack.fallImage]
                            if attack.direct == 2:
                                attack.source = self.rat_fall_n[attack.fallImage]
                            if attack.direct == 3:
                                attack.source = self.rat_fall_s[attack.fallImage]
                        attack.fallImage += 1
        else:
            self.message = "Game Over"

    def load_images(self):
        """
        Loads all the needed images for the game. This was based on the in class animation example.
        """
        curdir = dirname(__file__)
        i = 0
        for filename in glob(join(curdir, 'png_files', 'run_e', '*')):
            self.rat_run_e.append(filename)
            i += 1
        self.rat_run_e.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'run_n', '*')):
            self.rat_run_n.append(filename)
            i += 1
        self.rat_run_n.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'run_s', '*')):
            self.rat_run_s.append(filename)
            i += 1
        self.rat_run_s.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'run_w', '*')):
            self.rat_run_w.append(filename)
            i += 1
        self.rat_run_w.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'fall_e', '*')):
            self.rat_fall_e.append(filename)
            i += 1
        self.rat_fall_e.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'fall_n', '*')):
            self.rat_fall_n.append(filename)
            i += 1
        self.rat_fall_n.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'fall_s', '*')):
            self.rat_fall_s.append(filename)
            i += 1
        self.rat_fall_s.sort()

        i = 0
        for filename in glob(join(curdir, 'png_files', 'fall_w', '*')):
            self.rat_fall_w.append(filename)
            i += 1
        self.rat_fall_w.sort()


class DefenseApp(App):
    """
    Main class of Defense game
    """

    def build(self):
        game = DefenseGame()
        game.load_images()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


class Attacker(Widget):
    """
    The attack class has several variables to track animation images, direction of travel, state (moving, falling)
     the delay in animation and total number of attackers generated.
    """

    x_velocity = NumericProperty(0)
    y_velocity = NumericProperty(0)
    velocity = ReferenceListProperty(x_velocity, y_velocity)

    fallImage = 0
    imageNum = 0
    direct = 0
    state = 0

    delay = NumericProperty(10)
    total = NumericProperty(0)
    source = StringProperty(None)

    def move(self):
        """
        This move method was copied from the first project.
        :return:
        """
        self.pos = Vector(*self.velocity) + self.pos

    def set_start_pos(self):
        """
        A random number between 0 and 3 is generated to select which edge of the screen the attacker will start from,
        then a random number within the range of the window size is selected.
        :return:
        """
        edge = random.randint(0, 3)
        if edge == 0:
            x_pos = 0
            y_pos = random.randint(0, 540)
        elif edge == 1:
            x_pos = 740
            y_pos = random.randint(0, 540)
        elif edge == 2:
            x_pos = random.randint(0, 740)
            y_pos = 0
        else:
            x_pos = random.randint(0, 740)
            y_pos = 540
        self.pos = (x_pos, y_pos)


class Base(Widget):
    """
    Cheese wheel base that the rats try to get.
    """
    curdir = dirname(__file__)
    image_file = join(curdir, 'png_files', 'Cheese_Wheel.png')
    source = str(image_file)


if __name__ == '__main__':
    DefenseApp().run()