# from network_security.entity.artifact_entity import
from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file
from scipy.stats import ks_2samp
import os
import sys
import pandas as pd

"""
In DataValidation:
Input: DataIngestionArtifact
Output: DataValidationArtifact
DataIngestionArtifact -> DataValidationConfig -> DataValidation -> DataValidationArtifact
"""

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Dataframe has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n" 
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message= f"Test dataframe does not contain all columns.\n"
            expected_numerical_columns = set(self._schema_config["numerical_columns"])
            train_columns = set(train_dataframe.columns)

            missing_columns = expected_numerical_columns - train_columns
            if missing_columns:
                raise NetworkSecurityException(
                    f"The following numerical columns are missing in the training data: {missing_columns}",
                    sys
                )
            expected_numerical_columns = set(self._schema_config["numerical_columns"])
            test_columns = set(test_dataframe.columns)

            missing_columns = expected_numerical_columns - test_columns
            if missing_columns:
                raise NetworkSecurityException(
                    f"The following numerical columns are missing in the testing data: {missing_columns}",
                    sys
                )

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        