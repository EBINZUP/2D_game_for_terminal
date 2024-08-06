import curses
import random
import time
import os

class GameObject:
    def __init__(self, l, c, char):
        self.l = l
        self.c = c
        self.char = char

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxl = curses.LINES - 1
        self.maxc = curses.COLS - 1
        self.food_age = 100
        self.player_char = '🛸'
        self.food_char = '🍕'
        self.enemy_char = '👾'
        self.black_hole_char = '🌀'

        self.score = 0
        self.enemy_move_interval = 0.1
        self.last_enemy_move_time = time.time()
        self.play = True

        self.init_curses()
        self.init_world()
        self.run()

    def init_curses(self):
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def random_place(self):
        """Generate random coordinates for placing objects."""
        while True:
            a = random.randint(0, self.maxl - 1)
            b = random.randint(0, self.maxc - 1)
            if self.world[a][b] == ' ':
                return a, b

    def init_world(self):
        """Initialize the world with objects."""
        # Initialize an empty list to hold the world grid
        self.world = []

        # Loop through each row index
        for i in range(self.maxl + 1):
            # Create a new row
            row = []
            
            # Loop through each column index in the row
            for j in range(self.maxc + 1):
                # Decide the character based on a random condition
                if random.random() > 0.03:
                    row.append(' ')
                else:
                    row.append('.')
            
            # Append the completed row to the world grid
            self.world.append(row)

        # Initialize food objects
        num_food_items = random.randint(1, 20)
        self.food = []
        for _ in range(num_food_items):
            l, c = self.random_place()
            food_object = GameObject(l, c, self.food_char)
            self.food.append(food_object)

        # Initialize enemy objects
        num_enemies = 15
        self.enemies = []
        for _ in range(num_enemies):
            l, c = self.random_place()
            enemy_object = GameObject(l, c, self.enemy_char)
            self.enemies.append(enemy_object)

        # Initialize black hole objects
        num_black_holes = 2
        self.black_holes = []
        for _ in range(num_black_holes):
            l, c = self.random_place()
            black_hole_object = GameObject(l, c, self.black_hole_char)
            self.black_holes.append(black_hole_object)

        # Initialize player object
        player_l, player_c = self.random_place()
        self.player = GameObject(player_l, player_c, self.player_char)

    def in_range(self, a, min_val, max_val):
        return max(min(a, max_val), min_val)

    def draw(self):
        """Draw the world and objects on the screen."""
        self.stdscr.clear()
        for i in range(self.maxl):
            for j in range(self.maxc):
                self.stdscr.addch(i, j, self.world[i][j])

        # Show score
        self.stdscr.addstr(1, 1, f"score: {self.score}")

        # Draw food
        for f in self.food:
            self.stdscr.addch(f.l, f.c, f.char)

        # Draw enemies
        for e in self.enemies:
            self.stdscr.addch(e.l, e.c, e.char)

        # Draw black holes if score is above 50
        if self.score > 50:
            for b in self.black_holes:
                self.stdscr.addch(b.l, b.c, b.char)

        # Draw player
        self.stdscr.addch(self.player.l, self.player.c, self.player.char)
        self.stdscr.refresh()

    def move_player(self, key):
        """Move player based on input key."""
        if key == 'w' and self.world[self.player.l - 1][self.player.c] != '.':
            self.player.l -= 1
        elif key == 's' and self.world[self.player.l + 1][self.player.c] != '.':
            self.player.l += 1
        elif key == 'd' and self.world[self.player.l][self.player.c + 1] != '.':
            self.player.c += 1
        elif key == 'a' and self.world[self.player.l][self.player.c - 1] != '.':
            self.player.c -= 1

        self.player.l = self.in_range(self.player.l, 0, self.maxl - 1)
        self.player.c = self.in_range(self.player.c, 0, self.maxc - 1)

    def check_food(self):
        """Check if player has collected food."""
        for f in self.food:
            if self.player.l == f.l and self.player.c == f.c:
                self.score += 10
                f.l, f.c = self.random_place()

    def check_black_hole(self):
        """Check if player has encountered a black hole."""
        for b in self.black_holes:
            if self.player.l == b.l and self.player.c == b.c:
                curses.endwin()
                self.stdscr.clear()
                self.stdscr.addstr(self.maxl // 2, self.maxc // 2, "!!! YOU FOUND A HIDDEN WAY TO INTERSTELLAR JOURNEY !!!")
                self.stdscr.refresh()
                time.sleep(5)
                os.system('python another_script.py')
                exit()

    def move_enemies(self):
        """Move enemies and check for collisions with player."""
        for e in self.enemies:
            if random.random() > 0.6:
                if e.l > self.player.l:
                    e.l -= 1
                elif e.l < self.player.l:
                    e.l += 1
                if e.c < self.player.c:
                    e.c += 1
                elif e.c > self.player.c:
                    e.c -= 1

            e.l = self.in_range(e.l, 0, self.maxl - 1)
            e.c = self.in_range(e.c, 0, self.maxc - 1)

            if e.l == self.player.l and e.c == self.player.c:
                self.stdscr.addstr(self.maxl // 2, self.maxc // 2, "YOU DIED!!!!")
                self.stdscr.refresh()
                time.sleep(3)
                self.play = False

    def run(self):
        """Main game loop."""
        while self.play:
            current_time = time.time()
            try:
                key = self.stdscr.getkey()
            except:
                key = ''

            if key == 'q':
                self.play = False
            elif key == 'r':
                self.init_world()
            elif key in 'asdw':
                self.move_player(key)

            self.check_food()
            self.check_black_hole()
            if current_time - self.last_enemy_move_time > self.enemy_move_interval:
                self.move_enemies()
                self.last_enemy_move_time = current_time

            time.sleep(0.01)
            self.draw()

if __name__ == "__main__":
    try:
        curses.wrapper(Game)
    except KeyboardInterrupt:
        curses.endwin()
        print("Exited program")
    except Exception as e:
        curses.endwin()
        print(f"An error occurred: {e}")
