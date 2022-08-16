from db_operations.Training_DataBase_Operation import DBOperation
from application_logging.logger import App_Logger
from data_transformation import DataTransform

class Train_Insertion:

    '''
    Used to insert training batch files into a DataBase and export the DataBase file to csv for model training.
    Attributes:
    1. Insertion
    '''

    def __init__(self):
        self.db_operation = DBOperation()
        self.log_writer = App_Logger()
        self.data_transform = DataTransform()
        self.file_object = open("training_logs/TrainingInsertionLog.txt", 'a+')
    
    def Insertion(self):

        '''
        Used to insert batch files into a DataBase and export the DataBase file to csv for model training.
        '''

        try:
            self.log_writer.log(self.file_object, "Starting Data Transforamtion.")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.data_transform.replace_with_null()
            self.log_writer.log(self.file_object, "Data Transforamtion completed.")
            
            #Create tables in the database created above
            self.log_writer.log(self.file_object,'Creating Training_DB tables.')
            # Create database tables
            self.db_operation.create_table('Training_DB')
            self.log_writer.log(self.file_object,'DataBase table created successfully.')

            #Insert data into table
            self.log_writer.log(self.file_object,'Insertion of data into tables started.')
            self.db_operation.insert_into_table('Training_DB')
            self.log_writer.log(self.file_object, 'Insertion of data into tables completed.')

            #Export data to CSV file
            self.log_writer.log(self.file_object,'Exporting data to CSV.')
            self.db_operation.ExportDB_to_CSV('Training_DB')
            self.log_writer.log(self.file_object,'Export to CSV completed.')

        except Exception as e:
            self.log_writer.log(self.file_object, f'Exception occurred in Insertion method of Train_Insertion class. Exception: {e}')
            raise Exception()