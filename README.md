<h2> Air Pressure System Failure Detection </h2>

Dataset link: https://archive.ics.uci.edu/ml/datasets/APS+Failure+at+Scania+Trucks#

<h3> Problem Statement: </h3>
    
    The dataset consists of data collected from heavy Scania trucks in everyday usage. The system in focus is the Air Pressure system (APS) which generates pressurised
    air that are utilized in various functions in a truck, such as braking and gear changes. The datasets' positive class consists of component failures
    for a specific component of the APS system. The negative class consists of trucks with failures for components not related to the APS.
    
    The goal is to build a machine learning model which minimizes the total maintenance cost based on the inputs.
    There are two classes: pos and neg.
    pos: Consists of component failures for a specific component of the APS system
    neg: Consists of trucks with failures for components not related to the APS system.
    
<h3>Data Description </h3>
    
    The training data is divided into 6 different CSV files stored in folder named "training_batch_file", each having 10000 instances and 171 columns.        

<h3>Data Insertion in Database</h3>
     
     Database Creation and Connection: 
     Create a database with the given name passed. If the database is already created, open the connection to the database.
     
     Table creation in the database: 
     Table with name - "Raw_Data", is created in the database for inserting the training files in the "Training_file_from_DB" based on given column names and datatype. 
     If the table is already present, then the new table is not created and new files are inserted in the already present table as we want training to be done on new as well as old training files.
     
     Insertion of file in the table: 
     All the files in the "training_batch_file" are inserted in the above-created table.
     
<h3>Model Training</h3>
    
     Step 1 --> Data Export from DB:
     The data in a stored database is exported as a CSV file to the folder "training_file_from_DB" to be used for model training.
     
     Step 2 --> Data Preprocessing:
     Check for null values in the columns. If present, impute the null values using the median imputer.
     
     Step 3 --> Oversampling:
     Using Synthetic Minority Oversampling Technique (SMOTE) to handle the imbalanced class problem.
     
     Step 4 --> Clustering: 
     KMeans algorithm is used to create clusters in the preprocessed data. The optimum number of clusters is selected and best model is found cluster-wise.
     
<h3>Model Prediction</h3>
    
     Step 1 --> Data Export from DB:
     The data in a stored database is exported as a CSV file to the folder "prediction_file_from_DB" to be used for model training.
     
     Step 2 --> Data Preprocessing:
     Check for null values in the columns. If present, impute the null values using the median imputer.
          
     Step 3 --> Cluster-wise Prediction: 
     KMeans algorithm is used to create clusters in the testing data. The optimal model according to each cluster is used to make predictions.
     
<h3> Challlenge Metric </h3>

     Cost-metric of miss-classification:

     Predicted class |      True class       |
                     |    pos    |    neg    |
     -----------------------------------------
      pos            |     -     |  Cost_1   |
     -----------------------------------------
      neg            |  Cost_2   |     -     |
     -----------------------------------------
     
     Cost_1 = 10 and cost_2 = 500
  
     The total cost of a prediction model the sum of "Cost_1" multiplied by the number of Instances with type 1 failure and "Cost_2" with the number of instances with type 2 failure, 
     resulting in a "Total_cost".

     In this case Cost_1 refers to the cost that an unnessecary check needs to be done by an mechanic at an workshop, while Cost_2 refer to the cost of missing a faulty truck, 
     which may cause a breakdown.

     Total_cost = Cost_1*No_Instances + Cost_2*No_Instances.
