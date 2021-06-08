import pygame
import numpy as np
from pygame.locals import *
import PySimpleGUI as sg

#Definicja kolorów RGB
white = (255, 255, 255)
black = (0, 0, 0)
#Nazwa okna
pygame.display.set_caption("Automat Komórkowy")
#Flaga podwójnego buforu (zwiększa wydajność)
flags=DOUBLEBUF
#Rozmiar siatki
gridSize = 200 # musi być wielokrotnością 2
(width, height) = (3*gridSize, 3*gridSize)  # Rozmiar okna
resolution=[width,height]#Rozdzielczość na podstawie rozmiarów okna
screen = pygame.display.set_mode(resolution,flags,16)
#Opcja renderowania linii siatki
drawGridLines = False
#Minimalny interwał pomiedzy kolejnymi klatkami
updateTime = 0.1
#Inicjalizacja tablicy
board = []
randompatternsize=50
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
event, values = sg.Window('Wybierz zestaw reguł', [[sg.Text('Wybierz zestaw reguł:'), sg.Listbox(['gaz','losowe'], size=(20, 3), key='Choice')],
[sg.Text('Wybierz rozmiar generowanego wzoru'), sg.Listbox(['10','20','50','100'], size=(20, 3), key='Choice2')],
[sg.Button('Ok'), sg.Button('Domyślny')]]).read(close=True)






#Tablica dostępnych stanów
tablicaliczbowa=[[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]


tablicaregulowa=[]
#Wczytanie pliku z zasadami symulującymi gaz

#Funkcja generująca losowe zasady
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


#Funkcja wypełniająca czarne piksele
def fillCellBlack(x, y):
    pygame.draw.rect(screen, black, (
         x * int(width / gridSize), int(y * (height / gridSize)), int(width / gridSize), int(height / gridSize)))

#Funkcja umieszczająca piksele w odpowiedniej części tablicy zależnej od offsetu
def placePattern(pattern, offset_x, offset_y):
    global board
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            if offset_y + y < len(board) and offset_x + x < len(board[offset_y + y]):
                board[offset_y + y][offset_x + x] = pattern[y][x]


def transform(x,y,boards,tab):

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


#Funkcja obliczająca zmiany dla siatki 2x2 bez przesunięcia
def processBoard(tab):
        global board
        for y in range(0,int(len(board)),2):
            for x in range(0,int(len(board[y])),2):
                transform(x,y,board,tab)


        return board
#Funkcja obliczająca zmiany dla siatki 2x2 z przesunięciem o 1 piksel w każdym wymiarze
def processBoard2(tab):
        global board
        for y in range(1,int(len(board)),2):
            for x in range(1,int(len(board[y])),2):
                transform(x, y, board,tab)


        return board



#Funkcja rysująca komórki na podstawie wartości x,y
def drawCells():
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                fillCellBlack(x, y)





#Funkcja generująca losowe wzory
def drawrandompatern(size):
    tab= np.random.randint(2,size=(size, size))
    return tab

#Funkcja generująca czarne wzory
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
#placePattern(drawblack(50),75,75)
#placePattern(pattern2,0,0)
#Pobranie aktualnego czasu

even=True
clock = pygame.time.Clock()
fps=0

#Pętla zapewniająca ciągłość pracy programu

if event == 'Ok':

    try:
        if (values["Choice"][0] == "losowe"):
            tablicaregulowa=randomrules(14)
            randompatternsize = int(values["Choice2"][0])
            placePattern(drawrandompatern(randompatternsize), 75, 75)
        else:
            sg.popup(f'Wybrano {values["Choice"][0]}')
            filename = "Pliki testowe/" + values["Choice"][0]
            randompatternsize = int(values["Choice2"][0])
            file = open(filename)
            placePattern(drawrandompatern(gridSize), 0, 0)
            placePattern(drawblack(randompatternsize),int((gridSize - randompatternsize) / 2),int((gridSize - randompatternsize) / 2))
            for i in file:
                tablicaregulowa.append(i)
    finally:
        pass
        # file = open(filename)
        # placePattern(drawrandompatern(gridSize), 0, 0)
        # placePattern(drawblack(randompatternsize), (gridSize - randompatternsize) // 2, (gridSize - randompatternsize) // 2)
        # for i in file:
        #     tablicaregulowa.append(i)
else:
    sg.popup('W takim razie uruchomiona zostanie wersja domyślna')
    filename = "Pliki testowe/Gaz"
    randompatternsize = 50
    file = open(filename)
    placePattern(drawrandompatern(gridSize), 0, 0)
    placePattern(drawblack(randompatternsize), int((gridSize - randompatternsize) / 2), int((gridSize - randompatternsize) / 2))
    for i in file:
        tablicaregulowa.append(i)

while 1:

    #Funkcja wypełniająca ekran
    screen.fill(white)
    #odświeżenia tablicy z naniesieniem zmian
    if(even):
        processBoard(tablicaregulowa)
    else:
        processBoard2(tablicaregulowa)
    even=not even
    #Opcja narysowania linii siatki w zależnosci od przyjętego wcześniej parametru
    if drawGridLines:
        drawGrid()
    #Narysowanie tablicy
    drawCells()
    #Wyświetlenie zmian
    pygame.display.flip()
    clock.tick(25)

    if fps<clock.get_fps():
        fps=clock.get_fps()
    #Możliwość zamknięcia programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print(fps)
            exit()
