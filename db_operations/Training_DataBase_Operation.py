import sqlite3
from os import listdir
import os
import csv
from application_logging.logger import App_Logger

class DBOperation:

    '''
    Performs various operations on SQLite DataBase
    
    Attributes:
    1. DB_Connection
    2. create_table
    3. insert_into_table
    4. ExportDB_to_CSV
    '''

    def __init__(self):
        self.path = 'training_DB'
        self.FilePath = 'training_processed_batch_files/'
        self.logger = App_Logger()

    def DB_Connection(self, DB_Name):

        '''
        Opens the connection to the DataBase
        Returns: SQLite Connection
        '''

        try:

            myDB_connection = sqlite3.connect(self.path+'\\'+DB_Name+'.db')
            file = open(r'training_logs\DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, f'Opened {DB_Name} successfully.')
            file.close()

        except Exception as e:
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, f'Exception occurred in connecting to the database. Exception: {e}')
            file.close()
            raise Exception()
        
        return myDB_connection

    def create_table(self, DB_Name):

        '''
        Creates a table in the given DataBase 
        Returns: None
        '''

        self.columns = {'Idx': 'VARCHAR(10)','class': 'VARCHAR(20)','aa_000': 'VARCHAR(20)','ab_000': 'VARCHAR(20)','ac_000': 'VARCHAR(20)','ad_000': 'VARCHAR(20)','ae_000': 'VARCHAR(20)','af_000': 'VARCHAR(20)','ag_000': 'VARCHAR(20)','ag_001': 'VARCHAR(20)','ag_002': 'VARCHAR(20)','ag_003': 'VARCHAR(20)','ag_004': 'VARCHAR(20)','ag_005': 'VARCHAR(20)','ag_006': 'VARCHAR(20)','ag_007': 'VARCHAR(20)','ag_008': 'VARCHAR(20)','ag_009': 'VARCHAR(20)',
 'ah_000': 'VARCHAR(20)','ai_000': 'VARCHAR(20)','aj_000': 'VARCHAR(20)','ak_000': 'VARCHAR(20)','al_000': 'VARCHAR(20)','am_0': 'VARCHAR(20)','an_000': 'VARCHAR(20)','ao_000': 'VARCHAR(20)','ap_000': 'VARCHAR(20)','aq_000': 'VARCHAR(20)','ar_000': 'VARCHAR(20)','as_000': 'VARCHAR(20)','at_000': 'VARCHAR(20)','au_000': 'VARCHAR(20)','av_000': 'VARCHAR(20)','ax_000': 'VARCHAR(20)','ay_000': 'VARCHAR(20)','ay_001': 'VARCHAR(20)','ay_002': 'VARCHAR(20)','ay_003': 'VARCHAR(20)','ay_004': 'VARCHAR(20)','ay_005': 'VARCHAR(20)',
 'ay_006': 'VARCHAR(20)','ay_007': 'VARCHAR(20)','ay_008': 'VARCHAR(20)','ay_009': 'VARCHAR(20)','az_000': 'VARCHAR(20)','az_001': 'VARCHAR(20)','az_002': 'VARCHAR(20)','az_003': 'VARCHAR(20)','az_004': 'VARCHAR(20)','az_005': 'VARCHAR(20)','az_006': 'VARCHAR(20)','az_007': 'VARCHAR(20)','az_008': 'VARCHAR(20)','az_009': 'VARCHAR(20)','ba_000': 'VARCHAR(20)','ba_001': 'VARCHAR(20)','ba_002': 'VARCHAR(20)','ba_003': 'VARCHAR(20)','ba_004': 'VARCHAR(20)','ba_005': 'VARCHAR(20)','ba_006': 'VARCHAR(20)','ba_007': 'VARCHAR(20)',
 'ba_008': 'VARCHAR(20)','ba_009': 'VARCHAR(20)','bb_000': 'VARCHAR(20)','bc_000': 'VARCHAR(20)','bd_000': 'VARCHAR(20)','be_000': 'VARCHAR(20)','bf_000': 'VARCHAR(20)','bg_000': 'VARCHAR(20)','bh_000': 'VARCHAR(20)','bi_000': 'VARCHAR(20)','bj_000': 'VARCHAR(20)','bk_000': 'VARCHAR(20)','bl_000': 'VARCHAR(20)','bm_000': 'VARCHAR(20)','bn_000': 'VARCHAR(20)','bo_000': 'VARCHAR(20)','bp_000': 'VARCHAR(20)','bq_000': 'VARCHAR(20)','br_000': 'VARCHAR(20)','bs_000': 'VARCHAR(20)','bt_000': 'VARCHAR(20)','bu_000': 'VARCHAR(20)',
 'bv_000': 'VARCHAR(20)','bx_000': 'VARCHAR(20)','by_000': 'VARCHAR(20)','bz_000': 'VARCHAR(20)','ca_000': 'VARCHAR(20)','cb_000': 'VARCHAR(20)','cc_000': 'VARCHAR(20)','cd_000': 'VARCHAR(20)','ce_000': 'VARCHAR(20)','cf_000': 'VARCHAR(20)','cg_000': 'VARCHAR(20)','ch_000': 'VARCHAR(20)','ci_000': 'VARCHAR(20)','cj_000': 'VARCHAR(20)','ck_000': 'VARCHAR(20)','cl_000': 'VARCHAR(20)','cm_000': 'VARCHAR(20)','cn_000': 'VARCHAR(20)','cn_001': 'VARCHAR(20)','cn_002': 'VARCHAR(20)','cn_003': 'VARCHAR(20)','cn_004': 'VARCHAR(20)',
 'cn_005': 'VARCHAR(20)','cn_006': 'VARCHAR(20)','cn_007': 'VARCHAR(20)','cn_008': 'VARCHAR(20)','cn_009': 'VARCHAR(20)','co_000': 'VARCHAR(20)','cp_000': 'VARCHAR(20)','cq_000': 'VARCHAR(20)','cr_000': 'VARCHAR(20)','cs_000': 'VARCHAR(20)','cs_001': 'VARCHAR(20)','cs_002': 'VARCHAR(20)','cs_003': 'VARCHAR(20)','cs_004': 'VARCHAR(20)','cs_005': 'VARCHAR(20)','cs_006': 'VARCHAR(20)','cs_007': 'VARCHAR(20)','cs_008': 'VARCHAR(20)','cs_009': 'VARCHAR(20)','ct_000': 'VARCHAR(20)','cu_000': 'VARCHAR(20)','cv_000': 'VARCHAR(20)',
 'cx_000': 'VARCHAR(20)','cy_000': 'VARCHAR(20)','cz_000': 'VARCHAR(20)','da_000': 'VARCHAR(20)','db_000': 'VARCHAR(20)','dc_000': 'VARCHAR(20)','dd_000': 'VARCHAR(20)','de_000': 'VARCHAR(20)','df_000': 'VARCHAR(20)','dg_000': 'VARCHAR(20)','dh_000': 'VARCHAR(20)','di_000': 'VARCHAR(20)','dj_000': 'VARCHAR(20)','dk_000': 'VARCHAR(20)','dl_000': 'VARCHAR(20)','dm_000': 'VARCHAR(20)','dn_000': 'VARCHAR(20)','do_000': 'VARCHAR(20)','dp_000': 'VARCHAR(20)','dq_000': 'VARCHAR(20)','dr_000': 'VARCHAR(20)','ds_000': 'VARCHAR(20)',
 'dt_000': 'VARCHAR(20)','du_000': 'VARCHAR(20)','dv_000': 'VARCHAR(20)','dx_000': 'VARCHAR(20)','dy_000': 'VARCHAR(20)','dz_000': 'VARCHAR(20)','ea_000': 'VARCHAR(20)','eb_000': 'VARCHAR(20)','ec_00': 'VARCHAR(20)','ed_000': 'VARCHAR(20)','ee_000': 'VARCHAR(20)','ee_001': 'VARCHAR(20)','ee_002': 'VARCHAR(20)','ee_003': 'VARCHAR(20)','ee_004': 'VARCHAR(20)','ee_005': 'VARCHAR(20)','ee_006': 'VARCHAR(20)','ee_007': 'VARCHAR(20)','ee_008': 'VARCHAR(20)','ee_009': 'VARCHAR(20)','ef_000': 'VARCHAR(20)','eg_000': 'VARCHAR(20)'}
        
        try:
            myDB_connection = self.DB_Connection(DB_Name)
            cursor = myDB_connection.cursor()

            for key in self.columns.keys():
                val = self.columns[key]

                # in try block we check if the table exists, if yes then add columns to the table else in catch block we will create the table
                try:
                    cursor.execute(f'ALTER TABLE Raw_Data ADD COLUMN {key} {val}')
                except:
                    cursor.execute(f'CREATE TABLE Raw_Data ({key} {val})')

            cursor.close()

            file = open("training_logs/DataBaseCreateTableLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully.")
            file.close() 

            file = open("training_logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, f"Closed {DB_Name} database successfully.")
            file.close()   

        except Exception as e:
            file = open("training_logs/DataBaseCreateTableLog.txt", 'a+')
            self.logger.log(file, f"Exception occurred in creating table. Exception: {e}")
            file.close() 
            cursor.close()

            file = open("training_logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, f"Closed {DB_Name} database successfully.")
            file.close()   
            raise Exception()

    def insert_into_table(self, DB_Name):
    
        '''
        Inserts the data from training files into the previously created table
        Returns: None
        '''

        myDB_connection = self.DB_Connection(DB_Name)
        cursor = myDB_connection.cursor()
        file_path = self.FilePath
        files = [file for file in listdir(file_path)]
        logfile = open('training_logs/DataBaseInsertLog.txt', 'a+')

        for file in files:
            try:
                with open(file_path+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                cursor.execute(f'INSERT INTO Raw_Data values ({list_})')
                                self.logger.log(logfile,f"{file}: File loaded successfully.")
                                myDB_connection.commit()
                            except Exception as e:
                                self.logger.log(logfile, f'Exception: {e}')
                                raise Exception()
            
            except Exception as e:
                myDB_connection.rollback()
                self.logger.log(logfile, f'Exception occurred in creating table. Exception: {e}')
                logfile.close()
                myDB_connection.close()

        myDB_connection.close()
        logfile.close()

    def ExportDB_to_CSV(self, DB_Name):

        '''
        Exports the data in the table as a CSV file in a given location above created.
        Returns: None
        '''

        self.file_from_DB = 'training_file_from_DB/'
        self.file_name = 'aps_training_set.csv'
        logfile = open('training_logs/ExportDBToCSVLog.txt', 'a+')
        try:
            myDB_connection = self.DB_Connection(DB_Name)
            cursor = myDB_connection.cursor()
            cursor.execute("SELECT *  FROM Raw_Data")
            result = cursor.fetchall()
            
            # Get the headers of the csv file
            column_names = [i[0] for i in cursor.description]


            #Make the CSV ouput directory
            if not os.path.isdir(self.file_from_DB):
                os.makedirs(self.file_from_DB)

            # Open CSV file for writing.
            file = open(self.file_from_DB + self.file_name, 'w')
            csvFile = csv.writer(file,lineterminator='\n')

            # Add the headers and data to the CSV file.
            csvFile.writerow(column_names)
            csvFile.writerows(result)
            file.close()

            self.logger.log(logfile, "File exported successfully.")
            logfile.close()

        except Exception as e:
            self.logger.log(logfile, f'Exception occurred in exporting file. Exception: {e}')
            logfile.close()