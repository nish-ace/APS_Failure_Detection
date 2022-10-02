import pandas as pd

class Get_Test_Data:
    
    '''
    Used to load data from source file for prediction
    Attributes:
    1. get_data()
    '''
        
    def __init__(self, file_object, logger_object):
        self.training_file = 'prediction_file_from_DB/aps_test_set.csv'
        self.file_object = file_object #file object
        self.logger_object = logger_object #logger class object
    
    def get_data(self):
    
        '''
        Stores the input data into a DataFrame to be used for prediction
        Returns: Pandas DataFrame
        '''

        self.logger_object.log(self.file_object,'Entered the get_data method of the Get_Data class')
        try:
            self.data = pd.read_csv(self.training_file)
            self.logger_object.log(self.file_object, 'Data load successful. Exited the get_data method of Get_Data class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_data method of Get_Data class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Data load unsuccessful. Exited the get_data method of Get_Data class')
            raise Exception()