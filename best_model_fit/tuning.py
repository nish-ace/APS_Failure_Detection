import numpy as np
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from file_operations.file_methods import File_Operations
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix, precision_recall_curve

class Model_Finder:

    '''
    Fits the model with the input data and saves the model files using pickle

    Attributes:
    1. fit_RF
    2. fit_XGB
    3. fit_NB

    '''

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rf = RandomForestClassifier()
        self.lgbm = LGBMClassifier()
        self.nb = GaussianNB()
        self.mlp = MLPClassifier()

    
    def fit_RF(self, train_X, train_y):

        '''
        Gets the parameters for RandomForest Algorithm which give the best accuracy and saves the model using pickle
        Returns: None
        '''

        self.logger_object.log(self.file_object, 'Entered the fit_RF method of Model_Finder class.')
        
        try:
            self.param_grid = {'n_estimators':800,
              'max_depth':13,
              'min_samples_split' : 12,
              'max_leaf_nodes': 300,
              'ccp_alpha':0.01,
              'criterion': 'gini'}

            self.rf = RandomForestClassifier(**self.param_grid)
            self.rf.fit(train_X, train_y)
            self.calib_rf = CalibratedClassifierCV(self.rf, cv=3, method='sigmoid')
            self.calib_rf.fit(train_X, train_y)

            self.logger_object.log(self.file_object, f'RandomForest best parameters: {str(self.param_grid)}. Exited the get_best_params_RF method of Model_Finder class.')
            return self.calib_rf

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in fit_RF method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for RandomForest unsuccessful. Exited the fit_RF method of Model_Finder class.')
            raise Exception()

    def fit_LGBM(self, train_X, train_y):

        '''
        Gets the parameters for XGBoost Algorithm which give the best accuracy and saves the model using pickle
        Returns: None
        '''
        
        self.logger_object.log(self.file_object, 'Entered the fit_LGBM method of Model_Finder class.')
        try:
            self.param_grid = {'reg_lambda' : 1, 
                          'subsample' : 0.6, 
                          'colsample_bytree' : 1, 
                          'n_estimators':1200,
                          'num_leaves':50}

            self.lgbm = LGBMClassifier(**self.param_grid)
            self.lgbm.fit(train_X, train_y)
            self.calib_lgbm = CalibratedClassifierCV(self.lgbm, cv=3, method='sigmoid')
            self.calib_lgbm.fit(train_X, train_y)

            self.logger_object.log(self.file_object, f'LGBM best parameters: {str(self.param_grid)}. Exited the fit_XGB method of Model_Finder class.')
            
            return self.calib_lgbm

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in fit_LGBM method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for LGBM unsuccessful. Exited the fit_LGBM method of Model_Finder class.')
            raise Exception()

    def fit_NB(self, train_X, train_y):

        '''
        Fits the parameters for Gaussian Naive Bayes Algorithm which give the best accuracy and saves the model using pickle
        Returns: None
        '''

        self.logger_object.log(self.file_object, 'Entered the get_best_params_NB method of Model_Finder class.')
        try:
            self.param_grid = {'var_smoothing': 1.0}

            self.nb = GaussianNB(**self.param_grid)
            self.nb.fit(train_X, train_y)
            self.calib_nb = CalibratedClassifierCV(self.nb, cv=3, method='sigmoid')
            self.calib_nb.fit(train_X, train_y)

            self.logger_object.log(self.file_object, f'GaussianNB best parameters: {str(self.param_grid)}. Exited the fit_NB method of Model_Finder class.')
            
            return self.calib_nb

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in fit_NB method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for GaussianNB unsuccessful. Exited the fit_NB method of Model_Finder class.')
            raise Exception()

    
    def fit_MLP(self, train_X, train_y):

        '''
        Gets the parameters for XGBoost Algorithm which give the best accuracy and saves the model using pickle
        Returns: None
        '''

        self.logger_object.log(self.file_object, 'Entered the fit_mlp method of Model_Finder class.')
        try:
            self.param_grid = {'hidden_layer_sizes': 1000, 
                               'activation':'relu', 
                               'learning_rate_init':0.001,
                               'max_iter':500,
                               'n_iter_no_change':25,
                               'verbose':False}

            self.mlp = MLPClassifier(**self.param_grid)
            self.mlp.fit(train_X, train_y)
            self.calib_mlp = CalibratedClassifierCV(self.mlp, cv=3, method='sigmoid')
            self.calib_mlp.fit(train_X, train_y)

            self.logger_object.log(self.file_object, f'MLP best parameters: {str(self.param_grid)}. Exited the fit_MLP method of Model_Finder class.')
            
            return self.calib_mlp

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in fit_MLP method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for MLP unsuccessful. Exited the fit_XGB method of Model_Finder class.')
            raise Exception()

        
    def get_best_model(self,train_X, train_y, test_X, test_y):

        '''
        Finds the model which has the least cost
        Returns: Model object
        '''

        self.cost_dic = {}
        self.logger_object.log(self.file_object, 'Entered the get_best_model method of Model_Finder class.')

        def convert(arr):
            ls = []
            for _ in arr:
                if _ == False:
                    ls.append(-1)
                else:
                    ls.append(1)
            return np.array(ls)

        try:
            #LGBM
            self.lgbm = self.fit_LGBM(train_X, train_y)
            predicted_proba_lgbm = self.lgbm.predict_proba(test_X)
            cost_lgbm = {}
            for threshold in predicted_proba_lgbm[:,1]:
                y_predicted = convert(predicted_proba_lgbm[:,1] >= threshold)
                tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=y_predicted).ravel()
                cost_lgbm[threshold] = fn*500 + fp*10
            ls_lgbm = sorted(cost_lgbm.items(), key=lambda x: x[1])
            self.cost_dic['LGBM_Cost'] = [ls_lgbm[0][0], ls_lgbm[0][1]]
            self.logger_object.log(self.file_object, f'Threshold, Cost for LGBM: {ls_lgbm[0][0]}, ${str(ls_lgbm[0][1])}')
            
            #RandomForest
            self.rf = self.fit_RF(train_X, train_y)
            predicted_proba_rf = self.rf.predict_proba(test_X)
            cost_rf = {}
            for threshold in predicted_proba_rf[:,1]:
                y_predicted = convert(predicted_proba_rf[:,1] >= threshold)
                tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=y_predicted).ravel()
                cost_rf[threshold] = fn*500 + fp*10
            ls_rf = sorted(cost_rf.items(), key=lambda x: x[1])
            self.cost_dic['RandomForest_Cost'] = [ls_rf[0][0], ls_rf[0][1]]
            self.logger_object.log(self.file_object, f'Threshold, Cost for RandomForest: {ls_rf[0][0]}, ${str(ls_rf[0][1])}')
            
            #GaussianNB
            self.nb = self.fit_NB(train_X, train_y)
            predicted_proba_nb = self.nb.predict_proba(test_X)
            cost_nb = {}
            for threshold in predicted_proba_nb[:,1]:
                y_predicted = convert(predicted_proba_nb[:,1] >= threshold)
                tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=y_predicted).ravel()
                cost_nb[threshold] = fn*500 + fp*10
            ls_nb = sorted(cost_nb.items(), key=lambda x: x[1])

            self.cost_dic['NaiveBayes_Cost'] = [ls_nb[0][0], ls_nb[0][1]]
            self.logger_object.log(self.file_object, f'Threshold, Cost for GaussianNB: {ls_nb[0][0]} ${str(ls_nb[0][1])}')

            #Multilayer Perceptron
            self.mlp = self.fit_MLP(train_X, train_y)
            predicted_proba_mlp = self.mlp.predict_proba(test_X)
            cost_mlp = {}
            for threshold in predicted_proba_mlp[:,1]:
                y_predicted = convert(predicted_proba_mlp[:,1] >= threshold)
                tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=y_predicted).ravel()
                cost_mlp[threshold] = fn*500 + fp*10
            ls_mlp = sorted(cost_mlp.items(), key=lambda x: x[1])

            self.cost_dic['MLP_Cost'] = [ls_mlp[0][0], ls_mlp[0][1]]
            self.logger_object.log(self.file_object, f'Threshold, Cost for MLP: {ls_mlp[0][0]} ${str(ls_mlp[0][1])}')

            #Finding best among four
            ls = sorted(self.cost_dic.items(), key=lambda x: x[1][1])
            self.logger_object.log(self.file_object,'Model selection successful. Exited the get_best_model method of Model_Finder class.')
            
            if (ls[0][0] == 'RandomForest_Cost'):
                return 'RandomForest', self.rf, ls[0][1][0]
            
            if (ls[0][0] == 'LGBM_Cost'):
                return 'LGBM', self.lgbm, ls[0][1][0]

            if (ls[0][0] == 'NaiveBayes_Cost'):
                return 'GNB', self.nb, ls[0][1][0]

            if (ls[0][0] == 'MLP_Cost'):
                return 'MLP', self.mlp, ls[0][1][0]

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_best_model method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object,'Model selection failed. Exited the get_best_model method of Model_Finder class.')
            raise Exception()