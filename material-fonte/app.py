# -*- coding: utf-8 -*-
# @author: Humberto Cassio Nagato Fonseca
# @contact: humberto.nagatog@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável definir as configurações e iniciar o jogo.
"""
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.setcaption(Game)
    screen = pygame.display.set_mode((640,480))
    menu.Menu(screen)