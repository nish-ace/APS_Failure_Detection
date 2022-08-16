from datetime import datetime


class App_Logger:

    '''
    Writes log messages for each operation executed in a text file
    Attributes:
    1. log()
    '''

    def __init__(self):
        pass

    def log(self, file_object, log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.curr_time = self.now.strftime('%H:%M:%S')
        file_object.write(str(self.date)+'/'+str(self.curr_time)+'\t\t'+log_message+'\n')