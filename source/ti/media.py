# -*- coding: utf-8 -*-
# @author: Humberto Cassio Nagato Fonseca
# @contact: humberto.nagatog@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

import os
import pygame
from os.path import join as join_path

		
dados_py  = os.path.abspath(os.path.dirname(__file__)) #obtem o caminho absoluto da pasta 
dados_dir = os.path.normpath(join_path(dados_py, '..', 'media'))
		#abspatch Retorna o caminho da pasta raiz até a pasta q está o arquivo 'projeto-pygame/source/ti'
		#dirname retornará somente a pasta (sem o arquivo) = 'source/ti'
		#join_path junta os parametros passador dados_py/../media
		# corrige alguns detalhes de diretório, como exemplo a barra e contrabarra;

endereço_arquivos = dict(
	imagens = join_path(dados_dir,'imagens'),
)


def endereco_arquivo(tipo, nome_arquivo):
    return join_path(endereco_arquivos[tipo], nome_arquivo)


def carrega(tipo, nome_arquivo, modo='rb'):
	return open(endereco_arquivo(tipo, nome_arquivo), modo)


def carrega_fonte(nome_arquivo):
    return endereco_arquivo('fontes', nome_arquivo)


def carrega_imagem(nome_arquivo):
	return endereco_arquivo('imagens', nome_arquivo)


def carrega_imagem_menu(nome_arquivo):
    nome_arquivo = carrega('imagens', nome_arquivo)
    try:
        image = pygame.image.load(nome_arquivo)
    except pygame.error:
        raise SystemExit, "Unable to load: " + nome_arquivo
    return image

