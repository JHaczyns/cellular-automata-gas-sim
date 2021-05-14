import pygame
from datetime import datetime

black = (255, 255, 255)
white = (0, 0, 0)
(width, height) = (800, 800)  # Dimension of the window
screen = pygame.display.set_mode((width, height))  # Making of the screen
pygame.display.set_caption("Cellular automaton")

gridSize = 6  # musi być wielokrotnością 2
drawGridLines = False
updateTime = 0.05
board = [];


def initBoard():
    for y in range(gridSize):
        row = []
        for x in range(gridSize):
            row.append(0)
        board.append(row)


def drawGrid():
    for y in range(1, gridSize):
        pygame.draw.line(screen, white, (0, int((height / gridSize) * y)), (width, int((height / gridSize) * y)), 1)

    for x in range(1, gridSize):
        pygame.draw.line(screen, white, (int((width / gridSize) * x), 0), (int((width / gridSize) * x), height), 1)


def fillCell(x, y):
    if x < 0 or x > gridSize or y < 0 or y > gridSize:
        raise Exception("Invalid coords: " + str(x) + ":" + str(y));

    pygame.draw.rect(screen, white, (
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


def processBoard():
    global board
    Count =2
    if (Count % 2 == 0):
        boardCopy = board
        Count=Count+1
        for y in range(int(len(board))//2):
            for x in range(int(len(board))//2):
                nc = neighbourCount(2 * x, 2 * y)
                if x == gridSize - 1 and y < gridSize - 1:
                    transformed = [
                        boardCopy[y][gridSize - 1],
                        boardCopy[y][0],
                        boardCopy[y + 1][x],
                        boardCopy[y + 1][0]
                    ]
                if y == gridSize - 1 and x < gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[y][x + 1],
                        boardCopy[0][x],
                        boardCopy[0][x + 1]
                    ]
                if y == gridSize - 1 and x == gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[gridSize - 1][0],
                        boardCopy[0][gridSize - 1],
                        boardCopy[0][0]
                    ]
                if y < gridSize - 1 and x < gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[y][x + 1],
                        boardCopy[y + 1][x],
                        boardCopy[y + 1][x + 1]
                    ]
                # tutaj zdefiniujemy zasady a potem x i y +1 i mamy drugą siatke K
                if nc == [1, 0, 0, 0]:
                    if 2*y < gridSize - 1 and 2*x < gridSize - 1:
                        #  transformed[0]=0
                        # transformed[1]=0
                        # transformed[2]=0
                        # transformed[3]=1
                        boardCopy[2*y][2*x]=0
                        boardCopy[2*y][2*x + 1]=0
                        boardCopy[2*y + 1][2*x]=0
                        boardCopy[2*y + 1][2*x + 1]=1

    if (Count%2 == 1):
        boardCopy = board
        Count=Count+1
        for y in range(int(len(board))//2):
            for x in range(int(len(board))//2):

                nc = neighbourCount(2*x+1,2*y+1)
                if x == gridSize - 1 and y < gridSize - 1:
                    transformed = [
                        boardCopy[y][gridSize - 1],
                        boardCopy[y][0],
                        boardCopy[y + 1][x],
                        boardCopy[y + 1][0]
                    ]
                if y == gridSize - 1 and x < gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[y][x + 1],
                        boardCopy[0][x],
                        boardCopy[0][x + 1]
                    ]
                if y == gridSize - 1 and x == gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[gridSize - 1][0],
                        boardCopy[0][gridSize - 1],
                        boardCopy[0][0]
                    ]
                if y < gridSize - 1 and x < gridSize - 1:
                    transformed = [
                        boardCopy[y][x],
                        boardCopy[y][x + 1],
                        boardCopy[y + 1][x],
                        boardCopy[y + 1][x + 1]
                    ]
                # tutaj zdefiniujemy zasady a potem x i y +1 i mamy drugą siatke K
                if nc == [1, 0, 0, 0]:
                    if 2*y < gridSize - 2 and 2*x < gridSize - 2:
                        #  transformed[0]=0
                        # transformed[1]=0
                        # transformed[2]=0
                        # transformed[3]=1
                        boardCopy[2*y+1][2*x+1] = 0
                        boardCopy[2*y+1][2*x + 2] = 0
                        boardCopy[2*y + 2][2*x+1] = 0
                        boardCopy[2*y + 2][2*x + 2] = 1

    board = boardCopy


def drawCells():
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                fillCell(x, y)


pattern = [
    [1, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, ],
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
    screen.fill(black)

    if (time - prevTime).total_seconds() > updateTime:
        processBoard()

        prevTime = time

    if drawGridLines:
        drawGrid()

    drawCells()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
