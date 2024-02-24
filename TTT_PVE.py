import pygame
import sys
import TTT_setup as setup
from TTT_PVP import click
import random
from time import sleep as wait

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

'''
Algoritimo para não perder no jogo da velha:
Jogar seguindo as regras abaixo em ordem.
1- Se alguma linha possui 1 casa livre e as outras 2 ocupadas por
    você, marque a casa livre
2- Se alguma linha possui 1 casa livre e as outras 2 ocupadas pelo
    oponente, marque a casa livre
3- Se o meio estiver livre, marque ele
4- Se alguma diagonal possui uma quina ocupada pelo oponente e a
    outra livre, marque a quina livre
5- Se o oponente possui 2 quinas opostas, marque uma borda, se
    houver uma disponivel
6- Se o oponente possui duas bordas adjascentes a uma quina livre,
    marque essa quina
A primeira jogada pode ser livre entre quinas e o meio, não pode ser
uma borda
'''


def randomMove(game): #retorna uma posição disponivel aleatória
    free = []
    for i in range(3):
        for j in range(3):
            if game[i][j] == 'E':
                free.append([i, j])
    if len(free) == 0:
        return [3, 3]
    return random.choice(free)

    return

def bestPlay(game, p, op): #define a jogada para não ir a uma posição perdedora
    #p = player; op = opponent;
    #para a implementação de varias das condições a baixo será usada a função
    #-x+2, pois transforma 0 em 2, 2 em 0 e 1 em 1, sendo util para chegar na
    #casa oposta à referenciada
    
    #Se o tabuleiro estiver vazio, ele retornará uma jogada aleatória
    allE = True #bool que verificara se todas as posições estão com 'E'
    for line in game:
        for pos in line:
            allE = allE and (pos == 'E')
    if allE:
        fakeGame = [['E', 'O', 'E'],
                    ['O', 'E', 'O'],
                    ['E', 'O', 'E']]
        #jogo feito para gerar uma jogada aleatória que não é uma borda
        return randomMove(fakeGame)

    #listas uteis:
    quinas = [[0, 0], [0, 2], [2, 0], [2, 2]]
    bordas = [[0, 1], [2, 1], [1, 0], [1, 2]]

    #condições 1 e 2 são iguais, mudando apenas o jogador.
    for player in [p, op]:
        #condições 1 e 2 para o meio
        if (((player == game[0][1] == game[2][1]) or
            (player == game[1][0] == game[1][2]) or
            (player == game[0][0] == game[2][2]) or
            (player == game[0][2] == game[2][0])) and
            (game[1][1] == 'E')):
            return [1, 1]
        #condições 1 e 2 para as quinas:
        for i in quinas:
            if (((player == game[i[0]][(i[1]+1)%3] == game[i[0]][(i[1]+2)%3]) or
                (player == game[(i[0]+1)%3][i[1]] == game[(i[0]+2)%3][i[1]]) or
                (player == game[1][1] == game[-i[0]+2][-i[1]+2])) and
                (game[i[0]][i[1]] == 'E')):
                    return i
        #condições 1 e 2 para as bordas:
        for i in bordas:
            #as funções x^2-x e -x^2+3x serão usadas pq ambas
            #mantem 0 como 0 e 2 como 2 mas transformam 1 em
            #0 e 2, respectivamente
            if (((player == game[1][1] == game[-i[0]+2][-i[1]+2]) or
                player == game[i[0]**2-i[0]][-i[1]**2+3*i[1]] == game[-i[0]**2+3*i[0]][i[1]**2-i[1]]) and
                (game[i[0]][i[1]] == 'E')):
                    return i
    #condição 3:
    if game[1][1] == 'E':
        return [1, 1]
    #condição 4:
    for i in quinas:
        if ((game[i[0]][i[1]] == op) and
            (game[-i[0]+2][-i[1]+2] == 'E')):
            return [-i[0]+2, -i[1]+2]
    #condição 5:
    if ((game[0][0] == game[2][2] == op) or
        (game[2][0] == game[0][2] == op)):
        #verifica se tem bordas disponiveis:
        for i in bordas:
            if game[i[0]][i[1]] == 'E':
                return [i[0], i[1]]
    #condição 6:
    for i in quinas:
        if ((game[i[0]][i[1]] == 'E') and
            (game[i[0]][1] == game[1][i[1]] == op)):
            return [i[0], i[1]]
    #jogada livre:
    return randomMove(game)

def engineMove(game, p, op, level): #define o movimento a ser jogado
    if level == 1: #nivel facil
        #movimentos aleatórios
        return randomMove(game)
    if level == 2: #nivel médio
        #70% de chance do melhor movimento
        #30% de chance de um movimento aleatório
        r = random.random()
        if r>.7:
            return randomMove(game)
        return bestPlay(game, p, op)
    if level == 3: #nivel dificil
        #90% de chance do melhor movimento
        #10% de chance de um movimento aleatório
        r = random.random()
        if r>.9:
            return randomMove(game)
        return bestPlay(game, p, op)
    if level == 4: #nivel impossível
        #melhor movimento sempre
        return bestPlay(game, p, op)
    #se o nivel não está registrado
    raise ValueError('este nivel nao existe')


def PVE(screen, p1 = 'X', p2 = 'O', level = 4):

    player = p1 #quem faz a jogada
    clock = pygame.time.Clock()

    game = [['E', 'E', 'E'],
            ['E', 'E', 'E'],
            ['E', 'E', 'E']]

    # tamanho do jogo da velha
    x, y = 700, 700
    #achando a posição inicial do grid para ficar centralizado na tela
    sWidth, sHeigth = screen.get_size()
    x_0 = (sWidth-x)/2
    y_0 = (sHeigth-x)/2
    
    #loop principal
    running = True
    
    win = 'E'
    
    while running:
        
        if win[0] != 'E':
            wait(2)
            return win[0]
        
        if player == 'X': #se for vez da engine
            
            move = engineMove(game, 'X', 'O', level)
            game[move[0]][move[1]] = 'X'
            wait(1)
            player = 'O'
            
        
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) and (player == 'O'):
                    mx, my = pygame.mouse.get_pos()
                    #se ocorrer uma jogada, o jogador será trocado
                    if click(mx, my, player, x_0, y_0, x, y, game):
                        if player == p1:
                            player = p2
                        elif player == p2:
                            player = p1

        screen.fill(black)
        setup.drawGame(x_0, y_0, x, y, game, screen, OWidth = 3)
        
        win = setup.checkWinner(game)
        setup.drawWinLine(win, x_0, y_0, x, y, screen)

        pygame.display.flip()

        clock.tick(60)



#definindo dificuldades
def easy(screen, p1 = 'X', p2 = 'O'):
    return PVE(screen, p1, p2, 1)
def medium(screen, p1 = 'X', p2 = 'O'):
    return PVE(screen, p1, p2, 2)
def hard(screen, p1 = 'X', p2 = 'O'):
    return PVE(screen, p1, p2, 3)
def impossible(screen, p1 = 'X', p2 = 'O'):
    return PVE(screen, p1, p2, 4)

    

if __name__ == '__main__':
       
    pygame.init()
    #criando a tela
    screenWidth, screenHeigth = 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Tic Tac Toe")    
    print(PVE(screen, 'O', 'X', 3))
    pygame.quit()
    sys.exit()
    '''
    game = [['O', 'E', 'X'],
            ['E', 'O', 'E'],
            ['X', 'O', 'X']]
    
    print(bestPlay(game, 'X', 'O'))
    '''
