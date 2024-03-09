import pygame
import sys
import random
from pygame.locals import *

# Tabuleiro do jogo da velha
JOGO = [' '] * 10

# Possíveis padrões de vitória
PADROES_VENCE = [[7, 8, 9], [4, 5, 6], [1, 2, 3],
                 [7, 4, 1], [8, 5, 2], [9, 6, 3],
                 [7, 5, 3], [9, 5, 1]]

# Constantes para cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Espessura da linha e espaçamento do tabuleiro
ESPESSURA = 5
ESPACO_O = [0, (10, 290, 110, 110),
            (145, 290, 110, 110),
            (290, 290, 110, 110),
            (10, 145, 110, 110),
            (145, 145, 110, 110),
            (290, 145, 110, 110),
            (10, 10, 110, 110),
            (145, 10, 110, 110),
            (290, 10, 110, 110)]

ESPACO_X = [0,
            [[(10, 290), (110, 390)], [(10, 390), (110, 290)]],
            [[(145, 290), (245, 390)], [(145, 390), (245, 290)]],
            [[(290, 290), (390, 390)], [(290, 390), (390, 290)]],
            [[(10, 145), (110, 245)], [(10, 245), (110, 145)]],
            [[(145, 145), (245, 245)], [(145, 245), (245, 145)]],
            [[(290, 145), (390, 245)], [(290, 245), (390, 145)]],
            [[(10, 10), (110, 110)], [(10, 110), (110, 10)]],
            [[(145, 10), (245, 110)], [(145, 110), (245, 10)]],
            [[(290, 10), (390, 110)], [(290, 110), (390, 10)]]]

# Inicialização do pygame
pygame.init()

JANELA = pygame.display.set_mode((400, 430))  # Cria uma janela de exibição com tamanho 400x430 pixels
pygame.display.set_caption('Jogo da Velha')  # Define o título da janela
JANELA.fill(BRANCO)  # Preenche a janela com a cor branca

# Variáveis do placar
PLACAR_X = 0
PLACAR_O = 0
EMPATES = 0
FONT_PLACAR = pygame.font.Font(None, 30)

def desenhar_tabuleiro():
    # Desenha as linhas do tabuleiro
    pygame.draw.line(JANELA, PRETO, (133, 10), (133, 390), ESPESSURA)
    pygame.draw.line(JANELA, PRETO, (266, 10), (266, 390), ESPESSURA)
    pygame.draw.line(JANELA, PRETO, (10, 133), (390, 133), ESPESSURA)
    pygame.draw.line(JANELA, PRETO, (10, 266), (390, 266), ESPESSURA)

    # Desenha as marcações no tabuleiro
    for posicao in range(1, 10):
        if JOGO[posicao] == 'O':
            pygame.draw.ellipse(JANELA, AZUL, ESPACO_O[posicao])
        elif JOGO[posicao] == 'X':
            pygame.draw.line(JANELA, VERMELHO, ESPACO_X[posicao][0][0], ESPACO_X[posicao][0][1], ESPESSURA)
            pygame.draw.line(JANELA, VERMELHO, ESPACO_X[posicao][1][0], ESPACO_X[posicao][1][1], ESPESSURA)


def verificar_vitoria(jogador):
    # Verifica se o jogador atual venceu
    for padrao in PADROES_VENCE:
        if JOGO[padrao[0]] == JOGO[padrao[1]] == JOGO[padrao[2]] == jogador:
            return True, padrao
    return False, None


def marcar_posicao(posicao, jogador):
    # Marca a posição escolhida pelo jogador no tabuleiro
    JOGO[posicao] = jogador


def reiniciar_jogo():
    # Reinicia o jogo
    for i in range(1, 10):
        JOGO[i] = ' '


def atualizar_placar():
    # Atualiza o placar na tela
    placar_texto = FONT_PLACAR.render(f'X: {PLACAR_X}   O: {PLACAR_O}   Empates: {EMPATES}', True, PRETO)
    JANELA.blit(placar_texto, (10, 400))


def jogada_maquina():
    # Faz uma jogada aleatória para a máquina
    disponiveis = [i for i in range(1, 10) if JOGO[i] == ' ']
    if disponiveis:
        return random.choice(disponiveis)
    else:
        return None


def main():
    global PLACAR_X, PLACAR_O, EMPATES

    desenhar_tabuleiro()
    jogador = 'X'
    fim_jogo = False
    mensagem = ''

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if not fim_jogo:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Obtém a posição do mouse no momento do clique
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Verifica se o clique foi feito dentro de uma das áreas do tabuleiro
                    for posicao in range(1, 10):
                        if ESPACO_O[posicao][0] < mouse_x < ESPACO_O[posicao][0] + ESPACO_O[posicao][2] and \
                                ESPACO_O[posicao][1] < mouse_y < ESPACO_O[posicao][1] + ESPACO_O[posicao][3]:
                            # Verifica se a posição já está marcada
                            if JOGO[posicao] == ' ':
                                marcar_posicao(posicao, jogador)

                                # Verifica se o jogador venceu
                                venceu, linha_vencedora = verificar_vitoria(jogador)
                                if venceu:
                                    mensagem = 'Jogador {} venceu!'.format(jogador)
                                    fim_jogo = True
                                    if jogador == 'X':
                                        PLACAR_X += 1
                                    else:
                                        PLACAR_O += 1
                                    # Desenha um traço sobre a linha vencedora
                                    pygame.draw.line(JANELA, PRETO, ESPACO_X[linha_vencedora[0]][0][0],
                                                     ESPACO_X[linha_vencedora[2]][1][1], ESPESSURA * 2)
                                else:
                                    # Alterna o jogador
                                    jogador = 'O' if jogador == 'X' else 'X'
                    # Se não houver vencedor, é a vez da máquina jogar
                    if not fim_jogo and jogador == 'O':
                        posicao = jogada_maquina()
                        if posicao:
                            marcar_posicao(posicao, jogador)
                            venceu, linha_vencedora = verificar_vitoria(jogador)
                            if venceu:
                                mensagem = 'Jogador {} venceu!'.format(jogador)
                                fim_jogo = True
                                PLACAR_O += 1
                                # Desenha um traço sobre a linha vencedora
                                pygame.draw.line(JANELA, PRETO, ESPACO_X[linha_vencedora[0]][0][0],
                                                 ESPACO_X[linha_vencedora[2]][1][1], ESPESSURA * 2)
                            else:
                                jogador = 'X'
                                if ' ' not in JOGO[1:]:
                                    mensagem = 'Empate!'
                                    fim_jogo = True
                                    EMPATES += 1

            else:
                # Reinicia o jogo após um intervalo de tempo
                pygame.time.wait(500)
                reiniciar_jogo()
                fim_jogo = False
                mensagem = ''

        # Limpa a área do placar
        pygame.draw.rect(JANELA, BRANCO, (0, 400, 400, 30))
        # Atualiza o placar na tela
        atualizar_placar()
        # Atualiza a exibição do tabuleiro
        desenhar_tabuleiro()

        # Exibe a mensagem de vitória ou empate
        if mensagem:
            fonte = pygame.font.Font(None, 25)
            texto = fonte.render(mensagem, 1, PRETO)
            JANELA.blit(texto, (10, 405))

        # Atualiza a tela
        pygame.display.update()


if __name__ == '__main__':
    main()