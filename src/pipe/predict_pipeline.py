import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import requests

from src.utils import save_obj, load_object
from dataclasses import dataclass

@dataclass
class PredictionFileDetail:
    prediction_output_dirname: str = "predictions"
    prediction_file_name:str =  "predicted_file.csv"
    prediction_file_path:str = os.path.join(prediction_output_dirname,prediction_file_name)

class PredictPipelines:
    def __init__(self, request: request):
        self.request = request
        self.prediction_file_detail = PredictionFileDetail()

## ======================================================================================================================

    def save_prediction(self):
        try:
            pred_file_input_dir = "prediction_artifacts"
            os.makedirs(pred_file_input_dir, exist_ok=True)

            input_csv_file = self.request.files['file']
            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)
            
            
            input_csv_file.save(pred_file_path)


            return pred_file_path
        except Exception as e:
            raise CustomException(e,sys)

## ======================================================================================================================

    def predict(self, features):
        try:
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            mdoel_path = os.path.join("artifacts", "model.pkl")

            preprocessor = load_object(preprocessor_path)
            model = load_object(mdoel_path)

            data_scaled = preprocessor.transform(features)

            pred = model.predict(data_scaled)
            return pred

        except Exception as e:
            raise CustomException(e, sys)
        
## ======================================================================================================================

    def get_predicted_dataframe(self, input_dataframe_path: pd.DataFrame):
        try:
            prediction_column_name : str = "class"
            input_dataframe: pd.DataFrame = pd.read_csv(input_dataframe_path)
            predictions = self.predict(input_dataframe)
            input_dataframe[prediction_column_name] = [pred for pred in predictions]

            target_col_mapping = {0: "neg", 1:"pos"}

            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_col_mapping)

            os.makedirs( self.prediction_file_detail.prediction_output_dirname, exist_ok= True)
            input_dataframe.to_csv(self.prediction_file_detail.prediction_file_path, index= False)
            logging.info("predictions completed. ")

        except Exception as e:
            raise CustomException(e, sys)

## ======================================================================================================================
        
    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            self.get_predicted_dataframe(input_csv_path)

            return self.prediction_file_detail


        except Exception as e:
            raise CustomException(e,sys)
            