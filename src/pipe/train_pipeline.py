import sys, os
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transform import DataTransformation
from src.components.data_modeling import ModelTrainig

if __name__ == "__main__":
    ## Data Ingestion Time
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestioin()
    print(train_data_path, test_data_path)

    ## Data Transformation Time
    data_trans = DataTransformation()
    train_arr, test_arr, obj_path = data_trans.initiate_data_transformation_obj(train_data_path, test_data_path)

    ## Data Modelling Time
    modelling = ModelTrainig()
    modelling.initiate_model_training(train_arr, test_arr)