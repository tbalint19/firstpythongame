import curses
import time
import random
import os.path

screen = curses.initscr()
curses.start_color()
curses.init_color(0, 0, 0, 0)
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
screen.keypad(1)
border_of_map = screen.getmaxyx()
curses.noecho()
y = int(border_of_map[0] / 2)
x = int(border_of_map[1] / 2)

score = 0
lets_go = True
troll = False
map_displayed = 5
length = 5
remaining_time = 9999
troll_message_remaining = 9999
speed = 0.05
troll = False
troll_message_position = []

choose_map = "Turn NumLock off, and press 5 to start"


def menu():

    screen.clear()

    global choose_map
    global map_displayed
    map_displayed = 5
    screen.addstr(y, x - int(len(choose_map) / 2), str(choose_map))

    choose = screen.getch()
    screen.clear()

    if choose == curses.KEY_END:
        map_displayed = 1
    elif choose == curses.KEY_DOWN:
        map_displayed = 2
    elif choose == curses.KEY_NPAGE:
        map_displayed = 3
    elif choose == curses.KEY_LEFT:
        map_displayed = 4
    # map number 5 is the empty map
    elif choose == curses.KEY_RIGHT:
        map_displayed = 6

    return map_displayed


def create_map():

    global map_displayed

    if map_displayed == 1:
        screen.addch(y, x, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x, 'x', curses.color_pair(2))
        for coord in range(-(x - 7), y - 7):
            screen.addch(y, x + coord, 'x', curses.color_pair(2))

    if map_displayed == 2:
        screen.addch(y, x, 'x')
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x + coord, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x - coord, 'x', curses.color_pair(2))

    if map_displayed == 3:
        screen.addch(y, x, 'x')
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x + coord, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x - coord, 'x', curses.color_pair(2))
        for coord in range(-(x - 7), x - 7):
            screen.addch(y, x + coord, 'x', curses.color_pair(2))

    if map_displayed == 4:

        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x + coord + 10, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x - coord + 10, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x + coord - 10, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x - coord - 10, 'x', curses.color_pair(2))

    if map_displayed == 6:

        screen.addch(y, x, 'x')

        for coord in range(-(y - 7), x - 7):
            screen.addch(y, x + coord, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), x - 7):
            screen.addch(y + coord, x + 10, 'x', curses.color_pair(2))
        for coord in range(-(y - 7), y - 7):
            screen.addch(y + coord, x - 10, 'x', curses.color_pair(2))

    screen.border("#", "#", "#", "#", "#", "#", "#", "#")


def game():

    screen.border("#", "#", "#", "#", "#", "#", "#", "#")
    screen.nodelay(1)

    head = [20, 20]
    body = []
    direction = 3
    snake_moves = True
    food_exist = False

    global x
    global y
    global length

    while snake_moves:

        global score
        screen.addstr(0, 2 * x - 15, " "*10)
        screen.addstr(0, 2 * x - 15, "score: " + str(score))
        screen.move(border_of_map[0]-1, border_of_map[1]-1)

        while not food_exist:

            y_food = random.randrange(20, border_of_map[0] - 20)
            x_food = random.randrange(20, border_of_map[1] - 20)
            if screen.inch(y_food, x_food) == ord(' '):
                food_exist = True
                screen.addch(y_food, x_food, '+')

        screen.addch(head[0], head[1], 'o')
        co_ord_list = (head[0], head[1])
        body.append(list(co_ord_list))

        action = screen.getch()
        if action == curses.KEY_UP and direction != 2:
            direction = 8
        if action == curses.KEY_DOWN and direction != 8:
            direction = 2
        if action == curses.KEY_RIGHT and direction != 4:
            direction = 6
        if action == curses.KEY_LEFT and direction != 6:
            direction = 4
        if action == curses.KEY_HOME and direction != 3:
            direction = 7
        if action == curses.KEY_END and direction != 9:
            direction = 1
        if action == curses.KEY_PPAGE and direction != 1:
            direction = 9
        if action == curses.KEY_NPAGE and direction != 7:
            direction = 3

        if direction == 6:
            head[1] += 1
        elif direction == 4:
            head[1] -= 1
        elif direction == 2:
            head[0] += 1
        elif direction == 8:
            head[0] -= 1
        elif direction == 7:
            head[1] -= 1
            head[0] -= 1
        elif direction == 1:
            head[1] -= 1
            head[0] += 1
        elif direction == 9:
            head[1] += 1
            head[0] -= 1
        elif direction == 3:
            head[1] += 1
            head[0] += 1

        message_1 = "WATCH OUT!"
        message_2 = "TROLLED!"
        message_3 = "HAHAAAA"
        message_4 = "Ráb@$ztál!"
        message_5 = "SURPRISE!"

        message_x = random.randint(1, 5)

        if message_x == 1:
            message_to_display = message_1
        if message_x == 2:
            message_to_display = message_2
        if message_x == 3:
            message_to_display = message_3
        if message_x == 4:
            message_to_display = message_4
        if message_x == 5:
            message_to_display = message_5

        if screen.inch(head[0], head[1]) == ord('+'):
            good_or_bad = random.randint(0, 5)
            global score
            if good_or_bad == 0 and score > 2:
                score = round(score/2)
                food_exist = False
                for to_delete in range(0, length-5):
                    deleted_co_ord = body[to_delete]
                    screen.addch(deleted_co_ord[0], deleted_co_ord[1], " ")
                for to_delete in range(0, length-5):
                    body.remove(body[0])
                length = 5
            elif good_or_bad == 0 and score < 3:
                food_exist = False
            else:
                score += 1
                length += 5
                food_exist = False
                troll_message(message_to_display)
        if screen.inch(head[0], head[1]) == ord('#'):
            snake_moves = False
            return score
        if screen.inch(head[0], head[1]) == ord('x'):
            snake_moves = False
            return score
        if screen.inch(head[0], head[1]) == ord('o'):
            snake_moves = False
            return score

        troll_speed = random.randint(0, 200)
        global remaining_time
        global speed
        if troll_speed == 0:
            remaining_time = 10050
            speed = 0.01
            troll_message(message_to_display)
        remaining_time -= 1
        if remaining_time < 10000:
            speed = 0.05

        troll_direction = random.randint(0, 200)
        if troll_direction == 0:
            troll_direction = random.randint(1, 9)
            if troll_direction != 5 and troll_direction + direction != 10:
                direction = troll_direction
                troll_message(message_to_display)

        troll_teleport_happens = random.randint(0, 200)
        if troll_teleport_happens == 0:
            global border_of_map
            y_head = random.randint(10, border_of_map[0]-10)
            x_head = random.randint(10, border_of_map[1]-10)
            head = [y_head, x_head]
            troll_message(message_to_display)

        screen.move(border_of_map[0] - 1, border_of_map[1] - 1)
        screen.refresh()

        if direction == 4 or direction == 6:
            time.sleep(speed)
        else:
            time.sleep(speed * 1.5)

        disapperaing_co_ord = body[0]
        if body.index(body[-1]) > length:
            screen.addch(disapperaing_co_ord[0], disapperaing_co_ord[1], " ")
            body.remove(body[0])

        global troll_message_remaining
        troll_message_remaining -= 1

        if troll_message_remaining < 10000 and len(troll_message_position) > 0:
            for item_number in range(0, len(troll_message_position)):
                str_to_remove_start = list(troll_message_position[item_number])
                screen.addstr(str_to_remove_start[0], str_to_remove_start[1], (" ")*10)
            for item_number in range(0, len(troll_message_position)):
                troll_message_position.remove(troll_message_position[0])

    return score


def troll_message(message):

    global troll_message_remaining
    global y
    global x
    troll_message_remaining = 10025
    y_message = random.randint(10, 2*y-20)
    x_message = random.randint(10, 2*x-20)
    screen.addstr(y_message, x_message, str(message))
    position = [y_message, x_message]
    troll_message_position.append(position)


def highscore():

    screen.nodelay(0)
    global score
    screen.clear()
    new_record = False
    global troll
    do_we_wanna_troll = random.randint(0, 1)
    if do_we_wanna_troll == 1:
        troll = True

    if troll is False:
        if os.path.isfile("rekord.txt") is True:

            read_highscore = open("rekord.txt", "r")
            highscorelist = read_highscore.readlines()
            read_highscore.close()
            maybe_highscore = highscorelist[0]

            if score > int(maybe_highscore):
                rewrite = open("rekord.txt", "w")
                rewrite.write(str(score))
                rewrite.close
                new_record = True

        else:
            rewrite = open("rekord.txt", "w")
            rewrite.write(str(score))
            rewrite.close
            new_record = True

        screen.addstr(y, x - 7, "score: " + str(score))

        if new_record:
            screen.addstr(y + 1, x - 7, "Highscore: " + str(score))
        else:
            screen.addstr(y + 1, x - 7, "Highscore: " + str(maybe_highscore))

        screen.addstr(y + 2, x - 7, "press HOME to restart, or END to escape")

    else:

        screen.addstr(y, x - 7, "oooh well.....")
        screen.addstr(y + 1, x - 7, "This time we didnt count your points")
        screen.addstr(y + 5, x - 7, "LOL")

    global lets_go

    exit_game = screen.getch()
    if exit_game == curses.KEY_END:
        lets_go = False
    if exit_game == curses.KEY_HOME:
        lets_go = True

    return lets_go


def reset_troll():

    global troll
    troll = False
    return troll


def reset_score():

    global score
    score = 0
    return score


def reset_length():

    global length
    length = 5
    return length


def reset_speed():

    global speed
    speed = 0.05
    return speed


def reset_remaining_time():

    global remaining_time
    remaining_time = 9999
    return remaining_time

while lets_go:

    menu()
    #create_map()
    game()
    highscore()
    reset_troll()
    reset_score()
    reset_length()
    reset_remaining_time()
    reset_speed()

curses.endwin()
