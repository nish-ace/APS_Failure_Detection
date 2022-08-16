from os import listdir
import pandas
from application_logging.logger import App_Logger


class DataTransform:

    """
    Transforms the Raw Training Data before loading it in Database
    """

    def __init__(self):
        self.DataPath = 'training_batch_file'
        self.TargetPath = 'training_processed_batch_files'
        self.logger = App_Logger()


    def replace_with_null(self):
        
        """                            
        Replaces the missing values in columns with "NULL" to store in the table.
        """

        log_file = open("Training_Logs/DataTransformLog.txt", 'a+')
        try:
            onlyfiles = [f for f in listdir(self.DataPath)]
            for file in onlyfiles:
                csv = pandas.read_csv(self.DataPath+"/" + file)
                csv.replace("na","NULL",inplace=True)
                csv.to_csv(self.TargetPath+ "/" + file, index=None, header=True)
                self.logger.log(log_file,f"{file}: File Transformed successfully!!")
        except Exception as e:
               self.logger.log(log_file, f"Exception occurred in Data_Transformation. Exception:{e}")
               log_file.close()
        log_file.close()
