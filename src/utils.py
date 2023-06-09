import os, sys
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException

from pymongo import MongoClient


def export_collection_as_dataframe(collection_name, db_name):
    try:
        mongo_client = MongoClient(os.getenv("mongodb+srv://mohanty:RAM@cluster0.1owxeev.mongodb.net/?retryWrites=true&w=majority"))

        collection = mongo_client[db_name][collection_name]

        df = pd.DataFrame(list(collection.find()))

        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"], axis=1)

        df.replace({"na": np.nan}, inplace=True)

        return df

    except Exception as e:
        raise CustomException(e, sys)