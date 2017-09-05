from datetime import datetime
from pygaze import libtime


class GenerateInfo:
    def __init__(self):
        self.log_gen = LogGenerator()
        self.log = []

    def start_staring(self, food_type):
        data = LogData("Observou " + str(food_type) + " ", (libtime.get_time()))
        self.log.append(data)
        self.log_gen.record_log(data, 'LogStaring')

    def start_blinking(self, cont_blink):
        data = LogData("Qtde de Piscada:" + str(cont_blink) + "Tempo:", (libtime.get_time()))
        self.log.append(data)
        self.log_gen.record_log(data, 'LogBlinking')

    def get_quadrant(self, (x, y)):
        ## QUADRANTE A
        if ((0 <= x <= 250 ) and (0 <= y <= 150)):
            quadrant = "A1"
        elif ((250 <= x <= 500 ) and (0 <= y <= 150)):
            quadrant = "A2"
        elif ((0 <= x <= 250 ) and (150 <= y <= 300)):
            quadrant = "A3"
        elif ((250 <= x <= 500 ) and (150 <= y <= 300)):
            quadrant = "A4"
        ## QUADRANTE B
        elif ((500 <= x <= 750 ) and (0 <= y <= 150)):
            quadrant = "B1"
        elif ((750 <= x <= 1000 ) and (0 <= y <= 150)):
            quadrant = "B2"
        elif ((500 <= x <= 750 ) and (150 <= y <= 300)):
            quadrant = "B3"
        elif ((750 <= x <= 1000 ) and (150 <= y <= 300)):
            quadrant = "B4"
        ## QUADRANTE C
        elif ((0 <= x <= 250 ) and (300 <= y <= 450)):
            quadrant = "C1"
        elif ((250 <= x <= 500 ) and (300 <= y <= 450)):
            quadrant = "C2"
        elif ((0 <= x <= 250 ) and (450 <= y <= 600)):
            quadrant = "C3"
        elif ((250 <= x <= 500 ) and (450 <= y <= 600)):
            quadrant = "C4"
        ## QUADRANTE D
        elif ((500 <= x <= 750 ) and (300 <= y <= 450)):
            quadrant = "D1"
        elif ((750 <= x <= 1000 ) and (300 <= y <= 450)):
            quadrant = "D2"
        elif ((500 <= x <= 750 ) and (450 <= y <= 600)):
            quadrant = "D3"
        elif ((750 <= x <= 1000 ) and (450 <= y <= 600)):
            quadrant = "D4"
        else:
            quadrant = "FORA"

        data = LogData("Observou " + quadrant + " ", libtime.get_time())
        self.log.append(data)
        self.log_gen.record_log(data, "LogQuadrant")


class LogGenerator:
    def __init__(self):
        self.date_now = datetime.now
        self.data_to_log_staring = []
        self.data_to_log_quadrant = []
        self.data_to_log_blink = []
        self.data_to_log_fixation = []

    def record_log(self, data, file_name):
        file_name = file_name
        dt = datetime.now()
        date_string = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
        filename = file_name + date_string + '.txt'

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
                line = analyzing + str(final_time)
                f.write(line + '\n')
                ##Reset
                initial_time = 0
                end_time = 0
                analyzing = item.text
        final_time = (end_time - initial_time) / 1000
        line = analyzing + str(final_time)
        f.write(line + '\n')
        f.close()

    def store_data_fixation(self, array):
        self.data_to_log_fixation = array

    def store_data_quadrant(self, array):
        self.data_to_log_quadrant = array

    def store_data_blink(self, array):
        self.data_to_log_blink = array

    def store_data_staring(self, array):
        self.data_to_log_staring = array


class LogData:
    def __init__(self, text, time):
        self.text = text
        self.time = time
