import os
import shutil
import pickle


class File_Operations:

    '''
    Used to save the model after training and load the saved model for prediction.
    Attributes:
    1. save_model()
    2. load_model()
    3. correct_model_file()
    '''

    def __init__(self, file_object, logger_object):
        self.logger_object = logger_object
        self.file_object = file_object
        self.model_directory='models/'

    def save_model(self, model, filename):

        '''
        Saves model file using Pickle module
        Returns: None
        '''

        self.logger_object.log(self.file_object, 'Entered the save_model method of File_Operations class.')

        try:
            path = os.path.join(self.model_directory,filename) #creates seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path +'/' + filename+'.sav','wb') as f: # opens the file in binary format for writing.
                pickle.dump(model, f) # save the model to file
            self.logger_object.log(self.file_object, f'Model file {filename} saved. Exited the save_model method of File_Operations class.')
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in save_model method of File_Operations class. Exception: {e}')
            self.logger_object.log(self.file_object, f'Model File {filename} save unsuccessful. Exited the save_model method of File_Operations class.')
            raise Exception()

    def load_model(self, filename):

        '''
        Load the model file to memory
        Returns: Pickle file object
        '''

        self.logger_object.log(self.file_object, 'Entered the the load_model method of File_Operations class.')

        try:
            with open(self.model_directory + filename + '/' + filename + '.sav','rb') as f:
                self.logger_object.log(self.file_object, f'Model File {filename} loaded. Exited the load_model method of File_Operations class.')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in load_model method of File_Operations class. Exception: {e}')
            self.logger_object.log(self.file_object, f'Model File {filename} load unsuccessful. Exited the load_model method of File_Operations class.')
            raise Exception()

    def correct_model_file(self, cluster_number):

        '''
        Selects the appropriate model based on cluster number
        Returns: Pickle file
        '''

        self.logger_object.log(self.file_object, 'Entered the correct_model_file method of File_Operations class.')

        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.files_list = os.listdir(self.folder_name)
            for self.file in self.files_list:
                try:
                    if (self.file.index(str( self.cluster_number))!=-1):
                        self.model_name=self.file
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,'Finding correct model file successful. Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,f'Exception occured in correct_model_file method of the File_Operations class. Exception: {e}')
            self.logger_object.log(self.file_object,'Finding correct model file unsuccessful. Exited the correct_model_file method of the File_Operations class.')
            raise Exception()