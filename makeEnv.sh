#!/usr/bin/sh
git clone https://github.com/benrobbins20/Ethical_hacking.git
python3 -m venv Ethical_hacking/Ethical_hacking_venv
source Ethical_hacking/Ethical_hacking_venv/bin/activate
apt update 
apt install build-essential libnetfilter-queue-dev
pip3 install -r requirements.txt
