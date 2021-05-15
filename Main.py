import pygame
from datetime import datetime
import random
import numpy as np
from pygame.locals import *
import PySimpleGUI as sg
#Definicja kolorów RGB
white = (255, 255, 255)
black = (0, 0, 0)
(width, height) = (800, 800)  # Rozmiar okna
#Nazwa okna
pygame.display.set_caption("Automat Komórkowy")
#Flaga podwójnego buforu (zwiększa wydajność)
flags = DOUBLEBUF
#Rozdzielczość na podstawie rozmiarów okna
resolution=[width,height]
#Zdefiniowanie okna
screen = pygame.display.set_mode(resolution, flags, 16)
#Rozmiar siatki
gridSize = 100  # musi być wielokrotnością 2
#Opcja renderowania linii siatki
drawGridLines = False
#Minimalny interwał pomiedzy kolejnymi klatkami
updateTime = 0.01
#Inicjalizacja tablicy
board = []
#odczytanie pliku z zdefiniowanymi zasadami gry, w formacie X,X,X,X Y,Y,Y,Y
# kolejne X to stan sprawdzany, a Y- stan generowany w kolejności Lewy górny róg,
#Prawy górny róg, Lewy dolny róg, prawy dolny róg
filename="test"
randompatternsize=50

event, values = sg.Window('Wybierz zestaw reguł', [[sg.Text('Wybierz zestaw reguł:'), sg.Listbox(['Negacja.txt','NieDlaEpileptykow.txt', 'Interesujace.txt'], size=(20, 3), key='Choice')],
[sg.Text('Wybierz rozmiar generowanego wzoru'), sg.Listbox(['10','20', '50','100'], size=(20, 3), key='Choice2')],
    [sg.Button('Ok'), sg.Button('Domyślny')]]).read(close=True)

if event == 'Ok':

    try:
        sg.popup(f'Wybrano {values["Choice"][0]}')
        filename=values["Choice"][0]
        randompatternsize=int(values["Choice2"][0])
    except Exception:
        filename="test"
        randompatternsize = 50



else:
    sg.popup('W takim razie uruchomiona zostanie wersja domyślna')


file =open(filename)
tablicatestowa=[]
for i in file:
    t=i.split(" ")
    for j in t:
        x=j.split(',')
        for w in x:
            w=int(w)
        tablicatestowa.append([int(x[0]),int(x[1]),int(x[2]),int(x[3])])



#Funkcja inicjalizująca tablicę o rozmiarze gridSize x gridSize
def initBoard():
    for y in range(gridSize):
        row = []
        for x in range(gridSize):
            row.append(0)
        board.append(row)

#Funkcja rysująca linie siatki
def drawGrid():
    for y in range(1, gridSize):
        pygame.draw.line(screen, black, (0, int((height / gridSize) * y)), (width, int((height / gridSize) * y)), 1)

    for x in range(1, gridSize):
        pygame.draw.line(screen, black, (int((width / gridSize) * x), 0), (int((width / gridSize) * x), height), 1)


#Funkcja wypełniająca białe piksele
def fillCellWhite(x, y):
    if x < 0 or x > gridSize or y < 0 or y > gridSize:
        raise Exception("Invalid coords: " + str(x) + ":" + str(y));

    pygame.draw.rect(screen, white, (
        x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))


#Funkcja wypełniająca czarne piksele
def fillCellBlack(x, y):
    if x < 0 or x > gridSize or y < 0 or y > gridSize:
        raise Exception("Invalid coords: " + str(x) + ":" + str(y));

    pygame.draw.rect(screen, black, (
        x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))

#Funkcja umieszczająca piksele w odpowiedniej części tablicy zależnej od offsetu
def placePattern(pattern, offset_x, offset_y):
    global board
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            if offset_y + y < len(board) and offset_x + x < len(board[offset_y + y]):
                board[offset_y + y][offset_x + x] = pattern[y][x]

#Funkcja sprawdzająca sąsiednie komórki do zadanej
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
#Funkcja przekształcająca dane komórki na podstawie wartości tablicy tab
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

#Funkcja obliczająca zmiany dla siatki 2x2 bez przesunięcia
def processBoard():
        global board
        for y in range(0,int(len(board)),2):
            for x in range(0,int(len(board[y])),2):
                for i in range(0, len(tablicatestowa), 2):
                    nc = neighbourCount(x,y)
                    #definicja zasad według których działa funkcja transform

                    if nc == tablicatestowa[i]:
                            test = tablicatestowa[i+1]
                            transform(test, x, y, board)
        return board
#Funkcja obliczająca zmiany dla siatki 2x2 z przesunięciem o 1 piksel w każdym wymiarze
def processBoard2():
        global board
        for y in range(1,int(len(board)),2):
            for x in range(1,int(len(board[y])),2):
                for i in range(0, len(tablicatestowa), 2):
                    nc = neighbourCount(x, y)
                    #definicja zasad według których działa funkcja transform

                    if nc == tablicatestowa[i]:
                        test = tablicatestowa[i + 1]
                        transform(test, x, y, board)
        return board



#Funkcja rysująca komórki na podstawie wartości x,y
def drawCells():
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                fillCellBlack(x, y)
            if board[y][x] == 0:
                fillCellWhite(x, y)

#Przykładowy wzór do wykorzystania w ramach testów
pattern = [
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ],
[1,1,1,1,1,1,1,1 ]
]
#Funkcja generująca losowe wzory
def drawrandompatern(size):
    tab= np.random.randint(2,size=(size, size))
    return tab


#inicjalizacja tablicy
initBoard()
#Umieszczenie wzoru w tablicy
placePattern(drawrandompatern(randompatternsize), 0, 0)
#placePattern(pattern,0,0)

#Pobranie aktualnego czasu
prevTime = datetime.now()
#Pętla zapewniająca ciągłość pracy programu
while 1:
    #pobranie drugiej próbki czasu
    time = datetime.now()
    #Funkcja wypełniająca ekran
    screen.fill(white)
    #Na podstawie zmiany w pobranych próbkach czasu wykonywana jest procedura
    #odświeżenia tablicy z naniesieniem zmian
    if (time - prevTime).total_seconds() > updateTime:
        processBoard()
        drawCells()
        pygame.display.flip()
        processBoard2()
        drawCells()
        pygame.display.flip()
        prevTime = time
        drawGridLines=not drawGridLines

    #Opcja narysowania linii siatki w zależnosci od przyjętego wcześniej parametru
    if drawGridLines:
        drawGrid()
    #Narysowanie tablicy
    drawCells()
    #Wyświetlenie zmian
    pygame.display.flip()
    #Możliwość zamknięcia programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
