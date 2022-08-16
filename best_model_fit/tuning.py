import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_auc_score, accuracy_score,confusion_matrix
from sklearn.model_selection import GridSearchCV


class Model_Finder:

    '''
    Finds the model with best accuracy and AUC score

    Attributes:
    1. get_best_params_RF
    2. get_best_params_XGB
    3. get_best_params_NB
    4. get_best_model

    '''

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        self.nb = GaussianNB()

    def get_best_params_RF(self, train_X, train_y):

        '''
        Gets the parameters for RandomForest Algorithm which give the best accuracy using Hyper Parameter Tuning.
        Returns: RandomForestClassifier object
        '''

        self.logger_object.log(self.file_object, 'Entered the get_best_params_RF method of Model_Finder class.')
        
        try:
            self.param_grid = {'n_estimators':[800],
              'max_depth':[13],
              'min_samples_split':[12],
              'max_leaf_nodes':[300],
              'ccp_alpha':[0.01],
              'criterion': ['gini']}

            self.model = GridSearchCV(estimator=self.rf,param_grid=self.param_grid,cv=5,verbose=3)
            self.model.fit(train_X, train_y)
            self.best_params = self.model.best_params_

            self.rf = RandomForestClassifier(**self.best_params)
            self.rf.fit(train_X, train_y)
            self.logger_object.log(self.file_object, f'RandomForest best parameters: {str(self.model.best_params_)}. Exited the get_best_params_RF method of Model_Finder class.')
            return self.rf
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_best_params_RF method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for RandomForest unsuccessful. Exited the get_best_params_RF method of Model_Finder class.')
            raise Exception()

    def get_best_params_XGB(self, train_X, train_y):

        '''
        Gets the parameters for XGBoost Algorithm which give the best accuracy using Hyper Parameter Tuning
        Returns: XGBClassifier object
        '''

        self.logger_object.log(self.file_object, 'Entered the get_best_params_XGB method of Model_Finder class.')
        try:
            self.param_grid = {'reg_lambda' : [1],
                               'eta' : [0.05], 
                               'subsample' : [0.6], 
                               'colsample_bytree' : [1],
                               'scale_pos_weight':[1/59]}

            self.model = GridSearchCV(estimator=self.xgb,param_grid=self.param_grid,cv=5,verbose=3)
            self.model.fit(train_X, train_y)
            self.best_params = self.model.best_params_

            self.xgb = XGBClassifier(**self.best_params)
            self.xgb.fit(train_X, train_y)
            self.logger_object.log(self.file_object, f'XGBoost best parameters: {str(self.model.best_params_)}. Exited the get_best_params_XGB method of Model_Finder class.')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_best_params_XGB method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for XGBoost unsuccessful. Exited the get_best_params_XGB method of Model_Finder class.')
            raise Exception()

    def get_best_params_NB(self, train_X, train_y):

        '''
        Gets the parameters for XGBoost Algorithm which give the best accuracy using Hyper Parameter Tuning
        Returns: GaussianNB object
        '''

        self.logger_object.log(self.file_object, 'Entered the get_best_params_NB method of Model_Finder class.')
        try:
            params_NB = {'var_smoothing': np.logspace(0,-9, num=10)}
            self.model = GridSearchCV(estimator=self.nb,cv=5,verbose=3, param_grid = params_NB)
            self.model.fit(train_X, train_y)
            self.best_params = self.model.best_params_

            self.nb = GaussianNB(**self.best_params)
            self.nb.fit(train_X, train_y)
            self.logger_object.log(self.file_object, f'GaussianNB best parameters: {str(self.model.best_params_)}. Exited the get_best_params_NB method of Model_Finder class.')
            return self.nb
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_best_params_NB method of Model_Finder class. Exception: {e}')
            self.logger_object.log(self.file_object, 'Finding best parameters for GaussianNB unsuccessful. Exited the get_best_params_NB method of Model_Finder class.')
            raise Exception()
        
    def get_best_model(self, train_X, test_X, train_y, test_y):

        '''
        Finds the model which has the best AUC score.
        Returns: Model object
        '''

        self.logger_object.log(self.file_object, 'Entered the get_best_model method of Model_Finder class.')
        try:
            #XGBoost 
            self.xgb = self.get_best_params_XGB(train_X, train_y)
            self.pred_xgb = self.xgb.predict(test_X)
            tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=self.pred_xgb).ravel()
            self.xgb_score = fn*500 + fp*10
            self.logger_object.log(self.file_object, f'Cost for XGBoost: ${str(self.xgb_score)}')
            
            #RandomForest
            self.rf = self.get_best_params_RF(train_X, train_y)
            self.pred_rf = self.rf.predict(test_X)
            tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=self.pred_rf).ravel()
            self.rf_score = fn*500 + fp*10
            self.logger_object.log(self.file_object, f'Cost for RandomForest: ${str(self.rf_score)}')
            
            #GaussianNB
            self.nb = self.get_best_params_NB(train_X, train_y)
            self.pred_nb = self.nb.predict(test_X)
            tn, fp, fn, tp = confusion_matrix(y_true=test_y, y_pred=self.pred_nb).ravel()
            self.nb_score = fn*500 + fp*10
            self.logger_object.log(self.file_object, f'Cost for GaussianNB: ${str(self.nb_score)}')
            
            self.logger_object.log(self.file_object,'Model selection successful. Exited the get_best_model method of Model_Finder class.')

            #Finding best among three
            if (self.xgb_score <= self.rf_score) and (self.xgb_score <= self.nb_score):
                return 'XGBoost',self.xgb
            elif (self.rf_score <= self.xgb_score) and (self.rf_score <= self.nb_score):
                return 'RandomForest',self.rf
            else:
                return 'GaussianNB',self.nb
            
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in get_best_model method of Model_Finder class.')
            self.logger_object.log(self.file_object,'Model selection failed. Exited the get_best_model method of Model_Finder class.')
            raise Exception()