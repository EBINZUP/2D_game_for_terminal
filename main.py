import curses
import random
import time
import os

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    maxl = curses.LINES - 1
    maxc = curses.COLS - 1
    food_age = 100
    player_char = '🛸'
    food_char = '🍕'
    enemy_char = '👾'
    black_hole_char = '🌀'

    player_c = player_l = 0
    score = 0
    enemy = []
    food = []
    black_hole = []
    world = []

    enemy_move_interval = 0.1  # Enemies move every 0.5 seconds
    last_enemy_move_time = time.time()

    def random_place():
        """Generate random coordinates for placing player or food."""
        while True:
            a = random.randint(0, maxl - 1)
            b = random.randint(0, maxc - 1)
            if world[a][b] == ' ':
                return a, b

    def init_world():
        """Initialize the world with random dots and spaces."""
        nonlocal player_c, player_l, world, food, enemy, black_hole
        world = []
        for i in range(maxl + 1):
            world.append([])
            for j in range(maxc + 1):
                world[i].append(' ' if random.random() > 0.03 else '.')

        food = []
        for i in range(random.randint(1, 20)):
            fl, fc = random_place()
            fh = random.randint(food_age, food_age*10)
            food.append((fl, fc, fh))

        enemy = []
        for i in range(30):
            el, ec = random_place()
            enemy.append((el, ec))

        black_hole = []
        for i in range(2):
            bl, bc = random_place()
            black_hole.append((bl, bc))

        player_l, player_c = random_place()
        return world

    def in_range(a, min_val, max_val):
        if a > max_val:
            return max_val
        if a < min_val:
            return min_val
        return a

    def draw(world):
        """Draw the world grid on the screen."""
        # Draw world
        stdscr.clear()
        for i in range(maxl):
            for j in range(maxc):
                stdscr.addch(i, j, world[i][j])
                
        # Show score
        stdscr.addstr(1, 1, f"score: {score}")
        # Showing the food
        for f in food:
            fl, fc, fa = f
            stdscr.addch(fl, fc, food_char)
        # Showing enemy
        for e in enemy:
            el, ec = e
            stdscr.addch(el, ec, enemy_char)
        if score > 50:
            for b in black_hole:
                bl, bc = b
                stdscr.addch(bl, bc, black_hole_char)    

        # Showing the player
        stdscr.addch(player_l, player_c, player_char)
        stdscr.refresh()

    # Initialize the world
    world = init_world()
    draw(world)

    def move(key):
        """Move in one direction based on aswd."""
        nonlocal player_c, player_l

        if key == 'w' and world[player_l - 1][player_c] != '.':
            player_l -= 1
        elif key == 's' and world[player_l + 1][player_c] != '.':
            player_l += 1
        elif key == 'd' and world[player_l][player_c + 1] != '.':
            player_c += 1
        elif key == 'a' and world[player_l][player_c - 1] != '.':
            player_c -= 1

        player_l = in_range(player_l, 0, maxl - 1)  # Prevent moving out of bounds
        player_c = in_range(player_c, 0, maxc - 1)  # Prevent moving out of bounds

    def check_food():
        nonlocal score
        for i in range(len(food)):
            fl, fc, fh = food[i]
            fh -= 1
            if player_l == fl and player_c == fc:
                score += 10
                fl, fc = random_place()
                fh = random.randint(food_age, food_age * 10)
                food[i] = (fl, fc, fh)
            if fh <= 0:
                fl, fc = random_place()
                fh = random.randint(food_age, food_age * 10)
            food[i] = (fl, fc, fh)

    def check_black_hole():
        for i in range(len(black_hole)):
            bl, bc = black_hole[i]
            if player_l == bl and player_c == bc:
                curses.endwin()  # End curses mode before printing to the terminal or launching another script
                stdscr.clear()
                stdscr.addstr(maxl // 2, maxc // 2, "!!! YOU FOUND A HIDDEN WAY TO INTERSTELLAR JOURNEY !!!")
                stdscr.refresh()
                time.sleep(5)
                os.system('python another_script.py')
                exit() 

    def move_enemy():
        nonlocal play
        for i in range(len(enemy)):
            l, c = enemy[i]
            if random.random() > 0.6:
                if l > player_l:
                    l -= 2
                elif l < player_l:
                    l += 2
                elif c < player_c:
                    c += 2
                elif c > player_c:
                    c -= 2

                l = in_range(l, 0, maxl - 1)
                c = in_range(c, 0, maxc - 1)
                enemy[i] = (l, c)
            if l == player_l and c == player_c:
                stdscr.addstr(maxl // 2, maxc // 2, "YOU DIED!!!!")
                stdscr.refresh()
                time.sleep(3)
                play = False

    # Wait for user input to exit or refresh
    play = True
    while play:
        current_time = time.time()
        try:
            key = stdscr.getkey()
        except:
            key = ''

        if key == 'q':  # Press 'q' to exit
            play = False
        elif key == 'r':  # Press 'r' to refresh the screen
            world = init_world()
            draw(world)
        elif key in 'asdw':
            move(key)

        check_food()
        check_black_hole()
        if current_time - last_enemy_move_time > enemy_move_interval:
            move_enemy()
            last_enemy_move_time = current_time

        time.sleep(0.01)
        draw(world)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Ensure the terminal is reset on interrupt
        curses.endwin()
        print("Exited program")
    except Exception as e:
        # Ensure the terminal is reset on any other exception
        curses.endwin()
        print(f"An error occurred: {e}")
