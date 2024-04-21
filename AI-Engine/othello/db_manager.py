import requests
import json


class DBManager:
    
    def __init__(self, host: str="db-manager", port: int=3001) -> None:
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