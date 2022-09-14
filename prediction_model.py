import pandas as pd
from application_logging import logger
from data_preprocessing import preprocess
from data_ingestion import load_train_data
from file_operations import file_methods
from data_ingestion.load_prediction_data import Get_Data
from sklearn.metrics import confusion_matrix

class Predict_Model:
    
    '''
    Performs preprocessing and model fitting operations on test dataset.
    Attributes:
    1. model_prediction
    '''

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open('prediction_logs/ModelPredictionLog.txt', 'a+')
        self.getData = Get_Data(self.file_object, self.log_writer)

    def model_prediction(self):
        self.log_writer.log(self.file_object, 'Start of Prediction.')

        try:
            #get data from source
            getData = load_train_data.Get_Data(self.file_object, self.log_writer)
            data = getData.get_data()

            #preprocessing the data
            preprocessor = preprocess.Preprocessing(self.file_object, self.log_writer)

            data = preprocessor.drop_columns(data, 'Idx')

            #check for null values in feature columns, if present impute the missing values
            
            if(preprocessor.null_present(data)):
                data = preprocessor.impute_missing_values(data)

            #check for columns having zero standard deviation
            # cols_to_drop = preprocessor.get_zero_std_columns(data)

            #drop the columns obtained above
            # data = preprocessor.drop_columns(data,cols_to_drop)

            #split into X, y_true columns and
            X,y = preprocessor.seperate_label_features(data, 'class')

            X = preprocessor.log_transform(X) #log transforming the data, due to heavy skewness present

            #check for null values in feature columns, if present impute the missing values
            if(preprocessor.null_present(X)):
                X = preprocessor.impute_missing_values(X)

            #load model
            file_loader=file_methods.File_Operations(self.file_object,self.log_writer)
            kmeans=file_loader.load_model('KMeans')

            #clustering the data
            clusters=kmeans.predict(X)#drops the first column for cluster prediction
            X['clusters']= clusters
            X['label'] = y
            data = pd.DataFrame()
            sum = 0
            cluster=X['clusters'].unique()
            for i in cluster:
                cluster_table = X[X['clusters']==i]
                cluster_data, y_true = cluster_table.drop(['clusters','label'],axis=1),cluster_table['label']
                model_name = file_loader.correct_model_file(i)
                model = file_loader.load_model(model_name)
                tn, fp, fn, tp = confusion_matrix(y_true=y_true, y_pred=model.predict(cluster_data)).ravel()
                result = {f'cost{i}':fn*500 + fp*10}
                sum+= fn*500 + fp*10
                
            self.log_writer.log(self.file_object,'Successful end of Prediction.')
            result = pd.DataFrame({'Sum':sum})

        except Exception as e:
            self.log_writer.log(self.file_object, f'Exception occurred in predicting model. Exception: {e}')
            self.log_writer.log(self.file_object, f'Unsuccessful end of prediction.')
            raise Exception()
        return sum, result.head().to_json(orient="records")