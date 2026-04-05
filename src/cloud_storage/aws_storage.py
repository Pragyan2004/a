import sys
import boto3
import pickle
import os
from src.exception import MyException


class SimpleStorageService:
    def __init__(self):
        try:
            self.s3_resource = boto3.resource('s3')
            self.s3_client = boto3.client('s3')
        except Exception as e:
            raise MyException(e, sys)

    def s3_key_path_available(self, bucket_name, s3_key):
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=s3_key)
            return True
        except Exception:
            return False

    def load_model(self, model_path, bucket_name):
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=model_path)
            model_content = response["Body"].read()
            model = pickle.loads(model_content)
            return model
        except Exception as e:
            raise MyException(e, sys)

    def upload_file(self, from_file, to_filename, bucket_name, remove=False):
        try:
            self.s3_client.upload_file(from_file, bucket_name, to_filename)
            if remove:
                os.remove(from_file)
        except Exception as e:
            raise MyException(e, sys)