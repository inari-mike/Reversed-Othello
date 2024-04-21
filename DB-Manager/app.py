from flask import Flask, request, jsonify
from redis_util import Redis
import hashlib
from ai_engine import AIEngine
from datetime import datetime

app = Flask(__name__)
redis_handler = Redis() # ATTENTION: no arg for docker compose

ai_handler = AIEngine(port=3002)
time_limit_default = 3000 # 3 sec, 3000 million sec
extra_wait_time = 1000 # 1 sec, 1000 million sec, in case of network issue

@app.route('/')
def hello():
    return 'Hello, this is DB-Manager!'


@app.route('/get_choice', methods=['GET'])
def get_choice():
    """
    example get args:
    ?state=XO.X
    """
    # print("hit get_choice!!!")
    state = request.args.get('state')
    # hash_of_state = hash(state) # TODO
    hash_of_state = hashlib.sha256(state.encode('ascii')).hexdigest()
    # print(state)
    # print(hash_of_state)

    record = redis_handler.get_record(hash_of_state)
    current_timestamp = int(datetime.now().timestamp())
    
    if record is None:
        
        # print("record is None:", record)
        # TODO here call create agent
        # create new agent
        ai_handler.create_agent(
            state=state,
            time_limit=time_limit_default
        )
                
        redis_handler.create_record(
            hash_of_state=hash_of_state,
            wait_time=time_limit_default + extra_wait_time
        )
        
        expire_timestamp = current_timestamp + time_limit_default + extra_wait_time
        
        res =  jsonify(200, "please wait(0)", expire_timestamp)
    
    else:
        
        print("record is dict:", record)
        
        if record["action"] is None:
            expire_timestamp = int(record["expire_timestamp"])
            
            if current_timestamp > expire_timestamp: # over due
                res =  jsonify(200, "please wait(1)", expire_timestamp)
                
            else:
                # create new agent
                ai_handler.create_agent(
                    state=state,
                    time_limit=time_limit_default
                )
                res = jsonify(200, "please wait(2)", expire_timestamp)
            
        else:
            res = jsonify(200, record["action"])

    res.headers.add('Access-Control-Allow-Origin', '*') # disable CORs
    return res
    


@app.route('/update_record', methods=['GET'])
def update_record():
    """
    example get args:
    ?hash_of_state=-7689071305868051212&action=1,0
    """
    print("hit update_record!!!")
    hash_of_state = request.args.get('hash_of_state')
    action = request.args.get('action')
    print(hash_of_state, action)
    redis_handler.update_record(hash_of_state, action)
    return jsonify(200, "update record success!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=True)
