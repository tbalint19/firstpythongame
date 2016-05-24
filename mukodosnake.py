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
hatar = screen.getmaxyx()
screen.border()
curses.noecho()
m=int(hatar[0]/2) #y
n=int(hatar[1]/2) #x
terkep = 5
pontszam = 0
mehet = True
troll = False
a = "choose a map, press a number(1-9, turn off numlock)): "
how_many = 0
troll_death = 1

def menu():

    screen.clear()
    global a
    global terkep
    screen.addstr(m, n-int(len(a)/2), "choose a map, press a number(1-9, turn off numlock)): ")
    choose = screen.getch()
    if choose == curses.KEY_END :
        terkep = 1
    elif choose == curses.KEY_DOWN :
        terkep = 2
    elif choose == curses.KEY_NPAGE :
        terkep = 3
    elif choose == curses.KEY_LEFT :
        terkep = 4
    elif choose == curses.KEY_RIGHT :
        terkep = 6
    elif choose == curses.KEY_HOME :
        terkep = 7
    elif choose == curses.KEY_UP :
        terkep = 8
    elif choose == curses.KEY_PPAGE :
        terkep = 9

    screen.addstr(m, n-int(len(a)/2), " "*int(len(list(a))+2)) #elég tré, de ez törli ki a szöveget
    return terkep

def createMap() :

    if terkep == 1 :
        screen.addch(m, n, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n , 'x', curses.color_pair(2))
        for a in range(-(n-7), n-7) :
            screen.addch(m, n+a , 'x', curses.color_pair(2))

    if terkep == 2 :
        screen.addch(m, n, 'x')
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n+a, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n-a, 'x', curses.color_pair(2))

    if terkep == 3 :
        screen.addch(m, n, 'x')
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n+a, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n-a, 'x', curses.color_pair(2))
        for a in range(-(n-7), n-7) :
            screen.addch(m, n+a , 'x', curses.color_pair(2))

    if terkep == 4 :

        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n+a+10, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n-a+10, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n+a-10, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n-a-10, 'x', curses.color_pair(2))

    if terkep == 6 :

        screen.addch(m, n, 'x')

        for a in range(-(n-7), n-7) :
            screen.addch(m, n+a , 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n+10, 'x', curses.color_pair(2))
        for a in range(-(m-7), m-7) :
            screen.addch(m+a, n-10, 'x', curses.color_pair(2))


def game() :

    global how_many
    screen.nodelay(1)

    fej = [6, 6] # a kigyo a 6,6 pontnal jelenik meg (1,1 - bal felso sarok)
    test = [fej[:]]*5

    direction =  6 # 6: right, 2: down, 4: left, 8: up - a kigyo jobbra indul
    jatek = True
    jokaja = False
    rosszkaja = False
    vege = test[-1][:]

    while jatek :

        global pontszam
        pontszam = int(len(test)-5)
        screen.addstr(0, 2*n-15, "pontszam: " + str(pontszam))

        while not jokaja :
            q, w = random.randrange(1, hatar[0]-1), random.randrange(1, hatar[1]-1)
            y, x = random.randrange(1, hatar[0]-1), random.randrange(1, hatar[1]-1)
            if screen.inch(y, x) == ord(' '):
                jokaja = True
                screen.addch(y, x, '+')
                screen.addch(q, w, '-')

        if vege not in test :

            screen.addch(vege[0], vege[1], ' ')

        screen.addch(fej[0], fej[1], 'o', curses.color_pair(1))

        #mozgatas

        action = screen.getch()
        if action == curses.KEY_UP and direction != 2 :
            direction = 8
        if action == curses.KEY_DOWN and direction != 8 :
            direction = 2
        if action == curses.KEY_RIGHT and direction != 4 :
            direction = 6
        if action == curses.KEY_LEFT and direction != 6 :
            direction = 4
        if action == curses.KEY_HOME and direction != 3 :
            direction = 7
        if action == curses.KEY_END and direction != 9 :
            direction = 1
        if action == curses.KEY_PPAGE and direction != 1 :
            direction = 9
        if action == curses.KEY_NPAGE and direction != 7 :
            direction = 3

        #iranyok

        if direction == 6 :
            fej[1] += 1
        elif direction == 4 :
            fej[1] -= 1
        elif direction == 2 :
            fej[0] += 1
        elif direction == 8 :
            fej[0] -= 1
        elif direction == 7 :
            fej[1] -= 1
            fej[0] -= 1
        elif direction == 1 :
            fej[1] -= 1
            fej[0] += 1
        elif direction == 9 :
            fej[1] += 1
            fej[0] -= 1
        elif direction == 3 :
            fej[1] += 1
            fej[0] += 1


        vege = test[-1]

        for z in range(len(test)-1, 0, -1) :
            test[z] = test[z-1][:]

        test[0] = fej[:]

        if screen.inch(fej[0], fej[1]) != ord(' ') :
            if screen.inch(fej[0], fej[1]) == ord('+') :
                jokaja = False
                test.append(test[-1])
            elif screen.inch(fej[0], fej[1]) == ord('-') :
                jatek = False
                how_many = 0
                return how_many
            else :
                jatek = False
                how_many = 0
                return how_many

        screen.move(hatar[0]-1, hatar[1]-1)
        screen.refresh()

        speed =  0.5/len(test)

        if direction == 4 or direction == 6 :

            time.sleep(speed)

        else :

            time.sleep(speed*1.5)



        troll_death = random.randint(0, 20)
        if troll_death == 0 and how_many > 10:
            how_many = 0
            return how_many
            global troll
            troll = True
            jatek = False
        else:
            jatek = True

        how_many += 1

    return troll
    return pontszam
    return how_many


def highscore() :
    global pontszam
    screen.nodelay(0)
    screen.clear()
    ujrekord = False
    global troll

    if troll == False :
        if os.path.isfile("rekord.txt") is True :

            r = open("rekord.txt", "r")
            highscorelist = r.readlines()
            r.close()
            maybeHS = highscorelist[0]

            if pontszam > int(maybeHS) :
                w = open("rekord.txt", "w")
                w.write(str(pontszam))
                w.close
                ujrekord = True

        else :
            w = open("rekord.txt", "w")
            w.write(str(pontszam))
            w.close
            ujrekord = True

        screen.addstr(m, n-7, "pontszam: " + str(pontszam))
        if ujrekord == True :

            screen.addstr(m+1, n-7, "rekord: " + str(pontszam))
        else :
            screen.addstr(m+1, n-7, "rekord: " + str(maybeHS))

        screen.addstr(m+2, n-7, "press HOME to restart, press END to escape")

        kilep = screen.getch()
        global mehet

        if kilep == curses.KEY_END :
            mehet = False
        if kilep == curses.KEY_HOME :
            mehet = True


        return mehet

    else :

        screen.addstr(m, n-7, "Ha ha ha loooooooser xDDDD")
        screen.addstr(m-1, n-7, "Do you want to try again?")

        kilep = screen.getch()
        global mehet

        if kilep == curses.KEY_END :
            mehet = False
        if kilep == curses.KEY_HOME :
            mehet = True


        return mehet


while mehet == True :

    menu()
    createMap()
    game()
    highscore()


curses.endwin()
