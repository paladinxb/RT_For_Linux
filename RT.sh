#!/bin/bash

# Установка зависимостей Python
sudo apt-get install python3-pip

# Установка зависимостей Python (если они есть)
pip3 install flet

wget https://github.com/paladinxb/RT_For_Linux/blob/main/test.py/
wget https://github.com/paladinxb/RT_For_Linux/blob/main/interface.py/
echo "Установка завершена"
python3 /home/vadim/Загрузки/interface.py
