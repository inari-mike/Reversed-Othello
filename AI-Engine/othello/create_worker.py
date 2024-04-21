import sys
import othello
import agent
from db_manager import DBManager
import hashlib
import json


if __name__ == '__main__':

    assert len(sys.argv) == 3, "usage: create_worker [string of game state] [time limitation in sec]"
    game_state_str = sys.argv[1]
    
    assert len(game_state_str) == 64, "len(game_state_str) != 64"
    game_state = othello.State(
        board=[
                [
                    othello.PLAYER_NAMES.index(
                        game_state_str[8 * row + column]
                    ) for column in range(8)
                ] for row in range(8)
            ],
        boardSize=8,
        nextPlayerToMove=othello.PLAYER1 # AI always play O
    )
    print("Current game state:")
    print(game_state)
    print("Available Moves:")
    i = 0
    for move in game_state.generateMoves():
        i = i + 1
        print(f"{i}. {str(move)}")
    print(f"there are {i} available moves.")
    print("Start Searching...\r")

    time_limit = int(sys.argv[2])
    agent_time_limited = agent.extra(time_limit)
    best_move:othello.OthelloMove = agent_time_limited.choose_move(game_state)
    best_move_str = f"{best_move.x},{best_move.y}"
    # print("best_move_str:", best_move_str)

    # call DB Manager
    dm = DBManager(host="localhost") # TODO
    hash_of_state = hashlib.sha256(game_state_str.encode('ascii')).hexdigest()
    
    try:
        res = dm.update_record(hash_of_state=hash_of_state, action=best_move_str)
        # print(type(res.content), res.content)
        res = json.loads(res.content)
        if res[0] == 200:
            print("Upate best move to database success.")
        else:
            print("Upate best move to database fail!")
    except:
        print("Upate best move to database fail!")
    # TODO: error handling