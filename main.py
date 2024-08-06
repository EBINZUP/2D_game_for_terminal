import curses
import random
import time

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    maxl = curses.LINES - 1
    maxc = curses.COLS - 1

    world =[]
    player_c = player_l = 0
    food = []
    score = 0
    enemy = []
    def random_place():
        """Generate random coordinates for placing player or food."""
        while True:
            a = random.randint(0, maxl - 1)
            b = random.randint(0, maxc - 1)
            if world[a][b] == ' ':
                return a, b
     
    def init_world():
        """Initialize the world with random dots and spaces."""
        nonlocal player_c, player_l, world
        world = []
        for i in range( maxl+1):
            world.append([])
            for j in range (maxc+1):
                world[i].append(' ' if random.random() > 0.03 else '.')

        for i in range(random.randint(1 , 20)):
            fl , fc =  random_place()
            fh = random.randint(1000 ,10000)
            food.append((fl ,fc ,fh))         

        for i in range(3):
            el , ec =  random_place()
            enemy.append((el ,ec))

        player_l , player_c = random_place()      
        return world
    
    
    def in_range(a ,min ,max):
        if a > max:
            return max
        if a < min:
            return min
        
        return a
    
    def draw(world):
        """Draw the world grid on the screen."""
        #draw world
        stdscr.clear()
        for i in range(maxl):
            for j in range(maxc):
                stdscr.addch(i, j, world[i][j])
        # show sore
        stdscr.addstr(1 ,1 ,f"score : {score}")        
        # showing the food 
        for f in food :
            fl, fc, fa = f
            stdscr.addch(fl ,fc , '#')   
        # Showing enemy
        for e in enemy:
            el ,ec = e
            stdscr.addch(el, ec ,'E')

        # showing the player        
        stdscr.addch(player_l,player_c, 'X')        
        stdscr.refresh()

    # Initialize the world
    world = init_world()
    draw(world)

    def move(key):
        ''' move on one direction based on awsd'''
        
        nonlocal player_c, player_l

        if key == 'w' and world[player_l - 1][player_c] != '.':   
            player_l -= 1  
                
        elif key == 's' and world[player_l + 1][player_c] != '.':
            player_l += 1  

        elif key == 'd' and world[player_l][player_c + 1] != '.':
            player_c += 1  

        elif key == 'a' and world[player_l][player_c - 1] != '.':                    
            player_c -= 1  

        player_l = in_range(player_l ,0 ,maxl - 1)    # Prevent moving out of bounds

        player_c = in_range(player_c ,0 ,maxc - 1)    # Prevent moving out of bounds
    def cheak_food():
        for i in range (len(food)):
            nonlocal score
            fl ,fc ,fh =food[i]
            if player_l == fl and player_c == fc:
                score +=10
                nfl , nfc = random_place()
                nfh = random.randint(1000 ,10000)
                food[i]=(nfl ,nfc ,nfh)

    def move_enemy():
        nonlocal play
        for i in range(len(enemy)):
            l,c = enemy[i]   
            if random.random() > 0.6:
                l += random.choice([0 ,1 ,-1])
                c += random.choice([0 ,1 ,-1])
                l = in_range(l ,0 ,maxl - 1)
                c = in_range(c ,0 ,maxc - 1)
                enemy[i] = (l, c)
            if l == player_l and c==player_c:
                stdscr.addstr(maxl//2 ,maxc//2 ,"YOU DIED!!!!")
                stdscr.refresh()
                time.sleep(3)
                play = False

    # Wait for user input to exit or refresh
    play = True
    while play:
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
        cheak_food()     
        move_enemy() 
        time.sleep(0.1)
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
