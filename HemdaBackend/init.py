from paramModel import GeneralModel,SystemModel,ParamsModel
import json
from database import *

class MainInit:
    def __init__(self):
        self.paramsFile = r"D:\learn\chemdaBackend\params.json"
        self.params = self.load_params_from_json(self.paramsFile)
        self.conn = get_db_connection(self.params.system.postgresql)
        pass

    def __enter__(self):
        # the enter auto call when it calls with "with".
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load_params_from_json(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                raw_params = json.load(file)
                generalModel = GeneralModel(**raw_params.get("general", {}))
                systemlModel = SystemModel(**raw_params.get("system", {}))
                paramsModel = ParamsModel(generalModel, systemlModel)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f" Error reading param file: {e}")
            raise
        except Exception  as e:
            print(f"Unexpected error occurred: {e}")
            raise
        return paramsModel
