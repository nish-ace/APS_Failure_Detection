from sklearn.model_selection import train_test_split
from application_logging import logger
from data_ingestion import load_train_data
from data_preprocessing import preprocess, clustering
from best_model_fit import tuning
from file_operations import file_methods
from imblearn.over_sampling import SMOTE


class Train_Model:

    '''
    Trains the model on the dataset after preprocessing 

    Attriutes:
    1. model_training
    '''

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open('training_logs/ModelTrainingLog.txt', 'a+')

    def model_training(self):

        '''
        Preprocesses the data, then finds and fits the best model cluster-wise.
        Returns: None
        '''

        self.log_writer.log(self.file_object, 'Start of Training.')

        try:
            #get data from source
            getData = load_train_data.Get_Data(self.file_object, self.log_writer)
            data = getData.get_data()

            #preprocessing the data
            preprocessor = preprocess.Preprocessing(self.file_object, self.log_writer)

            #drop 'Idx' column
            data = preprocessor.drop_columns(data, 'Idx')

            #seperate label and features column
            X,y = preprocessor.seperate_label_features(data,'class')

            X = preprocessor.outlier_removal(X) #removing the outliers

            X = preprocessor.log_transform(X) #log transforming the data, due to heavy skewness present in the dataset

            #check for null values in feature columns, if present impute the missing values
            if(preprocessor.null_present(X)):
                X = preprocessor.impute_missing_values(X)

            #check for columns having zero standard deviation
            # cols_to_drop = preprocessor.get_zero_std_columns(X)

            #drop the columns obtained above
            # X = preprocessor.drop_columns(X,cols_to_drop)

            '''Oversampling the data to avoid the imabalance class problem'''
            smote = SMOTE()
            X_, y_ = smote.fit_resample(X, y)

            '''Clustering Approach'''

            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)
            cluster_count = kmeans.elbow_plot(X_)
            
            #divide data into clusters
            X_ = kmeans.create_clusters(X_,cluster_count)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X_['labels']=y_

            cluster_list = X_['cluster'].unique()

            '''parsing all the clusters and looking for the best ML algorithm to fit on individual cluster'''

            for i in cluster_list:
                cluster_data = X_[X_['cluster'] == i]
                cluster_features=cluster_data.drop(['labels','cluster'],axis=1)
                cluster_label= cluster_data['labels']

                #splitting the clustered data into train and test subsets
                train_X, test_X, train_y, test_y = train_test_split(cluster_features, cluster_label, test_size=0.3, random_state=100)

                #getting best model for each cluster
                find_model = tuning.Model_Finder(self.file_object, self.log_writer)
                best_model_name, best_model = find_model.get_best_model(train_X, test_X, train_y, test_y)

                #saving the best model to directory
                file_ops = file_methods.File_Operations(self.file_object, self.log_writer)
                file_ops.save_model(best_model, best_model_name+str(i))

            self.log_writer.log(self.file_object, 'Successful end of training.')
            self.file_object.close()
        except Exception as e:
            self.log_writer.log(self.file_object, f'Exception occurred during training. Exception: {e}')
            self.log_writer.log(self.file_object, 'Unsuccessful end of training.')
            self.file_object.close()
            raise Exception()
