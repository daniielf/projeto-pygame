# -*- coding: utf-8 -*-
# @author: Humberto Cassio Nagato Fonseca
# @contact: humberto.nagatog@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável pelos atores do jogo, como background, jogador, inimigos, etc.
"""
import pygame
import settings
from math import ceil
from pygame.locals import *

class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None

    def __init__( self, image ):
        self.isize  = image.get_size()
        self.pos    = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        largura = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * self.isize[ 0 ]
        altura  = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * self.isize[ 1 ]

        back = pygame.Surface( ( largura, altura ) )
        
        for i in range( ( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( ( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back
        
    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]

    def draw( self, screen ):
        screen.blit( self.image, self.pos )



class Bob( GameObject ):
    """
    Esta classe representa o ator "bob" do jogo.
    """

