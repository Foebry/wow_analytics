from datetime import datetime

import datetime
import time
import mysql.connector
import os



class Logger:

    def __init__(self, loc, rot='h'):
        self.path = os.path.join(loc, 'Logs')
        self.rot = rot

        if not os.path.exists(self.path): os.makedirs(self.path)

        self.files = {
            'Database': None,
            'Debug': None,
            'Error': None,
            "Warning": None,
            "Info": None
        }

        self.timings = {
            'Database': None,
            'Debug': None,
            'Error': None,
            'Warning': None,
            'Info': None
        }

        sql = f'{self.path}//Database'
        debug = f'{self.path}//Debug'
        error = f'{self.path}//Error'
        attention = f'{self.path}//Warning'
        info = f'{self.path}//Info'

        if os.path.exists(f'{self.path}//Database') and len(os.listdir(sql)) >= 1: self.files['Database'] = max(os.listdir(sql))
        if os.path.exists(f'{self.path}//Debug') and len(os.listdir(debug)) >= 1: self.files['Debug'] = max(os.listdir(debug))
        if os.path.exists(f'{self.path}//Error') and len(os.listdir(error)) >= 1: self.files['Error'] = max(os.listdir(error))
        if os.path.exists(f'{self.path}//Warning') and len(os.listdir(warning)) >= 1: self.files['Warning'] = max(os.listdir(warning))
        if os.path.exists(f'{self.path}//Info') and len(os.listdir(info)) >= 1: self.files['Info'] = max(os.listdir(info))


    def CreateNewFile(self, file):
        dir = os.path.join(self.path, file)

        if not os.path.exists(dir): os.makedirs(dir)

        now = datetime.datetime.now()

        if self.rot == 'w': filename = f'Week {datetime.date(now.year, now.month, now.day).strftime("%V")}.log'
        elif self.rot == 'd': filename = f'{now.date()}.log'
        elif self.rot == 'h': filename = f'{now.date()}_{now.hour}h.log'
        elif self.rot == 'm': filename = f'{now.date()}_{now.hour}h_{now.minute}m.log'
        elif self.rot == 's': filename = f'{now.date()}_{now.hour}h_{now.minute}m_{now.second}s.log'

        self.files[file] = os.path.join(self.path, file, filename)
        temp = open(self.files[file], 'a')
        temp.close()
        self.timings[file] = datetime.datetime.now()


    def log(self, debug=False, msg=None, type=None, timestamped=True):

        allocation = {
            "Info": [None,],
            "Database": [mysql.connector.errors.ProgrammingError,mysql.connector.errors.IntegrityError],
            "Warning": [KeyError, UnboundLocalError]
        }

        level = "Warning"

        for key in allocation:
            if type in allocation[key]:
                level = key
                break
            level = "Error"

        if debug: level = "Debug"

        self.IsValidTimeFrame(level)

        if level == "Warning":
            msg += f" //  {str(type)}"

        if level == "Warning": self.warning(msg, type)
        elif level == "Debug": self.debug(msg, type, timestamped)
        elif level == "Info": self.info(msg, type, timestamped)
        elif level == "Database": self.database(msg, type)
        elif level == "Error": self.error(msg, type)


    def warning(msg, type):
        time = f'{datetime.datetime.now()} - '

        file = open(os.path.join(self.path, "Warning", self.files["Warning"]), 'a')
        message = "\n"*2 + "WARNING:"+"%s%s"%(time, msg) + "*"*100

        file.write(message)
        file.close()


    def debug(msg, type, timestamped):
        time = ""
        if timestamped: time = f'{datetime.datetime.now()} - '

        file = open(os.path.join(self.path, "Debug", self.files["Debug"]), "a")
        message = "\n"*2+"DEBUG:"+"%s%s"%(time, msg)+"*"*100

        file.write(message)
        file.close()


    def Info(msg, type, timestamped):
        time = ""
        if timestamped: time = f'{datetime.datetime.now()} - '

        file = open(os.path.join(self.path, "Info", self.files["Info"]), "a")
        message = "INFO:"+"%s%s"%(time, msg)

        file.write(message)
        file.close()


    def database(msg, type):
        time = f'{datetime.datetime.now()} - '

        file = open(os.path.join(self.path, "Database", self.files["Database"]), "a")
        message = "\n"*2+"Database:" + "%s%s"%(time, msg)+"*"*100

        file.write(message)
        file.close()


    def Error(msg, type):
        time = f'{datetime.datetime.now()} - '

        file = open(os.path.join(self.path, "Error", self.files["Error"]), "a")
        message = "\n"*2+"ERROR: "+"%s%s"%(time, msg)+"*"*100

        file.write(message)
        file.close()


    def IsValidTimeFrame(self, file):
        creation = self.timings[file]
        now = datetime.datetime.now()

        if self.files[file] is None: self.CreateNewFile(file)
        else:
            diff_week = creation is None or (not datetime.date(creation.year, creation.month, creation.day).strftime("%V") == datetime.date(now.year, now.month, now.day).strftime("%V"))
            diff_day = creation is None or (not now.date() == creation.date())
            diff_h = creation is None or (diff_day or not now.hour == creation.hour)
            diff_m = creation is None or (diff_h or not now.minute == creation.minute)
            diff_s = creation is None or (diff_m or not now.second == creation.second)

            if self.rot == 'w' and diff_week: self.CreateNewFile(file)
            elif self.rot == 'd' and diff_day: self.CreateNewFile(file)
            elif self.rot == 'h' and diff_h: self.CreateNewFile(file)
            elif self.rot == 'm' and diff_m: self.CreateNewFile(file)
            elif self.rot == 's' and diff_s: self.CreateNewFile(file)
