#!/usr/bin/env python
from datetime import datetime
from pygaze import libtime
import avalgame


class GenerateInfo:
    def __init__(self):
        self.log_gen = LogGenerator()
        self.staring_log = []
        self.blink_log = []
        self.blink_log2 = []
        self.quadrant_log = []
        self.position_log = []
        self.fixation_log = []

        self.blinkPositionsAndCount = []  ## (x,y,count)
        self.fixationPositions = []  ## (x,y,0)

    def start_staring(self, food_type):
        data = LogData(str(food_type) + " ", (libtime.get_time()))
        self.staring_log.append(data)

    def start_blinkingTest(self, position, blinkCount):
        # data = LogData( "(" + position[0] + "," + position[1] + ") " + str(blinkCount), (libtime.get_time()))
        data = LogData(str(position) + " " + str(blinkCount) + " ", (libtime.get_time()))
        self.blink_log.append(data)

    def start_blinking(self, cont_blink, start_time, time_end):
        time = float(time_end[0])
        data = LogData(str(cont_blink), time)
        self.blink_log2.append(data)

    def get_quadrant(self, (x, y)):
        ## QUADRANTE A
        if (0 <= x <= 250) and (0 <= y <= 150):
            quadrant = "A1"
        elif (250 <= x <= 500) and (0 <= y <= 150):
            quadrant = "A2"
        elif (0 <= x <= 250) and (150 <= y <= 300):
            quadrant = "A3"
        elif (250 <= x <= 500) and (150 <= y <= 300):
            quadrant = "A4"
        ## QUADRANTE B
        elif (500 <= x <= 750) and (0 <= y <= 150):
            quadrant = "B1"
        elif (750 <= x <= 1000) and (0 <= y <= 150):
            quadrant = "B2"
        elif (500 <= x <= 750) and (150 <= y <= 300):
            quadrant = "B3"
        elif (750 <= x <= 1000) and (150 <= y <= 300):
            quadrant = "B4"
        ## QUADRANTE C
        elif (0 <= x <= 250) and (300 <= y <= 450):
            quadrant = "C1"
        elif (250 <= x <= 500) and (300 <= y <= 450):
            quadrant = "C2"
        elif (0 <= x <= 250) and (450 <= y <= 600):
            quadrant = "C3"
        elif (250 <= x <= 500) and (450 <= y <= 600):
            quadrant = "C4"
        ## QUADRANTE D
        elif (500 <= x <= 750) and (300 <= y <= 450):
            quadrant = "D1"
        elif (750 <= x <= 1000) and (300 <= y <= 450):
            quadrant = "D2"
        elif (500 <= x <= 750) and (450 <= y <= 600):
            quadrant = "D3"
        elif (750 <= x <= 1000) and (450 <= y <= 600):
            quadrant = "D4"
        else:
            quadrant = "FORA"

        data = LogData(quadrant + " ", libtime.get_time())
        self.quadrant_log.append(data)
        # self.log_gen.record_log(data, "LogQuadrant")

    def start_fixation(self, position):
        posString = "(" + str(position[0]) + "," + str(position[1]) + ") "
        data = LogData(posString, (libtime.get_time()))
        self.position_log.append(data)


class LogGenerator:
    def __init__(self):
        self.date_now = datetime.now

    ###
    #
    # file_name: name of the file without termination
    # data_type: enum {1,2,3,4} => fixation , quadrant , staring, blink

    def recordLog(self, data, file_name, data_type, student_id=0):

        dt = datetime.now()
        date_string = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
        filename = './logs/' + file_name + date_string + '.txt'
        lineNumber = 0
        header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "

        f = open(filename, 'a+')

        initial_time = 0
        end_time = 0

        analyzing = ""
        for item in data:
            if initial_time == 0:
                analyzing = item.text
                initial_time = item.time

            end_time = item.time
            if item.text != analyzing:
                final_time = (end_time - initial_time) / 1000
                lineNumber += 1
                header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
                line = header + analyzing + str(final_time)
                # f.write(line + '\n')
                ##Reset
                initial_time = 0
                end_time = 0
                analyzing = item.text
        final_time = (end_time - initial_time) / 1000
        lineNumber += 1

    ## NOVO
    def recordFinalFixationLog(self, avalgame, data, save_image=False):
        dateStart = datetime.now()
        lineNumber = 1
        for item in data:
            avalgame.recordFixation(dateStart=dateStart, tipo_AEEJ=1, codigo_AEEJ=931, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                                  valor_AEEJ_x=item[0], valor_AEEJ_y=item[1],valor_AEEJ_qtd=0,
                                  seq_number=lineNumber, save_image=save_image)
            lineNumber += 1

    def recordFinalBlinkLog(self, avalgame, data):
        dateStart = datetime.now()
        lineNumber = 1
        for item in data:
            avalgame.recordBlinks(dateStart=dateStart, tipo_AEEJ=1, codigo_AEEJ=932, nv_Jogo=1, fs_jogo=1, et_jogo=1,
                                  valor_AEEJ_x=item[0], valor_AEEJ_y=item[1], valor_AEEJ_qtd=item[2],
                                  seq_number=lineNumber, save_image=True)
            lineNumber += 1

    #### VERSAO ANTIGA, NAO DELETAR
    # def recordLog(self, data, file_name, data_type, student_id=0):
    #
    #     dt = datetime.now()
    #     date_string = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
    #     filename = './logs/' + file_name + date_string + '.txt'
    #     lineNumber = 0
    #     header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
    #
    #     f = open(filename, 'a+')
    #
    #     initial_time = 0
    #     end_time = 0
    #
    #     analyzing = ""
    #     for item in data:
    #         if initial_time == 0:
    #             analyzing = item.text
    #             initial_time = item.time
    #
    #         end_time = item.time
    #         if item.text != analyzing:
    #             final_time = (end_time - initial_time) / 1000
    #             lineNumber += 1
    #             header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
    #             line = header + analyzing + str(final_time)
    #             f.write(line + '\n')
    #             ##Reset
    #             initial_time = 0
    #             end_time = 0
    #             analyzing = item.text
    #     final_time = (end_time - initial_time) / 1000
    #     lineNumber += 1
    #     header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
    #     line = header + analyzing + str(final_time)
    #     f.write(line + '\n')
    #     f.close()

    def recordBlinkLog(self, data, file_name, data_type, student_id=0):
        dt = datetime.now()
        date_string = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
        filename = './logs/' + file_name + date_string + '.txt'
        lineNumber = 0
        header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "

        f = open(filename, 'a+')
        initial_time = 0
        end_time = 0

        analyzing = ""
        for item in data:
            analyzing = item.text
            lineNumber += 1
            header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
            line = header + analyzing + str(item.time)
            f.write(line + '\n')

        f.close()

    def recordFixationLog(self, data, file_name, data_type, student_id=0):
        dt = datetime.now()
        date_string = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
        filename = './logs/' + file_name + date_string + '.txt'
        lineNumber = 0
        header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "

        f = open(filename, 'a+')
        initial_time = 0
        end_time = 0

        analyzing = ""
        for item in data:
            analyzing = item.text
            lineNumber += 1
            header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
            line = header + analyzing + str(item.time)
            f.write(line + '\n')

        f.close()


class LogData:
    def __init__(self, text, time):
        self.text = text
        self.time = time
