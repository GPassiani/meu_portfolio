import pygame
import time
import random

pygame.init()


largura = 1280
altura = 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobrinha 🐍")


preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)


tamanho_bloco = 20
velocidade = 5


fonte = pygame.font.SysFont(None, 35)


def mostrar_pontuacao(pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, branco)
    tela.blit(texto, [10, 10])


def jogo():
    fim_de_jogo = False
    game_over = False

    x = largura / 2
    y = altura / 2

    x_mudanca = 0
    y_mudanca = 0

    corpo_cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0

    clock = pygame.time.Clock()

    while not fim_de_jogo:

        while game_over:
            tela.fill(preto)
            msg = fonte.render("Game Over! Pressione Q para sair ou C para jogar novamente", True, vermelho)
            tela.blit(msg, [largura / 6, altura / 3])
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        fim_de_jogo = True
                        game_over = False
                    if evento.key == pygame.K_c:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_de_jogo = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x_mudanca = -tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_RIGHT:
                    x_mudanca = tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_UP:
                    y_mudanca = -tamanho_bloco
                    x_mudanca = 0
                elif evento.key == pygame.K_DOWN:
                    y_mudanca = tamanho_bloco
                    x_mudanca = 0

        x += x_mudanca
        y += y_mudanca

        if x >= largura or x < 0 or y >= altura or y < 0:
            game_over = True

        tela.fill(preto)
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

        cabeca_cobra = []
        cabeca_cobra.append(x)
        cabeca_cobra.append(y)
        corpo_cobra.append(cabeca_cobra)

        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]

       
        for parte in corpo_cobra[:-1]:
            if parte == cabeca_cobra:
                game_over = True

        for parte in corpo_cobra:
            pygame.draw.rect(tela, verde, [parte[0], parte[1], tamanho_bloco, tamanho_bloco])

        mostrar_pontuacao(comprimento_cobra - 1)
        pygame.display.update()

      
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0
            comprimento_cobra += 1

        clock.tick(velocidade)

    pygame.quit()
    quit()


jogo()