## APS FAILURE DETECTION

### Problem Statement

    The dataset consists of data collected from heavy Scania trucks in everyday usage. The system in focus is the Air Pressure system (APS) which generates   pressurised air that are utilized in various functions in a truck, such as braking and gear changes. 
    
    The +1 class consists of component failures for a specific component of the APS system. 
    The -1 class consists of trucks with failures for components not related to the APS. 
    
    The data consists of a subset of all available data, selected by experts.
    For a given problem, the cost of failing to detect the faulty part has 50 times the cost of doing pointless check on acceptable parts. The total  maintenance cost was calculated as sum of total cost required for misclassified trucks.

    Dataset link: https://archive.ics.uci.edu/ml/datasets/APS+Failure+at+Scania+Trucks

### Dataset Description

#### Training Files

    There are 6 .csv files in the training set, each file containing 10000 instances and 171 features.
    In total, there are 60000 instances out of which 59000 belong to the negative class and 1000 positive class.

#### Testing Files

    There is one .csv file containing 16000 instances and 171 features.
    
### Data Insertion in Database

     Database Creation and Connection: 
     Create a database with "Training_DB" name. If the database is already created, open the connection to the database.
 
     Table creation in the database: 
     Table with name - "Raw_Data", is created in the database for inserting the files in the "training_batch_file" based on  given column names and datatype. If the table is already present, then the new table is not created and new files are inserted in the already present table as we want training to be done on new as well as old training files.
 
     Insertion of file in the table: 
     All the files in the "training_batch_file" are inserted in the above-created table.

### Model Training

    Data Export from DB: 
    The data in a stored database is exported as a .csv file to be used for model training.
 
    Data Preprocessing: 
    Check for null values in the columns. If present, impute the null values using the KNN imputer.
    
    Clustering: 
    KMeans algorithm is used to create clusters in the preprocessed data. The optimum number of clusters 
    is selected
     
