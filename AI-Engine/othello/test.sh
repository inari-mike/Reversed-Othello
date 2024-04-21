#!bin/bash
python3 main.py random extra 1000
# Start searching with time limit of 1.0 seconds...
# X should always win
python3 main.py random minmax 4

python3 create_worker.py ...........................OX......XO........................... 5000