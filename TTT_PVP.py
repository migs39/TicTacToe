import pygame
import TTT_setup as setup
from time import sleep as wait
import sys

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

def click(mx, my, player, x_0, y_0, x, y, game):
    if (mx <= x_0 or mx > x+x_0 or my <= y_0 or my > y+y_0):
        return False #nao aceitar jogada fora do tabuleiro
    #descobrindo em qual coluna o mouse clicou:
    if mx <= x_0+x/3:
        px = 0
    elif mx <= x_0+2*x/3:
        px = 1
    else:
        px = 2
    #descobrindo em qual linha o mouse clicou:
    if my <= y_0+y/3:
        py = 0
    elif my <= y_0+2*y/3:
        py = 1
    else:
        py = 2

    #analisando se o local está disponível:
    if game[py][px] != 'E':
        return False
    #Realiza a jogada:
    game[py][px] = player
    return True
    
    

def PVP(screen, p1 = 'X', p2 = 'O'):

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


        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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


                
if __name__ == '__main__':
    
    pygame.init()
    #criando a tela
    screenWidth, screenHeigth = 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Tic Tac Toe")    
    print(PVP(screen))
    pygame.quit()
    sys.exit()
