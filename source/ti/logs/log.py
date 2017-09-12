from datetime import datetime
from pygaze import libtime


class GenerateInfo:
    def __init__(self):
        self.log_gen = LogGenerator()
        self.staring_log = []
        self.blink_log = []
        self.quadrant_log = []
        self.position_log = []
        self.fixation_log = []

    def start_staring(self, food_type):
        data = LogData(str(food_type), (libtime.get_time()))
        self.staring_log.append(data)

    def start_blinking(self, cont_blink, start_time, time_end):
        time = int(start_time[0]) - int(time_end[0])
        data = LogData("Qtd de Piscada:" + str(cont_blink) + "Tempo:", (time,), 'Posicao_inicio:', start_time[1], 'PosicaoFinal:', time_end[1])
        self.blink_log.append(data)

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
            if (initial_time == 0):
                analyzing = item.text
                initial_time = item.time

            end_time = item.time
            if (item.text != analyzing):
                final_time = (end_time - initial_time) / 1000
                lineNumber += 1
                header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
                line = header + analyzing + str(final_time)
                f.write(line + '\n')
                ##Reset
                initial_time = 0
                end_time = 0
                analyzing = item.text
        final_time = (end_time - initial_time) / 1000
        lineNumber += 1
        header = str(data_type) + " " + str(student_id) + " " + str(lineNumber) + " "
        line = header + analyzing + str(final_time)
        f.write(line + '\n')
        f.close()

class LogData:
    def __init__(self, text, time, *args):
        self.text = text
        self.time = time
        self.args = args
