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

