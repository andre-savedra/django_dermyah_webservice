#!/bin/bash
cd /home/pi/klipper
sudo service klipper stop
make flash FLASH_DEVICE=$1
sudo service klipper start

echo "FLASH_DEVICE=$1"
exit 0
