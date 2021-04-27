#!/bin/sh
# File name: launcher.sh
# Description: run at startup, check the internet, then execute python script
# Set up: $ nano launcher.sh
#         $ chmod 755 launcher.sh
#         $ mkdir logs
#         $ sudo crontab -e
#         $ @reboot sh /home/pi/launch.sh >/home/pi/logs/cronlog 2>&1

echo "Hello launcher.sh"
while true; do
	ping -c 1 8.8.8.8

	if [ $? -eq 0 ]; then
		echo "Connected to Internet"
		break
	fi
	echo "waiting for network"
	sleep 2
done

sudo python3 /home/pi/crawlerTwitch.py &
sudo python3 /home/pi/crawlerYoutube.py
#sudo python3 /home/pi/crawlerYoutube.py >/home/pi/logs/crawlerYoutubeLog 2>&1

#https://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/