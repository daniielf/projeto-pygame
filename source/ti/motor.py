# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável por toda interação dos atores no jogo.
"""
import copy
import media
import pygame
import random
import settings
from atores import *
from pygame.locals import *

class Game:
    screen      = None
    screen_size = None
    run         = True
    intervalo   = 0
    lista       = None
    jogador     = None
    background  = None 
    
    def __init__( self, screen ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        atores = {}
        self.screen      = screen
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Pygame' )
        self.carrega_dados()

    def carrega_dados( self ):
        """
        Lê as imagens e sons necessarios pelo jogo.
        """
        # imagens
        self.imagem_jogador      = pygame.image.load( media.carrega_imagem(settings.IMG_BOB_JOGADOR) )
        self.imagem_fase_1       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_1) )
    

    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        jogador = self.jogador

        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_UP:
                    jogador.accel_top()
                elif k == K_DOWN:
                    jogador.accel_bottom()
                elif k == K_RIGHT:
                    jogador.accel_right()
                elif k == K_LEFT:
                    jogador.accel_left()
        
            elif t == KEYUP:
                if   k == K_DOWN:
                    jogador.accel_top()
                elif k == K_UP:
                    jogador.accel_bottom()
                elif k == K_LEFT:
                    jogador.accel_right()
                elif k == K_RIGHT:
                    jogador.accel_left()
        
            keys = pygame.key.get_pressed()     

      def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background( self.imagem_fase_1 )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock          = pygame.time.Clock()
        dt             = 16
        self.ticks     = 0
        self.intervalo = 1

        posicao      = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.jogador = Jogador( posicao = posicao, imagem = self.imagem_jogador )

        self.lista = {
            "jogador"       : pygame.sprite.RenderPlain( self.jogador ),
            }

        # Loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )
            self.intervalo += 1

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.atores_update( dt )

            # Faça os atores atuarem
            self.atores_act()
            
            # Desenhe os elementos do jogo.
            #self.atores_draw()
            
            # Por fim atualize o screen do jogo.
            pygame.display.flip()