from flask import Flask, request, jsonify
from redis_util import Redis


app = Flask(__name__)
redis_handler = Redis()

@app.route('/')
def hello():
    return 'Hello, this is DB-Manager!'

# F5
@app.route('/update_record', methods=['POST'])  
def update_record():
    """
    example post content:
    '{"hash_of_state": -7689071305868051212, "action": null}'
    """
    hash_action = request.get_json()
    print(hash_action)
    hash_of_state = hash_action["hash_of_state"]
    action = hash_action["action"]
    redis_handler.update_record(hash_of_state, action)
    return jsonify(200, "update record success!")
















# @app.route('/create_agent', methods=['POST'])  
# def create_agent():

#     state = request.json.get('state')
#     wait_time = request.json.get('wait_time')
    
#     # check
#     if not state or not wait_time:
#         return jsonify({'error': 'Missing required parameters'})
#     # connection
#     r = get_redis_connection()
#     if r.set(state, wait_time):
#         return jsonify({'New Agent has been created!'})
#     else:
#         return jsonify({'error': 'Failed to create agent in Redis'})
#     '''check 200/500/404'''

# ''' docker exec -it redis-test redis-cli'''



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=True)


