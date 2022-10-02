from configparser import MissingSectionHeaderError
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


class Preprocessing:
    
    '''
    Clean and transform the data before training
    Attributes:
    1. drop_columns()
    2. seperate_label_features()
    3. null_present()
    4. impute_missing_values()
    5. get_zero_std_columns()
    '''

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def drop_columns(self, data, columns):

        '''
        Drops the given columns from Pandas DataFrame
        Returns: Pandas Dataframe
        '''

        self.logger_object.log(self.file_object, 'Entered the drop_columns method of Preprocessing class.')
        self.data = data
        self.columns = columns

        try:
            self.refined_data = self.data.drop(labels = self.columns, axis = 1)
            self.logger_object.log(self.file_object, f'{self.columns} Features dropped successfully. Exited the drop_columns method of Preprocessing class.')
            return self.refined_data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in drop_columns method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Column drop unsuccessful. Exited the drop_columns method of Preprocessing class.')
            raise Exception()

    def seperate_label_features(self, data, label_column_name):

        '''
        Seperates the given Pandas DataFrame into features and labels
        Returns: Tuple of (Pandas Dataframe, Pandas Dataframe)
        '''

        self.logger_object.log(self.file_object, 'Entered the seperate_label_features method of Preprocessing class.')
        self.data = data
        self.label_column_name = label_column_name

        try:
            self.X = self.data.drop(labels = self.label_column_name, axis = 1)
            self.y = self.data[label_column_name]
            self.logger_object.log(self.file_object, 'Features-Label seperation successful. Exited the seperate_label_features method of Preprocessing class.')
            return self.X, self.y
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in seperate_label_features method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Features-Label seperation unsuccessful. Exited the seperate_label_features method of Preprocessing class.')
            raise Exception()

    def outlier_removal(self,data):

        '''
        Removes outliers present in the data
        Returns: Pandas DataFrame
        '''

        self.logger_object.log(self.file_object, 'Entered outlier_removal method of Preprocessing class.')
        self.data = data
        try:
            def outlier_limits(col):
                Q3, Q1 = np.nanpercentile(col, [75,25])
                IQR= Q3-Q1
                UL= Q3+1.5*IQR
                LL= Q1-1.5*IQR
                return UL, LL

            for column in self.data.columns:
                if self.data[column].dtype != 'int64':
                    UL, LL= outlier_limits(self.data[column])
                    self.data[column]= np.where((self.data[column] > UL) | (self.data[column] < LL), np.nan, self.data[column])

            self.logger_object.log(self.file_object, f'Outlier removal successful. Exited outlier_removal method of Preprocessing class.')

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in outlier_removal method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, f'Outlier removal unsuccessful. Exited outlier_removal method of Preprocessing class.')
            raise Exception()

        return self.data

    def log_transform(self,data):

        '''
        Applies logarithm to the values of the Pandas DataFrame
        Returns: Pandas DataFrame
        '''

        self.logger_object.log(self.file_object, 'Entered log_transform method of Preprocessing class.')
        self.data = data
        try:
            self.data.replace(0,1,inplace = True)
            self.data = np.log(self.data)
            self.logger_object.log(self.file_object, 'Log transformation successful. Exited the log_transformation method of Preprocessing class.')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in log_transform method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Log transformation unsuccessful. Exited log_transformation method of Preprocessing class.')
            raise Exception()

    def null_present(self, data):

        '''
        Checks whether null value is present column-wise in the given Pandas DataFrame
        Returns: Bool Value
        '''

        self.logger_object.log(self.file_object, 'Entered null_present method of Preprocessing class.')
        self.data = data
        self.isnull = False

        try:
            self.null_col_count = self.data.isnull().sum()
            for i in self.null_col_count:
                if i>0:
                    self.isnull = True
                    break
            if(self.isnull): #storing the null column names in the logs
                null_data = pd.DataFrame({'columns':self.data.isnull().sum().index, 'count':self.data.isnull().sum().values})
                null_data.to_csv('preprocessing_data/null_data.csv') #storing the info in a csv file
            self.logger_object.log(self.file_object, 'Finding missing values successful. Data written to null_data file. Exited the null_present method of Preprocessing class.')
            return self.isnull
        except Exception as e:
            self.logger_object.log(self.file_object,f'Exception occurred in null_present method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Null values detection unsuccessful. Exited the null_present method of Preprocessing class.')
            raise Exception()

    def impute_missing_values(self, data):

        '''
        Replaces all the missing values in the Dataframe using Simple Imputer
        Returns: Pandas Dataframe
        '''

        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data

        try:
            imputer = SimpleImputer(missing_values=np.nan, strategy='median')
            self.new_data = pd.DataFrame(imputer.fit_transform(self.data), columns=self.data.columns)
            self.logger_object.log(self.file_object, 'Missing values imputation successful. Exited the impute_missing_values method of Preprocessing class.')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in impute_missing_values method of Preprocessing class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Missing values imputation unsuccessful. Exited the impute_missing_values method of Preprocessing class.')
            raise Exception()
    
    def get_zero_std_columns(self, data):

        '''
        Finds the columns having zero standard deviation i.e., identical value in the columns
        Returns: List
        '''

        self.logger_object.log(self.file_object, 'Entered the get_zero_std_columns method of the Preprocessing class.')
        self.data = data
        self.cols_to_drop=[]

        try:
            for i in self.data.columns:
                if np.std(self.data[i]) == 0.0:
                    self.cols_to_drop.append(i)
            self.logger_object.log(self.file_object, 'Column-wise search for Zero Standard Deviation Successful. Exited the get_zero_std_columns method of the Preprocessor class.')
            return self.cols_to_drop
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_zero_std_columns method of the Preprocessor class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Search for Zero Standard Deviation Successful unsuccessful. Exited the get_zero_std_columns method of the Preprocessor class.')
            raise Exception()