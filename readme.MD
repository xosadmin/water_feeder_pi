### water_feeder_pi
  
This is a client program that run on Raspberry Pi in smart water feeder.  
   
#### How to deploy this program?
   
Two ways: Use one-key installer or deploy it manually.
   
I: Use One-key installer (Recommended)
1. Clone this project to Raspberry Pi
2. Start the installer via ``bash deploy.sh``
3. Wait until finished
4. Enjoy~
  
II: Manually deploy
1. Clone this project to Raspberry Pi
2. Change the project location in app.services
3. Move app.services to /etc/systemd/system
4. Install dependencies via ``pip install -r requirements.txt`` (some of system requires --break-system-packages)
5. Execute command ``sudo systemctl daemon-reload``
6. Execute command ``sudo systemctl start app``
  
If you have any issue, please raise your discussion.
