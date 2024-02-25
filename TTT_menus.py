import pygame
import sys
import TTT_PVP as PVP
import TTT_PVE as PVE

black = (0, 0, 0)
white = (255, 255, 255)


def selectGameMode(screen, c1 = black, c2 = white):
    
    #Obtendo o comprimento e altura da tela:
    x, y = pygame.display.get_surface().get_size()
    
    #definindo as fontes:
    fontSize = x//15 #tamanho padrao de fonte
    fontDefault = pygame.font.Font(None, fontSize)
    fontTitle = pygame.font.Font(None, 2*fontSize)
    fontMini = pygame.font.Font(None, fontSize//2)
    
    #definindo textos da tela:
    title = fontTitle.render('Jogo da Velha', True, c2)
    gamemode = fontDefault.render('Escolha o modo de jogo:', True, c2)
    PvP = fontDefault.render('PVP', True, c2)
    PvE = fontDefault.render('PVE', True, c2)
    ML = fontDefault.render('Em breve...', True, c2)
    #DM = fontMini.render('Dark/Light Mode', True, c2)

    #Obtendo os retângulos dos textos:
    title_rect = title.get_rect()
    gamemode_rect = gamemode.get_rect()
    PvP_rect = PvP.get_rect()
    PvE_rect = PvE.get_rect()
    ML_rect = ML.get_rect()
    #DM_rect = DM.get_rect()
    
    #definindo a posição de cada texto na tela:
    title_rect.center = (x//2, y//4)
    gamemode_rect.center = (x//2, 5*y//8)
    PvP_rect.center = (x//4, 3*y//4)
    PvE_rect.center = (2*x//4, 3*y//4)
    ML_rect.center = (3*x//4, 3*y//4)
    #DM sera definido depois de criar o botão

    #criando os botões:
    PvP_button = PvP_rect.inflate(x//20, y//20)
    PvP_button.center = PvP_rect.center
    PvE_button = PvE_rect.inflate(x//20, y//20)
    PvE_button.center = PvE_rect.center
    ML_button = ML_rect.inflate(x//20, y//20)
    ML_button.center = ML_rect.center

    #DM_button = DM_rect.inflate(x//30, y//30)
    #DM_button.bottomright = (x, y)
    #DM_rect.center = DM_button.center
    
    buttons = [PvP_button, PvE_button, ML_button]#, DM_button]


    # Loop principal
    running = True
    mx, my = 0, 0
    while running:
        
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    #conferindo se o click foi em algum botão
                    for button in buttons:
                        if ((button.left < mx < button.right) and
                        (button.top < my < button.bottom)):
                            #retorna o nome do botão atual
                            if button == PvP_button:
                                return PVP.PVP
                            if button == PvE_button:
                                return 'PVE'
                            #if button == DM_button:
                                #return 'Dark Mode'
                            if button == ML_button:
                                #return ML
                                break
                        

        # Preenchendo a tela com a cor de fundo
        screen.fill(c1)
        
        # Blitando os textos na tela
        screen.blit(title, title_rect)
        screen.blit(gamemode, gamemode_rect)
        screen.blit(PvP, PvP_rect)
        screen.blit(PvE, PvE_rect)
        screen.blit(ML, ML_rect)
        #screen.blit(DM, DM_rect)

        # Atualizando a tela
        pygame.display.flip()

def selectNumOfMatches(screen, c1 = 'black', c2 = 'white'):

    n = 1
    #Obtendo o comprimento e altura da tela:
    x, y = pygame.display.get_surface().get_size()
    
    #definindo a fonte:
    fontSize = x//15 #tamanho padrao de fonte
    fontDefault = pygame.font.Font(None, fontSize)  
    fontNumber = pygame.font.Font(None, 2*fontSize)
    fontArrow = pygame.font.Font(None, 2*fontSize)

    #definindo textos da tela:
    txt = fontDefault.render('Selecione o número de rodadas', True, c2)
    jogar = fontDefault.render('jogar', True, c2)
    number = fontNumber.render(str(n), True, c2)
    arrowU = fontArrow.render('^', True, c2)
    arrowD = pygame.transform.rotate(arrowU, 180)
    
    #Obtendo os retângulos dos textos:
    txt_rect = txt.get_rect()
    jogar_rect = jogar.get_rect()
    number_rect = number.get_rect()
    arrowU_rect = arrowU.get_rect()
    arrowD_rect = arrowD.get_rect()

    #definindo a posição de cada texto na tela:
    txt_rect.center = (x//2, y//2)
    jogar_rect.center = (x//2, 5*y//6)
    number_rect.center = (9*x//20, 4*y//6)
    arrowU_rect.center = (11*x//20, 38*y//60)
    arrowD_rect.center = (11*x//20, 42*y//60)

    #criando os botões:
    jogar_button = jogar_rect.inflate(x//20, y//20)
    jogar_button.center = jogar_rect.center
    arrowU_button = arrowU_rect.inflate(x//30, y//30)
    arrowU_button.center = arrowU_rect.center
    arrowD_button = arrowD_rect.inflate(x//30, y//30)
    arrowD_button.center = arrowD_rect.center

    buttons = [jogar_button, arrowU_button, arrowD_button]


    # Loop principal
    running = True
    mx, my = 0, 0
    while running:
        
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    #conferindo se o click foi em algum botão
                    for button in buttons:
                        if ((button.left < mx < button.right) and
                        (button.top < my < button.bottom)):
                            #retorna o nome do botão atual
                            if button == jogar_button:
                                return n
                            if button == arrowU_button:
                                if n<10:
                                    n+=1
                                    number = fontNumber.render(str(n), True, c2)
                            if button == arrowD_button:
                                if n>1:
                                    n-=1
                                    number = fontNumber.render(str(n), True, c2)
                        

        # Preenchendo a tela com a cor de fundo
        screen.fill(c1)
        
        # Blitando os textos na tela
        screen.blit(txt, txt_rect)
        screen.blit(jogar, jogar_rect)
        screen.blit(arrowU, arrowU_rect)
        screen.blit(arrowD, arrowD_rect)
        screen.blit(number, number_rect)
        
        # Atualizando a tela
        pygame.display.flip()


def selectDifficulty(screen, c1 = 'black', c2 = 'white'):

    #Obtendo o comprimento e altura da tela:
    x, y = pygame.display.get_surface().get_size()
    
    #definindo as fontes:
    fontSize = x//15 #tamanho padrao de fonte
    fontDefault = pygame.font.Font(None, fontSize)
    fontTitle = pygame.font.Font(None, 2*fontSize)

    #definindo textos da tela:
    title = fontTitle.render('Escolha a dificuldade', True, c2)
    easy = fontDefault.render('Facil', True, (0, 255, 255))
    med = fontDefault.render('Medio', True, (0, 255, 0))
    hard = fontDefault.render('Dificil', True, (255, 255, 0))
    imp = fontDefault.render('Impossivel', True, (255, 0, 0))
    ML = fontDefault.render('Em Breve...', True, (0, 0, 255))

    #Obtendo os retângulos dos textos:
    title_rect = title.get_rect()
    easy_rect = easy.get_rect()
    med_rect = med.get_rect()
    hard_rect = hard.get_rect()
    imp_rect = imp.get_rect()
    ML_rect = ML.get_rect()
    
    #definindo a posição de cada texto na tela:
    title_rect.center = (x//2, y//4)
    easy_rect.center = (x//4, 4*y//6)
    med_rect.center = (x//2, 4*y//6)
    hard_rect.center = (3*x//4, 4*y//6)
    imp_rect.center = (x//2, 5*y//6)
    ML_rect.center = (x//2, y//2)

    #criando os botões:
    easy_button = easy_rect.inflate(x//20, y//20)
    easy_button.center = easy_rect.center
    med_button = med_rect.inflate(x//20, y//20)
    med_button.center = med_rect.center
    hard_button = hard_rect.inflate(x//20, y//20)
    hard_button.center = hard_rect.center
    imp_button = imp_rect.inflate(x//20, y//20)
    imp_button.center = imp_rect.center
    ML_button = ML_rect.inflate(x//20, y//20)
    ML_button.center = ML_rect.center
    
    buttons = [easy_button, med_button, hard_button, imp_button, ML_button]


    # Loop principal
    running = True
    mx, my = 0, 0
    while running:
        
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    #conferindo se o click foi em algum botão
                    for button in buttons:
                        if ((button.left < mx < button.right) and
                        (button.top < my < button.bottom)):
                            #retorna o nome do botão atual
                            if button == easy_button:
                                return PVE.easy
                            if button == med_button:
                                return PVE.medium
                            if button == hard_button:
                                return PVE.hard
                            if button == imp_button:
                                return PVE.impossible
                            if button == ML_button:
                                #return ML.PVE
                                break
                        
        # Preenchendo a tela com a cor de fundo
        screen.fill(c1)
        
        # Blitando os textos na tela
        screen.blit(easy, easy_rect)
        screen.blit(med, med_rect)
        screen.blit(hard, hard_rect)
        screen.blit(imp, imp_rect)
        screen.blit(ML, ML_rect)
        screen.blit(title, title_rect)

        # Atualizando a tela
        pygame.display.flip()


    

if __name__ == '__main__':
    
    pygame.init()
    #criando a tela
    screenWidth, screenHeigth = 800, 800
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Tic Tac Toe")

    print(selectDifficulty(screen))
    
