#!/bin/bash
echo "ESPERANDO SCRIPT!!!"
sleep 6s
echo "RETOMANDO SCRIPT!!!"
cd /home/pi/dermyah_service
echo "DIRETORIO"
source venv/bin/activate
echo "VENV"
sleep 3s
echo "RUNSERVER"
#python3 manage.py runserver dermyah.local:8000 --noreload ANTIGOOOO
sudo python3 manage.py runserver --insecure dermyah.local:80 --noreload
echo "INICIADO EBAAA"
exit 0
