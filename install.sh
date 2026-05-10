#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip git curl tor
pip3 install PySocks
pip3 install requests[socks] proxy-rotator
pip3 install requests fake-useragent beautifulsoup4
sudo systemctl enable tor
sudo systemctl start tor
