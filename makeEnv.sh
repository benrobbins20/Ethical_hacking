#!/usr/bin/sh
python3 -m venv Ethical_hacking_venv
source Ethical_hacking_venv/bin/activate
apt update 
apt install build-essential libnetfilter-queue-dev
pip3 install -r requirements.txt
