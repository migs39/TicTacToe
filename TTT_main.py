import pygame
import sys
import TTT_setup as setup
import TTT_PVP as PVP
import TTT_PVE as PVE
import TTT_menus as menus

def gameSeries(n, gamemode, screen): #melhor de N naquele modo de jogo
    if n == 0:
        return 'Draw'
    X_points, O_points = 0, 0
    p1, p2 = 'X', 'O'
    gamesPlayed = 0
    while True:
        winner = gamemode(screen, p1, p2)
        if winner == 'X':
            X_points += 1
        if winner == 'O':
            O_points +=1
        p1, p2 = p2, p1 #troca o primeiro jogador
        print('X: ' + str(X_points))
        print('O: ' + str(O_points))
        gamesPlayed+=1
        gamesLeft = n - gamesPlayed
        if X_points > O_points + gamesLeft:
            return 'X'
        if O_points > X_points + gamesLeft:
            return 'O'
        if gamesLeft == 0:
            return 'V'



if __name__ == '__main__':

    pygame.init()
    #criando a tela
    screenWidth, screenHeigth = 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Tic Tac Toe")
    
    game = menus.selectGameMode(screen)
    n = menus.selectNumOfMatches(screen)
    if game == 'PVE':
        game = menus.selectDifficulty(screen)
    winner = gameSeries(n, game, screen)
    if winner == 'V':
        print('Draw')
    else:
        print('Winner: ' + winner)
    pygame.quit()
    sys.exit()
