from application_logging.logger import App_Logger
from data_transformation_prediction import DataTransformPrediction
from db_operations.Testing_DataBase_Operation import DBOperation
class Predict_Insertion:

    '''
    Used to insert testing files into a DataBase and export the DataBase file to csv for model prediction.
    Attributes:
    1. Insertion
    '''

    def __init__(self):
        self.log_writer = App_Logger()
        self.db_operation = DBOperation()
        self.data_transform = DataTransformPrediction()
        self.file_object = open("prediction_logs/PredictionInsertionLog.txt", 'a+')
    
    def Insertion(self):

        '''
        Used to insert batch files into a DataBase and export the DataBase file to csv for model training.
        '''

        try:
            self.log_writer.log(self.file_object, "Starting Data Transforamtion.")
            # replacing blanks in the csv file with "NULL" to insert in table
            self.data_transform.replace_with_null()
            self.log_writer.log(self.file_object, "Data Transforamtion completed.")

            #Create tables in the database created above
            self.log_writer.log(self.file_object,'Creating Testing_DB tables.')
            # Create database tables
            self.db_operation.create_table('Testing_DB')
            self.log_writer.log(self.file_object,'DataBase table created successfully.')

            #Insert data into table
            self.log_writer.log(self.file_object,'Insertion of data into tables started.')
            self.db_operation.insert_into_table('Testing_DB')
            self.log_writer.log(self.file_object, 'Insertion of data into tables completed.')

            #Export data to CSV file
            self.log_writer.log(self.file_object,'Exporting data to CSV.')
            self.db_operation.ExportDB_to_CSV('Testing_DB')
            self.log_writer.log(self.file_object,'Export to CSV completed.')

        except Exception as e:
            self.log_writer.log(self.file_object, f'Exception occurred in Insertion method of Prediction_Insertion class. Exception: {e}')
            raise Exception()