import curses

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    maxl = curses.LINES - 1
    maxc = curses.COLS - 1

    world = []

    def init():
        for i in range(maxl):
            world.append([])
            for j in range(maxc):
                world[i].append(".")

    def draw():
        for i in range(maxl):
            for j in range(maxc):
                stdscr.addch(i, j, world[i][j])
        stdscr.refresh()

    init()
    draw()

    # Wait for user input to exit
    while True:
        key = stdscr.getch()
        if key == ord('q'):  # Press 'q' to exit
            break

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
