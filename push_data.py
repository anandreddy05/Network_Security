import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def csv_to_json_convertor(self,file_path:Path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_in_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
if __name__ == "__main__":
    FILE_PATH="./Network_Data/phisingData.csv"
    DATABASE="ANAND_AI"
    COLLECTION="NetworkData"
    network_obj=NetworkDataExtract()
    RECORDS = network_obj.csv_to_json_convertor(file_path=FILE_PATH)
    no_of_records=network_obj.insert_data_in_mongodb(RECORDS,DATABASE,COLLECTION)
    print(f"No of Records: {no_of_records}")