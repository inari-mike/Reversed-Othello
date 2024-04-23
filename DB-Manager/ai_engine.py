import requests
import os


class AIEngine:
    def __init__(self, host: str=None, port: int=3002) -> None:
        
        if host is None:
            ai_engine_domain = os.getenv("ai_engine_domain")
            if ai_engine_domain is None:
                host = "localhost"
            else:
                host = ai_engine_domain
                
        print("ai_engine_domain:", ai_engine_domain)
                
        self.uri = f"http://{host}:{port}"
        self.endpoints = {
            "create_agent": f"{self.uri}/create_agent"
        }

    def create_agent(self, state: str, time_limit:int=3000):
        """
        state: a string of json indicate the state of the game board
        wait_time: count in million second, the time limitation for agent
        """
        params = {
            "state": state,
            "time_limit": int(time_limit)
        }
        res = requests.get(
            self.endpoints["create_agent"],
            params=params            
        )
        return res