#!/bin/bash
cd /home/marsboard/PiMonitor

while true
do
sudo PYTHONPATH=. python2.7 /home/marsboard/PiMonitor/pimonitor/PMDial.py $1
sleep 1
done
