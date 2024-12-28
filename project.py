#Catch the Ball



#GAME RULES
#Players can choose their preferred colors.
#Whoever catches 5 of their preferred balls first wins
#However if any player misses their respective colors 15 times then the opponent wins by default





from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

print(f"GAME RULES:-->\nPlayers can CHOOSE their preferred COLOR.\nThe PLAYER who catches 5 of their preferred balls FIRST WINS\nHowever if any player MISSES their respective colors 15 times then the OPPONENT WINS BY DEFAULT\nPRESS PAUSE BUTTON TO START")
colors={"yellow":[1,1,0],"red":[1,0,0],"blue":[0,0,1],"green":[0,1,0],"aqua":[0,1,1],"purple":[0.5,0,0.5],"orange":[1,0.5,0]}
a = input("Preferred color for Player 1: ").lower()

while a not in colors.keys():
    a = input("Not available! Player 1 choose another color: ").lower()
color_for_p1 = colors.get(a)
colors.pop(a)
b = input(f"Cannot choose {a}. Preferred color for Player 2: ")
while b not in colors.keys():
    b = input("Not available! Player 2 choose another color: ").lower()
color_for_p2 = colors.get(b)
speed = 1
scoreForP1 = 0
scoreForP2= 0
W_Width, W_Height = 500,500
BasketPos = [15,45]
BasketInfo = {'radius': 30, 'center': [0, 0], 'color': color_for_p1,'fill_level':0}
BasketPos2 = [400, 100]
BasketInfo2 = {'radius': 30, 'center': [0, 0], 'color': color_for_p2 ,'fill_level':0}
fill_basket= []
fill_basket2= []

balls2 = []
missed_P1_balls = 0
missed_P2_balls=0
pause_symbol = True
isfrozen = True
isGameOver = False
p1Win=False
p2Win=False
pause_box = {"x": 220, "y": 460, "width": 40, "height": 40}
pause_box2 = {"x": 240,"y": 460,"width": 20,"height": 40}

restart_box = { 'x': 0, 'y': 460, 'width': 40, 'height': 40}

cross_box = { 'x': 460, 'y': 460, "width": 40, "height": 40}

def drawPause():
    global pause_symbol, isfrozen #used to represent two different states of pause button
    if pause_symbol and isfrozen:
        eightWaySymmetry(220, 460, 220, 500, (1, 0.75, 0))
        eightWaySymmetry(220, 460, 260, 480, (1, 0.75, 0))
        eightWaySymmetry(260, 480, 220, 500, (1, 0.75, 0))
    else:
        eightWaySymmetry(240, 460, 240, 500, (1, 0.75, 0))
        eightWaySymmetry(260, 460, 260, 500, (1, 0.75, 0))


def drawRestart():
    square_center = (25, 470)
    square_size = 40
    square_color = (1, 1, 1)

    # 4 corners
    p1_x = int(square_center[0] + square_size / 2)
    p1_y = int(square_center[1] + square_size / 2)

    p2_x = int(square_center[0] - square_size / 2)
    p2_y = int(square_center[1] + square_size / 2)

    p3_x = int(square_center[0] - square_size / 2)
    p3_y = int(square_center[1] - square_size / 2)

    p4_x = int(square_center[0] + square_size / 2)
    p4_y = int(square_center[1] - square_size / 2)

    # List of corners
    corners = [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)]


    for i in range(4):

        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        eightWaySymmetry(x1, y1, x2, y2, square_color)

def drawCross():
    eightWaySymmetry(460, 460, 500, 500, (1, 0, 0))
    eightWaySymmetry(460, 500, 500, 460, (1, 0, 0))

def convertCoordinate(x,y):
    global W_Width, W_Height
    a = x
    b = W_Height-y
    return (a,b)


def drawPoints(x, y, color):
    glColor3f(*color)
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def cirPoints(x, y, color, center):
    drawPoints(x+center[0], y+center[1], color)
    drawPoints(-x+center[0], y+center[1], color)
    drawPoints(x+center[0], -y+center[1], color)
    drawPoints(-x+center[0], -y+center[1], color)
    drawPoints(y+center[0], x+center[1], color)
    drawPoints(-y+center[0], x+center[1], color)
    drawPoints(y+center[0], -x+center[1], color)
    drawPoints(-y+center[0], -x+center[1], color)


def convertzone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convertzoneM(x,y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6


def midpointLine(x1, y1, x2, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
    y = y1
    # print(x1, y1, x2, y2, zone)
    for x in range(x1, x2+1):
        oz_x, oz_y = convertzoneM(x, y, zone)

        drawPoints(oz_x , oz_y, color)
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1

def eightWaySymmetry(x1, y1, x2, y2, color = (1, 1, 0)):
    zone = findzone(x1, y1, x2, y2)
    # print(zone)
    x1, y1 = convertzone0(x1, y1, zone)
    x2, y2 = convertzone0(x2, y2, zone)
    midpointLine(x1, y1, x2, y2, zone, color)

def midpointCircle(radius, color, center = (0,0)):
    x = 0
    y = radius
    d = 1 - radius
    cirPoints(x, y, color, center)
    while x < y:
        if d < 0:
            d = d + 2*x+3
            x = x+1
        else:
            d = d + 2*(x-y)+5
            x = x+1
            y = y-1
        cirPoints(x, y, color, center)



def summonNewBall():
    global color_for_p1,color_for_p2
    x = random.randint(10, 490)
    y = random.randint(350, 450)
    radius = 10

    if random.random() < 0.5:
        if random.random()< 0.5:

           color_choice = color_for_p1
        else:
           color_choice = color_for_p2
    else:

        color_choice = random.choice([[0, .7, .3], [1, 1, 1], [1, .2,.7], [.2, 0.5, .8], [0.5, 1, 0.5],[.4,.4,.4]])

    speed = random.uniform(0.1, 0.4)

    # Horizontal wiggle
    horizontal_speed = 0
    if random.random() < 0.5:
        horizontal_speed = random.uniform(-0.5, .5)

    return {'radius': radius, 'center': [x, y], 'color': color_choice, 'speed': speed, 'horizontal_speed': horizontal_speed}

def has_collided(circle1, circle2):
    circle1_center_x, circle1_center_y = circle1['center']
    circle2_center_x, circle2_center_y = circle2['center']
    distance = ((circle1_center_x - circle2_center_x) ** 2 + (circle1_center_y - circle2_center_y) ** 2) ** 0.5
    return distance < (circle1['radius'] + circle2['radius'])

def summonBalls():
    global balls2

    if len(balls2) < 15:
        ballSummon = summonNewBall()
        collided = False

        for existing in balls2:
            if has_collided(ballSummon, existing):
                collided = True
                break

        if not collided:
            balls2.append(ballSummon)

def drawBasket(basket_pos, basket_info):

    center_x, center_y = basket_pos
    radius = basket_info['radius']
    color = basket_info['color']
    fill_level=basket_info['fill_level']
    # find the point of rectangle
    left = center_x - radius
    right = center_x + radius
    bottom = center_y - radius


    for x in range(int(left), int(right) + 1):
        drawPoints(x, bottom, color)  # Bottom edge

    for y in range(int(bottom), int(center_y) + 1):
        drawPoints(left, y, color)  # Left edge
        drawPoints(right, y, color) # Right edge

    fill_height = int((fill_level / 10) * radius * 2)
    fill_color = [0.5, 0.5, 0.5]
    for y in range(center_y - radius, center_y - radius + fill_height + 1):
        for x in range(center_x - radius + 1, center_x + radius):
            drawPoints(x, y, fill_color)

def isBallInBasket(ball, basket):

    distance = ((ball['center'][0] - basket[0]) ** 2 + (ball['center'][1] - basket[1]) ** 2)**0.5

    if distance < ball['radius'] + BasketInfo['radius']:
        return True
    return False


def drawBalls():
    global balls2, scoreForP1, scoreForP2, missed_P1_balls, missed_P2_balls,color_for_p1,color_for_p2,a,b


    for ball in balls2[:]:
        ball['center'][1] -= ball['speed']


        if ball['horizontal_speed'] != 0:
            ball['center'][0] += ball['horizontal_speed']

            if ball['center'][0] < 10:
                ball['horizontal_speed'] = abs(ball['horizontal_speed'])
            elif ball['center'][0] > 490:
                ball['horizontal_speed'] = -abs(ball['horizontal_speed'])

        # scoring for both
        if isBallInBasket(ball, BasketPos):
            if ball['color'] == color_for_p1:
                scoreForP1 += 1
                print("Player 1 scored:", scoreForP1)
                BasketInfo['fill_level'] = min(10, BasketInfo.get('fill_level', 0) + 1)
            else:
                print(f"OOPSSS Player One!!! Not {a} Color. Try Again!")
                scoreForP1 = 0
                BasketInfo['fill_level']=0
            balls2.remove(ball)

        elif isBallInBasket(ball, BasketPos2):
            if ball['color'] == color_for_p2 :
                scoreForP2 += 1
                print("Player 2 scored:", scoreForP2)
                BasketInfo2['fill_level'] = min(10, BasketInfo2.get('fill_level', 0) + 1)
            else:
                print(f"YUCKK Player 2!! Not {b} Color. Go again!!")
                scoreForP2 = 0
                BasketInfo2['fill_level']=0
            balls2.remove(ball)

        elif ball['center'][1] < 0:
            balls2.remove(ball)
            if ball['color'] == color_for_p1 :
                missed_P1_balls += 1
                if 5 - missed_P1_balls > 0:
                    print(f"CAREFUL! Player 1 have {15 - missed_P1_balls} chances left.")
            if ball['color'] == color_for_p2:
                missed_P2_balls += 1
                if 5 - missed_P2_balls > 0:
                    print(f"WARNING! Player 2 have {15 - missed_P2_balls} chances left.")

        midpointCircle(ball['radius'], ball['color'], ball['center'])
    summonBalls()


def animate():
    global isGameOver, isfrozen
    if not isGameOver and not isfrozen:
        summonBalls()
        drawBalls()
        glutPostRedisplay()
        time.sleep(0.001)


def checkGameOver():
    global balls2, BasketInfo,isGameOver, missed_P1_balls,missed_P2_balls,p1Win,p2Win,color_for_p1,color_for_p2, isfrozen,pause_symbol,a,b

    if missed_P1_balls>= 15:
        print(f"GAMEOVER!! Player Two Won by Default. Player 1 missed more than 15 {a} balls")
        isGameOver = True
        p2Win=True

        restartFunction(True,True)
    if missed_P2_balls>= 15:
        print(f"GAMEOVER!! Player One Won by Default. Player 2 missed more than 15 { b } balls")
        isGameOver = True
        p1Win=True

        restartFunction(True,True)
    if scoreForP1 == 5:
        print(f"Congratulations! Player One win with a score of {scoreForP1}!")
        isGameOver = True
        p1Win=True

        restartFunction(True,True)
    if scoreForP2 == 5:
        print(f"Congratulations! Player Two win with a score of {scoreForP2}!")
        isGameOver = True
        p1Win=True

        restartFunction(True,True)

def specialKeyListener(key,x,y):
    global BasketPos2, BasketInfo2
    if key == GLUT_KEY_RIGHT:
        if BasketPos2[0] + BasketInfo2['radius'] < W_Width - 10:
            BasketPos2[0] += 15
    if key == GLUT_KEY_LEFT:
        if BasketPos2[0] - BasketInfo2['radius'] > 10:
            BasketPos2[0] -= 15
    if key == GLUT_KEY_UP:
        if BasketPos2[1] + BasketInfo2['radius'] < W_Height - 300:
            BasketPos2[1] += 15
    if key == GLUT_KEY_DOWN:
        if BasketPos2[1] - BasketInfo2['radius'] > 10:
            BasketPos2[1] -= 15
    glutPostRedisplay()


def keyboardListener(key,x,y):
    global BasketPos, BasketInfo

    if key == b'a':
        if BasketPos[0] - BasketInfo['radius'] > 10:
            BasketPos[0] -= 15
    if key == b'd':
        if BasketPos[0] + BasketInfo['radius'] < W_Width - 10:
            BasketPos[0] += 15
    if key == b'w':
        if BasketPos[1] + BasketInfo['radius'] < W_Height - 300:
            BasketPos[1] += 15
    if key == b's':
        if BasketPos[1] - BasketInfo['radius'] > 10:
            BasketPos[1] -= 15

    glutPostRedisplay()


def restartFunction(gO = False,pS = False):
                global BasketPos, BasketInfo, balls2, scoreForP1,scoreForP2, isGameOver, pause_symbol, isfrozen, restart_box, cross_box, pause_box, pause_box2, missed_P2_balls,missed_P1_balls,BasketPos2, BasketInfo2,color_for_p1,color_for_p2
                BasketPos = [15,45]
                BasketInfo = {'radius': 30, 'center': [0,0], 'color': color_for_p1,'fill_level':0}
                BasketPos2 = [400,100]
                BasketInfo2 = {'radius': 30, 'center': [0,0], 'color': color_for_p2,'fill_level':0}
                balls2 = []
                scoreForP1 = 0
                scoreForP2= 0
                pause_symbol = pS
                isGameOver = gO
                isfrozen = False
                missed_P2_balls =0
                missed_P1_balls =0

def mouseListener(button, state, x, y):
    global BasketPos, BasketInfo, balls2, scoreForP1,scoreForP2, isGameOver, pause_symbol, isfrozen, restart_box, cross_box, pause_box, pause_box2, missed_P2_balls,missed_P1_balls,BasketPos2, BasketInfo2,color_for_p1,color_for_p2
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            adj_x, adj_y = convertCoordinate(x, y)
            if adj_x >= restart_box['x'] and adj_x <= restart_box['x'] + restart_box['width'] and adj_y >= restart_box['y'] and adj_y <= restart_box['y'] + restart_box['height']:
                restartFunction()
            if adj_x >= cross_box['x'] and adj_x <= cross_box['x'] + cross_box['width'] and adj_y >= cross_box['y'] and adj_y <= cross_box['y'] + cross_box['height']:
                print("GoodBye")
                glutLeaveMainLoop()
            if pause_symbol:
                if adj_x >= pause_box["x"] and adj_x <= pause_box["x"] + pause_box["width"] and adj_y >= pause_box["y"] and adj_y <= pause_box["y"] + pause_box["height"]:
                    pause_symbol = not pause_symbol
                    isfrozen = not isfrozen
            elif adj_x >= pause_box2["x"] and adj_x <= pause_box2["x"] + pause_box2["width"] and adj_y >= pause_box2["y"] and adj_y <= pause_box2["y"] + pause_box2["height"]:
                pause_symbol = not pause_symbol
                isfrozen = not isfrozen





def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global BasketInfo ,BasketInfo2 , BasketPos , BasketPos2
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    drawBasket(BasketPos, BasketInfo)
    drawBasket(BasketPos2, BasketInfo2)

    drawBalls()
    summonBalls()
    checkGameOver()
    drawRestart()
    drawPause()
    drawCross()

    glutSwapBuffers()

glutInit()

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Ball")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()