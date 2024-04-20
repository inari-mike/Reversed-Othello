import requests


class AIEngine:
    def __init__(self, host: str="localhost", port: int=3002) -> None:
        self.uri = f"http://{host}:{port}"
        self.endpoints = {
            "create_agent": f"{self.uri}/create_agent"
        }

    def create_agent(self, state: str, wait_time:int=1000):
        """
        state: a string of json indicate the state of the game board
        wait_time: count in million second, the time limitation for agent
        """
        res = requests.get(self.endpoints["create_agent"]) # async: no wait
        return res