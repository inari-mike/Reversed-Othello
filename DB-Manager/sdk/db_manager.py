import requests


class DBManager:
    def __init__(self, host: str="localhost", port: int=3001) -> None:
        self.uri = f"http://{host}:{port}"
        self.endpoints = {
            "update_record": f"{self.uri}/update_record"
        }

    def update_record(self, hash_of_state: int, action: list[int]):

        res = requests.post(
            self.endpoints["update_record"],
            data = {
                "hash_of_state": hash_of_state,
                "action": action
            }
        )
        return res