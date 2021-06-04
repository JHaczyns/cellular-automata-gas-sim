import pygame
from datetime import datetime

import numpy as np
from pygame.locals import *
import PySimpleGUI as sg
import itertools

#Definicja kolorów RGB
white = (255, 255, 255)
black = (0, 0, 0)
(width, height) = (1000, 1000)  # Rozmiar okna
#Nazwa okna
pygame.display.set_caption("Automat Komórkowy")
#Flaga podwójnego buforu (zwiększa wydajność)
flags=DOUBLEBUF
#Rozdzielczość na podstawie rozmiarów okna

#Zdefiniowanie okna

#Rozmiar siatki
gridSize = 200 # musi być wielokrotnością 2
(width, height) = (4*gridSize, 4*gridSize)  # Rozmiar okna
resolution=[width,height]
screen = pygame.display.set_mode(resolution,flags,16)
# Rozmiar okna
#Opcja renderowania linii siatki
drawGridLines = False
#Minimalny interwał pomiedzy kolejnymi klatkami
updateTime = 0.01
#Inicjalizacja tablicy
board = []
#odczytanie pliku z zdefiniowanymi zasadami gry, w formacie X,X,X,X Y,Y,Y,Y
# kolejne X to stan sprawdzany, a Y- stan generowany w kolejności Lewy górny róg,
#Prawy górny róg, Lewy dolny róg, prawy dolny róg
filename= "Pliki testowe/test"
randompatternsize=50
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
event, values = sg.Window('Wybierz zestaw reguł', [[sg.Text('Wybierz zestaw reguł:'), sg.Listbox(['Negacja.txt','NieDlaEpileptykow.txt', 'Interesujace.txt'], size=(20, 3), key='Choice')],
[sg.Text('Wybierz rozmiar generowanego wzoru'), sg.Listbox(['10','20', '50','100'], size=(20, 3), key='Choice2')],
    [sg.Button('Ok'), sg.Button('Domyślny')]]).read(close=True)

if event == 'Ok':

    try:
        sg.popup(f'Wybrano {values["Choice"][0]}')
        filename="Pliki testowe/"+values["Choice"][0]
        randompatternsize=int(values["Choice2"][0])
    except Exception:
        filename= "Pliki testowe/test"
        randompatternsize = 50




else:
    sg.popup('W takim razie uruchomiona zostanie wersja domyślna')

tablicaliczbowa=[[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]

file =open(filename)
tablicatestowa=[]
for i in file:
    t=i.split(" ")
    for j in t:
        x=j.split(',')
        for w in x:
            w=int(w)
        tablicatestowa.append([int(x[0]),int(x[1]),int(x[2]),int(x[3])])

tablicaregulowa=[]

file =open("Gaz")
tablicatestowa=[]
for i in file:
        tablicaregulowa.append(i)

def randomrules(range):
    tab = np.random.randint(range, size=(16))
    return tab

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
    # if x < 0 or x > gridSize or y < 0 or y > gridSize:
    #     raise Exception("Invalid coords: " + str(x) + ":" + str(y));

    pygame.draw.rect(screen, white, (
         x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))

    #pygame.draw.rect(screen, white, (x ,y,1,1))
#Funkcja wypełniająca czarne piksele
def fillCellBlack(x, y):
    # if x < 0 or x > gridSize or y < 0 or y > gridSize:
    #     raise Exception("Invalid coords: " + str(x) + ":" + str(y));
    pygame.draw.rect(screen, black, (
         x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))

    #pygame.draw.rect(screen, black, ( x ,y,1,1))
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
def neighbourCount2(x, y):
    count =0;
    if y < gridSize - 1 and x < gridSize - 1:

        count = 1*board[y][x]+2*board[y][x + 1] + 4* board[y + 1][x] + 8*board[y + 1][x + 1]

    if x == gridSize - 1 and y < gridSize - 1:

        count=1* board[y][gridSize - 1]+2* board[y][0]+4* board[y + 1][x]+8* board[y + 1][0]
    if y == gridSize - 1 and x < gridSize - 1:

        count =1* board[y][x]+2* board[y][x + 1]+ 4*board[0][x]+ 8*board[0][x + 1]
    if y == gridSize - 1 and x == gridSize - 1:

        count = board[y][x]+ + 2*board[gridSize - 1][0] +4*board[0][gridSize - 1]+ 8*board[0][0]

    return count;





def transform2(x,y,boards,tab):
    # count=neighbourCount2(x,y);
    # wynik=int(tablicaregulowa[count])
    #
    # UL = int(tablicaliczbowa[wynik][3])
    # UR = int(tablicaliczbowa[wynik][2])
    # DL = int(tablicaliczbowa[wynik][1])
    # DR = int(tablicaliczbowa[wynik][0])
    if y < gridSize - 1 and x < gridSize - 1:

        count = 1 * board[y][x] + 2 * board[y][x + 1] + 4 * board[y + 1][x] + 8 * board[y + 1][x + 1]
        wynik = int(tab[count])
        UL = int(tablicaliczbowa[wynik][3])
        UR = int(tablicaliczbowa[wynik][2])
        DL = int(tablicaliczbowa[wynik][1])
        DR = int(tablicaliczbowa[wynik][0])


        boards[y][x] = UL
        boards[y][x + 1] = UR
        boards[y + 1][x] = DL
        boards[y + 1][x + 1] = DR


    if x == gridSize - 1 and y < gridSize - 1:

        count = 1 * board[y][gridSize - 1] + 2 * board[y][0] + 4 * board[y + 1][x] + 8 * board[y + 1][0]

        wynik = int(tab[count])

        UL = int(tablicaliczbowa[wynik][3])
        UR = int(tablicaliczbowa[wynik][2])
        DL = int(tablicaliczbowa[wynik][1])
        DR = int(tablicaliczbowa[wynik][0])

        boards[y][gridSize - 1] = UL
        boards[y][0] = UR
        boards[y + 1][x] = DL
        boards[y + 1][0] = DR


    if y == gridSize - 1 and x < gridSize - 1:
        count = 1 * board[y][x] + 2 * board[y][x + 1] + 4 * board[0][x] + 8 * board[0][x + 1]

        wynik = int(tab[count])

        UL = int(tablicaliczbowa[wynik][3])
        UR = int(tablicaliczbowa[wynik][2])
        DL = int(tablicaliczbowa[wynik][1])
        DR = int(tablicaliczbowa[wynik][0])

        boards[y][x] = UL
        boards[y][x + 1] = UR
        boards[0][x] = DL
        boards[0][x + 1] = DR


    if y == gridSize - 1 and x == gridSize - 1:

        count = board[y][x] + + 2 * board[gridSize - 1][0] + 4 * board[0][gridSize - 1] + 8 * board[0][0]

        wynik = int(tab[count])

        UL = int(tablicaliczbowa[wynik][3])
        UR = int(tablicaliczbowa[wynik][2])
        DL = int(tablicaliczbowa[wynik][1])
        DR = int(tablicaliczbowa[wynik][0])

        boards[y][x] = UL
        boards[gridSize - 1][0] = UR
        boards[0][gridSize - 1] = DL
        boards[0][0] = DR

    return board

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



                return board

#Funkcja obliczająca zmiany dla siatki 2x2 bez przesunięcia
def processBoard(tab):
        global board
        for y in range(0,int(len(board)),2):
            for x in range(0,int(len(board[y])),2):
                transform2(x,y,board,tab)
                # for i in range(0, len(tablicatestowa), 2):
                #     #definicja zasad według których działa funkcja transform
                #     if nc == tablicatestowa[i]:
                #             test = tablicatestowa[i+1]
                #             transform(test, x, y, board)

        return board
#Funkcja obliczająca zmiany dla siatki 2x2 z przesunięciem o 1 piksel w każdym wymiarze
def processBoard2(tab):
        global board
        for y in range(1,int(len(board)),2):
            for x in range(1,int(len(board[y])),2):
                transform2(x, y, board,tab)
                # for i in range(0, len(tablicatestowa), 2):
                #     #definicja zasad według których działa funkcja transform
                #     if nc == tablicatestowa[i]:
                #         test = tablicatestowa[i + 1]
                #         transform(test, x, y, board)

        return board



#Funkcja rysująca komórki na podstawie wartości x,y
def drawCells():
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                fillCellBlack(x, y)


#Przykładowy wzór do wykorzystania w ramach testów
pattern = [
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1],
]
pattern2 = [
[1]
]
#Funkcja generująca losowe wzory
def drawrandompatern(size):
    tab= np.random.randint(2,size=(size, size))
    return tab
def drawblack(size):
    tab=[]
    for y in range(size):
        row = []
        for x in range(size):
            row.append(1)
        tab.append(row)
    return tab

#inicjalizacja tablicy
initBoard()
#Umieszczenie wzoru w tablicy
placePattern(drawrandompatern(15), 70, 70)
#placePattern(drawblack(1),75,75)
placePattern(pattern2,0,0)
#Pobranie aktualnego czasu
prevTime = datetime.now()
even=True
clock = pygame.time.Clock()
tab = randomrules(14)
tab[0]=0
tab[7]=5
tab[15]=15
print(tab)
#Pętla zapewniająca ciągłość pracy programu
while 1:
    #pobranie drugiej próbki czasu
    #Funkcja wypełniająca ekran
    screen.fill(white)
    #Na podstawie zmiany w pobranych próbkach czasu wykonywana jest procedura
    #odświeżenia tablicy z naniesieniem zmian
    if(even):
        processBoard(tab)
    else:
        processBoard2(tab)
    even=not even
    #Opcja narysowania linii siatki w zależnosci od przyjętego wcześniej parametru
    if drawGridLines:
        drawGrid()
    #Narysowanie tablicy
    drawCells()
    #Wyświetlenie zmian
    pygame.display.flip()
    clock.tick()
    fps=0
    if fps<clock.get_fps():
        fps=clock.get_fps()
    #Możliwość zamknięcia programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print(fps)
            exit()
