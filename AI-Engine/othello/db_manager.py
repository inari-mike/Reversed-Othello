import requests
import json
import os


class DBManager:
    
    def __init__(self, host: str=None, port: int=3001) -> None:
        
        if host is None:
            env_db_manager_domain = os.getenv("db_manager_domain")
            if env_db_manager_domain is None:
                host = "localhost"
            else:
                host = env_db_manager_domain

        print("env_db_manager_domain:", env_db_manager_domain)
                
        self.uri = f"http://{host}:{port}"
        self.endpoints = {
            "update_record": f"{self.uri}/update_record",
            "get_choice": f"{self.uri}/get_choice"
        }

    def hello(self):

        res = requests.get(
            f"{self.uri}/"
        )
        return res

    def update_record(self, hash_of_state: int | str, action: str):
        params = {
            "hash_of_state": str(hash_of_state),
            "action": action
        }
        res = requests.get(
            self.endpoints["update_record"],
            params=params            
        )
        return res
    
    
    def get_choice(self, state: str):
        """
        example get args:
        ?state=XO.X
        """
        params = {
            "state": state
        }

        res = requests.get(
            self.endpoints["get_choice"],
            params=params            
        )
        return res