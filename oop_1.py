import os
import time
import random
import curses

class game():
    def __init__(self,stdscr):
        self.stdscr = stdscr
        self.maxl = curses.LINES - 1
        self.maxc = curses.COLS - 1
        self.food_age = 100
        self.player_char = '🛸'
        self.enemy_char = '👾'
        self.food_char = '🍕'
        self.black_hole_char = '🌀'

        self.score = 0
        self.enemy_move_interval = 0.1
        self.eneym_move_time = time.time()

        self.init_curses()
        self.init_world()
        self.run()
    def init_curses(self):
        curses.curs_set(0)
        curses.n

