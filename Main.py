import pygame
from datetime import datetime

white = (255, 255, 255)
black = (0, 0, 0)
(width, height) = (800, 800)  # Dimension of the window
screen = pygame.display.set_mode((width, height))  # Making of the screen
pygame.display.set_caption("Cellular automaton")

gridSize = 36  # musi być wielokrotnością 2
drawGridLines = True
updateTime = 0.01
board = [];
file =open("test")
tablicatestowa=[]
for i in file:
    t=i.split(" ")
    for j in t:
        x=j.split(',')
        for w in x:
            w=int(w)
        tablicatestowa.append([int(x[0]),int(x[1]),int(x[2]),int(x[3])])




def initBoard():
    for y in range(gridSize):
        row = []
        for x in range(gridSize):
            row.append(0)
        board.append(row)


def drawGrid():
    for y in range(1, gridSize):
        pygame.draw.line(screen, black, (0, int((height / gridSize) * y)), (width, int((height / gridSize) * y)), 1)

    for x in range(1, gridSize):
        pygame.draw.line(screen, black, (int((width / gridSize) * x), 0), (int((width / gridSize) * x), height), 1)


def fillCell(x, y):
    if x < 0 or x > gridSize or y < 0 or y > gridSize:
        raise Exception("Invalid coords: " + str(x) + ":" + str(y));

    pygame.draw.rect(screen, black, (
        x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))


def placePattern(pattern, offset_x, offset_y):
    global board
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            if offset_y + y < len(board) and offset_x + x < len(board[offset_y + y]):
                board[offset_y + y][offset_x + x] = pattern[y][x]


def neighbourCount(x, y):
    UR = 0
    DR = 0
    DL = 0
    UL = 0
    if x == gridSize - 1 and y < gridSize - 1:
        UL = board[y][gridSize - 1]
        UR = board[y][0]
        DL = board[y + 1][x]
        DR = board[y + 1][0]
    if y == gridSize - 1 and x < gridSize - 1:
        UL = board[y][x]
        UR = board[y][x + 1]
        DL = board[0][x]
        DR = board[0][x + 1]
    if y == gridSize - 1 and x == gridSize - 1:
        UL = board[y][x]
        UR = board[gridSize - 1][0]
        DL = board[0][gridSize - 1]
        DR = board[0][0]
    if y < gridSize - 1 and x < gridSize - 1:
        UL = board[y][x]
        UR = board[y][x + 1]
        DL = board[y + 1][x]
        DR = board[y + 1][x + 1]

    neighbours = [UL, UR, DL, DR]
    return neighbours
def transform(tab,x,y,boards):
                UL=int(tab[0])
                UR=int(tab[1])
                DL=int(tab[2])
                DR=int(tab[3])

                if x == gridSize - 1 and y < gridSize - 1:
                    boards[y][gridSize - 1]=UL
                    boards[y][0]=UR
                    boards[y + 1][x]=DL
                    boards[y + 1][0]=DR
                if y == gridSize - 1 and x < gridSize - 1:
                    boards[y][x]=UL
                    boards[y][x + 1]=UR
                    boards[0][x]=DL
                    boards[0][x + 1]=DR
                if y == gridSize - 1 and x == gridSize - 1:
                    boards[y][x]=UL
                    boards[gridSize - 1][0]=UR
                    boards[0][gridSize - 1]=DL
                    boards[0][0]=DR
                if y < gridSize - 1 and x < gridSize - 1:
                    boards[y][x]=UL
                    boards[y][x + 1]=UR
                    boards[y + 1][x]=DL
                    boards[y + 1][x + 1]=DR

                boards=board
                return board


def processBoard():
        global board
        for y in range(0,int(len(board)),2):
            for x in range(0,int(len(board[y])),2):
                for i in range(0, len(tablicatestowa), 2):
                    nc = neighbourCount(x,y)
                    # tutaj zdefiniujemy zasady a potem x i y +1 i mamy drugą siatke K

                    if nc == tablicatestowa[i]:
                            test = tablicatestowa[i+1]
                            transform(test, x, y, board)
def processBoard2():
        for y in range(1,int(len(board)),2):
            for x in range(1,int(len(board[y])),2):
                for i in range(0, len(tablicatestowa), 2):
                    nc = neighbourCount(x, y)
                    # tutaj zdefiniujemy zasady a potem x i y +1 i mamy drugą siatke K

                    if nc == tablicatestowa[i]:
                        test = tablicatestowa[i + 1]
                        transform(test, x, y, board)





def drawCells():
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                fillCell(x, y)


pattern = [
    [0, 0, 0, 0, 0, 0, ],
    [0, 1, 0, 1, 0, 1, ],
    [0, 0, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 0, 0, ],
    [0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, ],
]

# pattern = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]

initBoard()
placePattern(pattern, 0, 0)

running = True
prevTime = datetime.now()

while running:
    time = datetime.now()
    screen.fill(white)

    if (time - prevTime).total_seconds() > updateTime:
        processBoard()
        prevTime = time
    time=datetime.now()
    if (time - prevTime).total_seconds() > updateTime:
        processBoard2()
        prevTime = time

    if drawGridLines:
        drawGrid()

    drawCells()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
