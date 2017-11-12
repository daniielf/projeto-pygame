#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import sys
import csv
sys.path.append('C:/Users/Daniel-PC/Downloads/WinPython-PyGaze-0.5.1/WinPython-PyGaze-0.5.1/python-2.7.3/Lib/site-packages')
from datetime import datetime
from cv2 import *



class Avalgame:
    _file = 'avalgame.install.cfg'
    _code = ""
    _status = False

    _done = False
    _playerCode = ""
    _date = ""
    _time = ""

    _wcam = VideoCapture(0)
    _imgf = './imagensjogadores/'
    _imgcnt = 0

    csvBlinkLines = [] # transformar em excel
    csvFixationLines = []

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

    def install(self, status, code=1):

        if type(status) is not bool:
            raise Exception("Valor invalido no argumento status ( bool )")

        if type(code) is not int or code < 0 or code > 999999:
            raise Exception("Valor invalido no argumento Codigo ( int ) 0-999999")

        f = open(self._file, 'w')

        f.writelines([
            "enabled:" + str(status) + '\n',
            "code:" + str(code) + '\n'
        ])

        # Diz se o modo de coleta de dados esta ativo
        self._status = status

        # Guarda codigo do jogo
        self._code = code

        f.close()

    def isEnabled(self):
        return self._status

    def initial(self, playerCode):

        if type(playerCode) is not int or playerCode < 0 or playerCode > 99999999999999:
            raise Exception("Valor invalido no argumento Codigo do Jogador ( int ) 0-99999999999999")

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
    def comp(self, tipo_AEEJ, codigo_AEEJ, nv_Jogo=1, fs_jogo=1, et_jogo=1, valor_AEEJ=0, valor_AEEJ_2=0, valor_AEEJ_3=0, imagem=False):

        nome_imagem = ''
        # Verifica se tudo foi iniciado.
        if self._done is False or self._status is False:
            return

        ###############################
        # Valida tipo argumentos
        ###############################
        # print(str(type(codigo_AEEJ)))
        # print(str(codigo_AEEJ))
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

        if type(valor_AEEJ) is not int or valor_AEEJ < 0 or valor_AEEJ > 9999:
            raise Exception("Valor invalido no argumento valor AEEJ ( int ) 0-9999")

        if type(valor_AEEJ_2) is not int or valor_AEEJ_2 < 0 or valor_AEEJ_2 > 9999:
            raise Exception("Valor invalido no argumento valor AEEJ ( int ) 0-9999")

        if type(valor_AEEJ_3) is not int or valor_AEEJ_3 < 0 or valor_AEEJ_3 > 9999:
            raise Exception("Valor invalido no argumento valor AEEJ ( int ) 0-9999")

        dt = datetime.now()

        if imagem:

            valida, imgObj = self._wcam.read()
            valida, imgObj = self._wcam.read()
            valida, imgObj = self._wcam.read()

            if valida:
                nome_imagem = 'I-%s-%s-%04d%02d%02d%02d%02d.raw.png' % (
                    self._playerCode,
                    self._imgcnt,
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour,
                    dt.minute)

                imwrite((self._imgf + nome_imagem), imgObj)
                self._imgcnt = self._imgcnt + 1


        f = open('./logs/LogAEEJ_%s.%s_%s.txt' % (
        self._playerCode, self._date.replace('-', ''), self._time.replace(':', '')),
                 'a+')

        f.write("%s;%s;%s%s;%d;%d;%d;'%s';%d;%d;%d;%d;%d;%04d-%02d-%02d;%02d:%02d;'%s'\n" %
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
                 valor_AEEJ_2,
                 valor_AEEJ_3,
                 self._imgcnt,
                 dt.year,
                 dt.month,
                 dt.day,
                 dt.hour,
                 dt.minute,
                 nome_imagem)
                )

        f.close()

    def storeCreditCollection(self, dateStart, tipo_AEEJ='A', codigo_AEEJ=1, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                              valor_AEEJ=1):
        dt = datetime.now()
        f = open('./logs/CreditCard_LOG.txt',
                 'a+')

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %d %04d-%02d-%02d %02d:%02d\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
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

    def storePyramidCompletion(self, dateStart, tipo_AEEJ='T', codigo_AEEJ=11, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                               valor_AEEJ=0):
        dt = datetime.now()
        f = open('./logs/PyramidCompletion_LOG.txt',
                 'a+')

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %.1f %04d-%02d-%02d %02d:%02d\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
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

    def storeFoodQuantity(self, dateStart, tipo_AEEJ='T', codigo_AEEJ=11, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                          valor_AEEJ=0):
        dt = datetime.now()
        f = open('./logs/FoodQuantity_LOG.txt',
                 'a+')

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %d %04d-%02d-%02d %02d:%02d\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
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

    def storeAverageScore(self, dateStart, tipo_AEEJ='T', codigo_AEEJ=11, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                          valor_AEEJ=0):
        dt = datetime.now()
        f = open('./logs/AverageScore_LOG.txt',
                 'a+')

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %d %04d-%02d-%02d %02d:%02d\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
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

    def recordBestScore(self, time, score):
        f = open("./logs/bestScore.txt", "a+")
        f.write(str(self._playerCode) + " " + str(score) + " " + str(time) + "\n")

    ## NOVO
    def recordFixation(self, dateStart, tipo_AEEJ='T', codigo_AEEJ=931, nv_Jogo=1, fs_jogo=1, et_jogo=1, valor_AEEJ_x=0,
                       valor_AEEJ_y=0, valor_AEEJ_qtd=0, seq_number=0, save_image=False):
        dt = datetime.now()
        f = open('./logs/Fixation_LOG.txt', 'a+')

        fullDateStart = str(dateStart.year) + "-" + str(dateStart.month) + "-" + str(dateStart.day)
        fullHourStart = str(dateStart.hour) + ":" + str(dateStart.minute)

        fullDateEnd = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
        fullHourEnd = str(dt.hour) + ":" + str(dt.minute)

        if (save_image):
            filePath = 'I-%s-%s-%04d%02d%02d%02d%02d.raw.png' % (
                self._playerCode,
                self._imgcnt,
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute)

            imwrite((self._imgf + nome_imagem), imgObj)
            self._imgcnt = self._imgcnt + 1

        csvLine = (
            self._playerCode, fullDateStart, fullHourStart, self._code, nv_Jogo, fs_jogo, et_jogo, tipo_AEEJ,
            codigo_AEEJ,
            valor_AEEJ_x, valor_AEEJ_y, valor_AEEJ_qtd, seq_number, fullDateEnd, fullHourEnd, "")
        self.csvFixationLines.append(csvLine)

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %d %d %d %d %04d-%02d-%02d %02d:%02d %s\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
                 self._code,
                 nv_Jogo,
                 fs_jogo,
                 et_jogo,
                 tipo_AEEJ,
                 codigo_AEEJ,
                 valor_AEEJ_x,
                 valor_AEEJ_y,
                 valor_AEEJ_qtd,
                 seq_number,
                 dt.year,
                 dt.month,
                 dt.day,
                 dt.hour,
                 dt.minute,
                 filePath)
                )

        f.close()

    def recordBlinks(self, dateStart, tipo_AEEJ='T', codigo_AEEJ=932, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                              valor_AEEJ_x=0, valor_AEEJ_y=0, valor_AEEJ_qtd=0, seq_number=0, save_image=False):

        dt = datetime.now()
        f = open('./logs/Blink_LOG.txt',
                 'a+')

        fullDateStart = str(dateStart.year) + "-" + str(dateStart.month) + "-" + str(dateStart.day)
        fullHourStart = str(dateStart.hour) + ":" + str(dateStart.minute)

        fullDateEnd = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
        fullHourEnd = str(dt.hour) + ":" + str(dt.minute)

        ## IMG SAVING
        if (save_image):
            filePath = 'I-%s-%s-%04d%02d%02d%02d%02d.raw.png' % (
                self._playerCode,
                self._imgcnt,
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute)

            imwrite((self._imgf + nome_imagem), imgObj)
            self._imgcnt = self._imgcnt + 1

        csvLine = (
        self._playerCode, fullDateStart, fullHourStart, self._code, nv_Jogo, fs_jogo, et_jogo, tipo_AEEJ, codigo_AEEJ,
        valor_AEEJ_x, valor_AEEJ_y, valor_AEEJ_qtd, seq_number, fullDateEnd, fullHourEnd, "")
        self.csvBlinkLines.append(csvLine)

        f.write("%s %04d-%02d-%02d %02d:%02d %s %d %d %d '%s' %s %d %d %d %d %04d-%02d-%02d %02d:%02d %s\n" %
                (self._playerCode,
                 dateStart.year,
                 dateStart.month,
                 dateStart.day,
                 dateStart.hour,
                 dateStart.minute,
                 self._code,
                 nv_Jogo,
                 fs_jogo,
                 et_jogo,
                 tipo_AEEJ,
                 codigo_AEEJ,
                 valor_AEEJ_x,
                 valor_AEEJ_y,
                 valor_AEEJ_qtd,
                 seq_number,
                 dt.year,
                 dt.month,
                 dt.day,
                 dt.hour,
                 dt.minute,
                 filePath)
                )

        f.close()

    def startCSV(self,fileName):
        if (not os.path.isfile("./logs/" + fileName + "_Table.csv")):
            print("criou")
            with open('./logs/' + fileName + '_Table.csv', 'a') as csvfile:
                field_names = ["Matricula", "Data_Inicio", "Hora_Inicio", "Cod_Jogo", "Nivel_Jogo", "Fase_Jogo",
                               "Etapa_Jogo", "Tipo_AEEJ", "Cod_AEEJ", "AEEJ_1", "AEEJ_2", "AEEJ_3", "N_Sequencial",
                               "Data_Termino", "Hora_Termino", "Arquivo_Imagem"]
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writerow({'Matricula': "Matricula",
                                 "Data_Inicio": "Data_Inicio",
                                 "Hora_Inicio": "Hora_Inicio",
                                 "Cod_Jogo": "Cod_Jogo",
                                 "Nivel_Jogo": "Nivel_Jogo",
                                 "Fase_Jogo": "Fase_Jogo",
                                 "Etapa_Jogo": "Etapa_Jogo",
                                 "Tipo_AEEJ": "Tipo_AEEJ",
                                 "Cod_AEEJ": "Cod_AEEJ",
                                 "AEEJ_1": "AEEJ_1",
                                 "AEEJ_2": "AEEJ_2",
                                 "AEEJ_3": "AEEJ_3",
                                 "N_Sequencial": "N_Sequencial",
                                 "Data_Termino": "Data_Termino",
                                 "Hora_Termino": "Hora_Termino",
                                 "Arquivo_Imagem": "Arquivo_Imagem"
                                 })

    def exportCSV(self, fileName, dataSet):
        with open('./logs/' + fileName + '_Table.csv', 'a') as csvfile:
            field_names = ["Matricula", "Data_Inicio", "Hora_Inicio", "Cod_Jogo", "Nivel_Jogo", "Fase_Jogo",
                           "Etapa_Jogo", "Tipo_AEEJ", "Cod_AEEJ", "AEEJ_1", "AEEJ_2", "AEEJ_3", "N_Sequencial",
                           "Data_Termino", "Hora_Termino", "Arquivo_Imagem"]
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            for item in dataSet:
                writer.writerow({'Matricula': item[0],
                                 "Data_Inicio": item[1],
                                 "Hora_Inicio": item[2],
                                 "Cod_Jogo": item[3],
                                 "Nivel_Jogo": item[4],
                                 "Fase_Jogo": item[5],
                                 "Etapa_Jogo": item[6],
                                 "Tipo_AEEJ": item[7],
                                 "Cod_AEEJ": item[8],
                                 "AEEJ_1": item[9],
                                 "AEEJ_2": item[10],
                                 "AEEJ_3": item[11],
                                 "N_Sequencial": item[12],
                                 "Data_Termino": item[13],
                                 "Hora_Termino": item[14],
                                 "Arquivo_Imagem": item[15]
                                 })
