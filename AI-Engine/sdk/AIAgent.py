import requests


url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'somekey': 'somevalue'}

class AIAgent:
    def __init__(self, host: str="localhost", port: int=3002) -> None:
        self.uri = f"https://{host}:{port}"
        self.endpoints = {
            "create_agent": self.uri
        }

    def creat_agent(self, state: str, wait_time:int=1000):
        """
        state: a string of json indicate the state of the game board
        wait_time: count in million second, the time limitation for agent
        """
        res = requests.get()
        
x = requests.post(url, json = myobj)