#!/bin/bash

sudo apt-get install python3-pip
#downloads flet to system
pip3 install flet

wget https://github.com/paladinxb/RT_For_Linux/blob/main/test.py/
wget https://github.com/paladinxb/RT_For_Linux/blob/main/interface.py/
echo "Completed"
python3 /home/vadim/Загрузки/interface.py
