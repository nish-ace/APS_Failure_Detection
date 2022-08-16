import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods
from sklearn.cluster import k_means


class KMeansClustering:

    '''
    Divides the data into clusters before training 
    Attributes:
    1. elbow_plot()
    2. create_cluster()
    '''

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
            
        '''
        Saves the elbow plot to a file to decide the optimum number of clusters
        Returns: Integer, the optimal number of clusters
        '''

        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of KMeansClustering class.')
        self.data = data
        wcss=[]
        
        try:
            for i in range (1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42) 
                kmeans.fit(self.data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, f'The optimum number of clusters is: {self.kn.knee}. Exited the elbow_plot method of the KMeansClustering class.')
            return self.kn.knee
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in elbow_plot method of the KMeansClustering class. Exception:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):

        '''
        Creates a new dataframe consisting of the cluster information.
        Returns: Pandas DataFrame
        '''

        self.logger_object.log(self.file_object, 'Entered the create_clusters method of KMeansClustering class.')
        self.data = data

        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init = 'k-means++', random_state=30)
            self.y_kmeans = self.kmeans.fit_predict(data)
            self.file_op = file_methods.File_Operations(self.file_object, self.logger_object)
            self.file_op.save_model(self.kmeans, 'KMeans')
            self.data['cluster'] = self.y_kmeans
            self.logger_object.log(self.file_object, f'Succesfully created {self.kn.knee} clusters. Exited the create_clusters method of the KMeansClustering class.')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in create_cluster method of KMeansClustering class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Cluster creation unsuccessful. Exited the create_clusters method of the KMeansClustering class.')
            raise Exception()