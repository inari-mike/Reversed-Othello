from flask import Flask, request, jsonify
from redis_util import Redis
import hashlib

app = Flask(__name__)
redis_handler = Redis()
wait_time_default = 1000 # million sec


@app.route('/')
def hello():
    return 'Hello, this is DB-Manager!'


@app.route('/get_choice', methods=['GET'])
def get_choice():
    """
    example get args:
    ?state=XO.X
    """
    print("hit get_choice!!!")
    state = request.args.get('state')
    # hash_of_state = hash(state) # TODO
    hash_of_state = hashlib.sha256(state.encode('ascii')).hexdigest()
    print(state)
    print(hash_of_state)

    record = redis_handler.get_record(hash_of_state)

    if record is dict:
        return jsonify(200, record["action"])
    
    else:
        # TODO here call create agent
        redis_handler.create_record(
            hash_of_state=hash_of_state,
            wait_time=wait_time_default
        )
        return jsonify(200, "please wait")


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
