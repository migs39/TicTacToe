import pygame
import sys
from math import pi
from math import floor


'''gameSample:
    game = [['O', 'E', 'E'],
            ['X', 'X', 'E'],
            ['E', 'E', 'O']]
    #E = Empty
    #X = X
    #O = O
'''


black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

def drawGrid(x_0, y_0, x, y, screen, color = white, width=5):

    '''
    as linhas começam cruzam todo o tamanho do grid (x_0 até x_0+x pras linhas horizontais
    ou y_0 até y_0+x pras linhas verticais) e acontecem sempre no primeiro e no segundo
    terço da tela (y_0+y/3 e y_0+2*y/3 pras linhas horizontais ou x_0+x/3 e x_0+2*x/3 pras
    linhas verticais)
    '''
    pygame.draw.line(screen, color, (x_0, y_0+y/3), (x_0+x, y_0+y/3), width) #primeira linha horizontal
    pygame.draw.line(screen, color, (x_0, y_0+2*y/3), (x_0+x, y_0+2*y/3), width) #segunda linha horizontal
    pygame.draw.line(screen, color, (x_0+x/3, y_0), (x_0+x/3, y_0+y), width) #primeira linha vertical
    pygame.draw.line(screen, color, (x_0+2*x/3, y_0), (x_0+2*x/3, y_0+y), width) #segunda linha vertical
    
def drawX(x_0, y_0, x, y, screen, color = white, width = 5):
    #o X possui linhas conectando os cantos opostos da area definida
    #os cantos sao (x_0, y_0), (x_0+x, y_0), (x_0, y_0+y) e (x_0+x, y_0+y)
    pygame.draw.line(screen, color, (x_0, y_0), (x_0+x, y_0+y), width)
    pygame.draw.line(screen, color, (x_0+x, y_0), (x_0, y_0+y), width)
    
def drawO(x_0, y_0, x, y, screen, color = white, width = 5):
    rect = (x_0, y_0, x, y) #retangulo em que a bola é centrada
    pygame.draw.arc(screen, color, rect, 0, 2*pi, width)


def drawGame(x_0, y_0, x, y, game, screen, fill = .8, OColor = blue, XColor = red, gridColor = white,
             XWidth = 5, OWidth = 5, gridWidth = 5):
    #fill é o quanto do espaço da jogada será preenchido pela jogada
    #OColor é a cor do O
    #XColor é a cor do X
    #gridColor é a cor do tabuleiro
    #game é a matriz das posições ocupadas
    
    full_rect_x = x//3 #largura do espaço para jogada
    rect_x = floor(fill*full_rect_x) #largura do espaço que a jogada usará
    full_rect_y = y//3 #altura do espaço para jogada
    rect_y = floor(fill*full_rect_y) #altura do espaço que a jogada usará

    jump_x = (full_rect_x - rect_x)/2 #espaço em x que deve ser pulado para centralizar a jogada
    jump_y = (full_rect_y - rect_y)/2 #espaço em y que deve ser pulado para centralizar a jogada
    
    #valores de x_0 para as jogadas em cada coluna do tabuleiro:
    X_0 = [(x_0 + jump_x), x_0 + full_rect_x + jump_x, x_0 + 2*full_rect_x + jump_x]
    #valores de y_0 para as jogadas em cada linha do tabuleiro:
    Y_0 = [(y_0 + jump_y), y_0 + full_rect_y + jump_y, y_0 + 2*full_rect_y + jump_y]

    #desenha o tabuleiro
    drawGrid(x_0, y_0, x, y, screen, gridColor, gridWidth)

    #itera entre as posições para desenhar X ou O se necessário
    for line in range(3):
        for column in range(3):
            if game[line][column] == 'E':
                continue
            elif game[line][column] == 'X':
                drawX(X_0[column], Y_0[line], rect_x, rect_y, screen, XColor, XWidth)
            elif game[line][column] == 'O':
                drawO(X_0[column], Y_0[line], rect_x, rect_y, screen, OColor, OWidth)
            else:
                raise ValueError("Jodaga Invalida")

            
def checkWinner(game):
    winner = 'E'
    winPos = '' #diz em que linha, coluna ou diagonal foi encontrada uma sequencia vencedora
    for p in ['X', 'O']:
        #checando linhas
        for line in range(3):
            if all(x == p for x in game[line]): #se todas as jogadas na linha forem iguais a p
                winner = p
                winPos = 'line ' + str(line)
        #checando colunas:
        for column in range(3):
            if game[0][column] == game[1][column] == game[2][column] == p:
                winner = p
                winPos = 'column ' + str(column)
        #checando diagonal 1
        if game[0][0] == game[1][1] == game[2][2] == p:
            winner = p
            winPos = 'diagonal 1'
        #checando diagonal 2
        if game[2][0] == game[1][1] == game[0][2] == p:
            winner = p
            winPos = 'diagonal 2'
        if winner == 'E': #se n tiver achado um vencedor
            velha = True
            #verifica se ainda existe alguma posição vazia
            for line in game:
                for pos in line:
                    velha = velha and (pos != 'E')
            if velha:
                winner = 'V'
    return [winner, winPos]


def drawWinLine(win, x_0, y_0, x, y, screen, color = white, width = 5):
    if win[0] == 'E' or win[0] == 'V':
        return True
    winPos = win[1]
    if winPos == 'diagonal 1':
        pygame.draw.line(screen, color, (x_0, y_0), (x_0+x, y_0+y), width)
        return True
    if winPos == 'diagonal 2':
        pygame.draw.line(screen, color, (x_0+x, y_0), (x_0, y_0+y), width)
        return True
    
    idx = int(winPos[-1]) #indice da linha ou coluna vencedora
    if winPos[:4] == 'line':
        lPos = y_0 + y/6 #posição vertical da linha se a vitória for na primeira linha
        lPos = lPos + (y/3)*idx #ajusta a posição para a linha vencedora
        pygame.draw.line(screen, color, (x_0, lPos), (x_0+x, lPos), width)
        return True
    if winPos[:6] == 'column':
        lPos = x_0 + x/6 #posição horizontal da linha se a vitória for na primeira coluna
        lPos = lPos + (x/3)*idx #ajusta a posição para a coluna vencedora
        pygame.draw.line(screen, color, (lPos, y_0), (lPos, y_0+y), width)
        return True
    raise ValueError('vetor de vitoria invalido')

    

def test():
    
    pygame.init()

    #criando a tela
    screenWidth, screenHeigth = 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Tic Tac Toe")

    clock = pygame.time.Clock()

    #loop principal
    running = True
    
    game = [['X', 'O', 'X'],
            ['O', 'O', 'X'],
            ['X', 'X', 'O']]
    while running:


        # tamanho do jogo da velha
        x = 700
        y = 700
        #achando a posição inicial do grid para ficar centralizado na tela
        sWidth, sHeigth = screen.get_size()
        x_0 = (sWidth-x)/2
        y_0 = (sHeigth-x)/2
        
        screen.fill(black)
        drawGame(x_0, y_0, x, y, game, screen, OWidth = 3)
        win = checkWinner(game)
        drawWinLine(win, x_0, y_0, x, y, screen)
        pygame.display.flip()
        print(win[0])
        #adiciona o evento quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        clock.tick(60)


                
    #finalizando
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    test()
