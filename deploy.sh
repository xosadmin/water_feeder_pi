#!/bin/sh -e
pip install -r requirements.txt --break-system-packages
sudo pip install -r requirements.txt --break-system-packages
sudo mkdir -p /opt/app
sudo cp -r * /opt/app
sudo cp -r app.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl restart app
echo "Complete."