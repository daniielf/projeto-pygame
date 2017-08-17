#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys


class Avalgame:

    _file = 'avalgame.install.cfg'
    _code = ""
    _status = False

    _done = False
    _playerCode = ""
    _date = ""
    _time = ""


    def __init__(self):
        try:
            f = open(self._file, 'r')

            lines = f.readlines()

            #####################################################################
            ## Tenta iniciar as configurações a partir de um arquivo de texto
            #####################################################################

            if len(lines) >= 2:
                statusLine = lines[0].split(':')
                codeLine = lines[1].split(':')

                if len(statusLine) == 2 and len(codeLine) == 2:
                    if statusLine[0].strip() == 'enabled':
                        statusLine = statusLine[1].strip()
                    else:
                        statusLine = 'False'

                    if statusLine.upper() == 'TRUE':
                        self._status = True
                    else:
                        self._status = False

                    if codeLine[0].strip() == 'code':
                        self._code = codeLine[1].strip()

                        try:
                            self._code = int(self._code)
                        except:
                            self._code = None
                            self._status = True

                    else:
                        self._code = None
                        self._status = False



                else:
                    self._code = None
                    self._status = False
        except IOError:
            self._code = None
            self._status = False
        except:
            raise Exception("Unexpected error:", sys.exc_info()[0])

    def install(self, status, code):

        if type(status) is not bool:
            raise Exception("Valor invalido no argumento status ( bool )")

        if type(code) is not int or code < 0 or code > 999999:
            raise Exception("Valor invalido no argumento Codigo ( int ) 0-999999")

        f = open(self._file, 'w')

        f.writelines([
            "enabled:" + str(status) + '\n',
            "code:" + str(code) + '\n'
        ])

        #Diz se o modo de coleta de dados esta ativo
        self._status = status

        #Guarda codigo do jogo
        self._code = code

        f.close()

    def isEnabled(self):
        return self._status

    def initial(self, playerCode):

        if type(playerCode) is not int or playerCode < 0 or playerCode > 999999:
            raise Exception("Valor invalido no argumento Codigo do Jogador ( int ) 0-999999")

        self._playerCode = playerCode
        dt = datetime.now()

        # Formata data e hora para uso posterior
        self._date = "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)
        self._time = "%02d:%02d" % (dt.hour, dt.minute)

        # Diz que o objeto esta pronto para fazer os logs
        if self._status:
            self._done = True
        else:
            self._done = False

    ###########################################################
    # comp - Registra uma linha no arquivo de log do jogador
    # @tipo_AEEJ: Obrigatorio, Tipo do log AEEJ (C – conhecimento, H-habilidade, A-atitude)
    # @codigo_AEEJ: Obrigatorio, Numero sequencial a cargo do desenvolvedor 0-999
    # @nv_Jogo: Opsional, Nivel de dificuldade informado pelo desenvolvedor 0-99 padrão 1
    # @fs_jogo: Opsional, Fase do jogo informado pelo desenvolvedor 0-99 padrão 1
    # @et_jogo: Opsional, Etapa da fase informada pelo desenvolvedor 0-99 padrão 1
    # @valor_AEEJ: Opsional, Valor da pontuação feita pelo jogador, 0-99 padrão 0
    ##############################
    def comp(self, tipo_AEEJ, codigo_AEEJ, nv_Jogo=1, fs_jogo=1, et_jogo=1, valor_AEEJ=0):

        #Verifica se tudo foi iniciado.
        if self._done is False or self._status is False:
            return

        ###############################
        # Valida tipo argumentos
        ###############################
        print(str(type(codigo_AEEJ)))
        print(str(codigo_AEEJ))
        if type(codigo_AEEJ) is not int and codigo_AEEJ < 0 or codigo_AEEJ > 999:
            raise Exception("Valor invalido no argumento codigo AEEJ ( int )")

        if type(tipo_AEEJ) is not str and tipo_AEEJ in ["C", "H", "A"]:
            raise Exception("Valor invalido no argumento TIPO ( C => conhecimento, H => habilidade, A => atitude )")

        if type(nv_Jogo) is not int or nv_Jogo < 0 or et_jogo > 99:
            raise Exception("Valor invalido no argumento Nivel ( int )")

        if type(fs_jogo) is not int or fs_jogo < 0 or et_jogo > 99:
            raise Exception("Valor invalido no argumento Fase ( int )")

        if type(et_jogo) is not int or et_jogo < 0 or et_jogo > 99:
            raise Exception("Valor invalido no argumento Etapa ( int )")

        if type(valor_AEEJ) is not int or valor_AEEJ < 0 or valor_AEEJ > 99:
            raise Exception("Valor invalido no argumento valor AEEJ ( int ) 0-99")
        # ate 99


        dt = datetime.now()

        f = open('LogAEEJ_%s.%s_%s.txt' % (self._playerCode, self._date.replace('-', ''), self._time.replace(':', '')),
                 'a+')

        f.write("%s;%s;%s;%s;%d;%d;%d;'%s';%s;%d;%04d-%02d-%02d;%02d:%02d\n" %
                (self._playerCode,
                 self._date,
                 self._time,
                 self._code,
                 nv_Jogo,
                 fs_jogo,
                 et_jogo,
                 tipo_AEEJ,
                 codigo_AEEJ,
                 valor_AEEJ,
                 dt.year,
                 dt.month,
                 dt.day,
                 dt.hour,
                 dt.minute)
              )

        f.close()
