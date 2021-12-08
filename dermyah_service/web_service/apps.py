
from django.apps import AppConfig


from threading import Timer

import http.client as httplib

import subprocess
import os

import requests

from web_service import messager

tentativas = 0

#botao de reset:
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BOARD)
resetbutton = 16
GPIO.setup (resetbutton,GPIO.IN, pull_up_down=GPIO.PUD_UP)
tentativasIOreset = 0



def change_access():
    
    print("CHANGE TO ACCESS POINT!!!")
    r = subprocess.check_output('sudo systemctl enable hostapd dnsmasq', shell=True)
    r = subprocess.check_output('sudo cp -f /etc/dhcp_change/local/dhcpcd.conf /etc/', shell=True)
    
    r = subprocess.check_output('wpa_cli remove_network 0', shell=True)    
    r = subprocess.check_output('wpa_cli remove_network 1', shell=True)
    r = subprocess.check_output('wpa_cli save_config', shell=True)
    
    messager.message1 = "Reinicie a maquina,"
    messager.message2 = "wifi Local ativado"
    #os.system('sudo reboot')

def set_tentativa(value):    
    global tentativas

    if(value == 0):
        tentativas = 0
    else:    
        tentativas += value
    return tentativas


def setInterval(function, interval, *params, **kwparams):
    
    def setTimer(wrapper):
        wrapper.timer = Timer(interval, wrapper)
        wrapper.timer.start()

    def wrapper():
        function(*params, **kwparams)
        setTimer(wrapper)
    
    setTimer(wrapper)
    return wrapper

def clearInterval(wrapper):
    wrapper.timer.cancel()




def checaConexao():
    
    from .models import Dermyah

    global tentativas    
    
    #mm = str(Dermyah.objects.get(id=1))
    mode_str = str(Dermyah.objects.get(id=1))    
    messager.type_mode = "Conexao: " + mode_str
    
    print("modo db:")
    print(mode_str)
          
    if(mode_str == 'Local'):
        print("MODO LOCAL ATIVO!!!")
        messager.internet1 = "Internet: Offline"
        messager.internet2 = "Internet: Offline"
        

    elif (messager.wifi_configurated == 0):
        if(tentativas > 4):
            print("EXCEDIDA AS TENTATIVAS!!!!!!!!!!!!")            
            messager.internet1 = "Tentativas de"
            messager.internet2 = "conexao excedidas!"
            m = Dermyah.objects.filter(id=1).update(wifi_mode='Local')
            change_access()            
        else:
            conn = httplib.HTTPConnection("www.google.com", timeout=50)
            try:
                conn.request("HEAD", "/")
                conn.close()
                print("Conectado à Internet")
                print("tentativas: ")
                print(set_tentativa(0))
                messager.internet1 = "Internet: Online"
                messager.internet2 = "Internet: Online"
                return True
            except:
                print("Falha Internet")
                print("tentativas: ")
                print(set_tentativa(1))
                conn.close()
                messager.internet1 = "Internet: Offline"
                messager.internet2 = "Tentativa: " + str(tentativas) + "/5"
                return False


def checkIo():
	
	if(GPIO.input(resetbutton) == 0):
		from .models import Dermyah
		tentativasIOreset = 0
		m = Dermyah.objects.filter(id=1).update(wifi_mode='Local')
		change_access()            
		print("RESETADOOOO")

class WebServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_service'
    
    def ready(self):         
       print("SEGUINDO")            
       interval_conexao = setInterval(checaConexao, 30)
       messager.message1 = "Maquina OK"
       messager.message2 = "Maquina OK"
       interval_messager = setInterval(messager.refreshMessage, 2)
       interval_button = setInterval(checkIo, 2)

