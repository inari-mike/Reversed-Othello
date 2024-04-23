#!/bin/sh
# This script is only for hosting the instance on aws, not for local deployment

# sudo git clone https://github.com/inari-mike/Reversed-Othello.git &&

# sudo snap install docker &&

# cd Reversed-Othello &&

# When run on aws, we need to pass our public IP to React frontend
sudo echo export const backend_domain=\"$(dig +short myip.opendns.com @resolver1.opendns.com)\" > Frontend/src/env.js &&

cd Docker &&

sudo docker compose up
