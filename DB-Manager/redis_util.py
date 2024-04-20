import json
from datetime import datetime
import redis

"""
An example of key-value pairs in our DB:

key(hash of state):
3331931248134196401

value(a json string):
'{"action": [1, 1], "expire_timestamp": 1713650515}'

or
'{"action": null, "expire_timestamp": 1713650515}'

"""

class Redis:

    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses


    def get_redis_connection(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses
        )


    def create_record(self, hash_of_state: int, wait_time: int) -> None:
        """wait_time: count in second"""
        current_timestamp = int(datetime.now().timestamp())
        expire_timestamp: int = current_timestamp + wait_time
        record_str: str = json.dumps(
            {
                "action": None,
                "expire_timestamp": expire_timestamp
            }
        )
        r = self.get_redis_connection()
        r.set(hash_of_state, record_str)

    def get_record(self, hash_of_state: int) -> dict:
        r = self.get_redis_connection()
        record_str: str = r.get(hash_of_state)
        record: dict = json.loads(record_str)
        return record


    def update_record(self, hash_of_state: int, action: list[int]):
        record = self.get_record(hash_of_state)
        record["action"] = action
        record_str: str = json.dumps(record)
        r = self.get_redis_connection()
        r.set(hash_of_state, record_str)
        