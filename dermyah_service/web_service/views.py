from django.shortcuts import render, redirect

import subprocess

import re

import os

from .models import Dermyah

from web_service import messager


redes = {
}

def remove_access_point():
    m = Dermyah.objects.filter(id=1).update(wifi_mode="Rede Ext.")
    print("REMOVE ACCESS POINT")
    r = subprocess.check_output('sudo systemctl disable hostapd dnsmasq', shell=True)
    r = subprocess.check_output('sudo cp -f /etc/dhcp_change/dhcpcd.conf /etc/', shell=True)            
	

def mainPage(request):
	
	dados = {
        'myip' : messager.getIp()
    }
	
	return render(request, 'index.html', dados)
	

def reset(request):
 
	try:
		m = Dermyah.objects.filter(id=1).update(wifi_mode='Local')
		r = subprocess.check_output('sudo systemctl enable hostapd dnsmasq', shell=True)
		r = subprocess.check_output('sudo cp -f /etc/dhcp_change/local/dhcpcd.conf /etc/', shell=True)

		r = subprocess.check_output('wpa_cli remove_network 0', shell=True)    
		r = subprocess.check_output('wpa_cli remove_network 1', shell=True)
		r = subprocess.check_output('wpa_cli save_config', shell=True)

		messager.message1 = "Reinicie a maquina,"
		messager.message2 = "wifi Local ativado"
		print("---------END------------")
		return render(request, 'index.html')
 
	except Exception:
		
		return render(request, 'index.html')

#main page
def index(request):
	
	dados = {
		'myip' : messager.getIp()
	}
	
	return render(request, 'index.html', dados)

#called to auth user
def wifi(request):
	credentials = {
        'user': 'dermyah',
        'pswd': 'dermyah3d',
        'admin': 'admin'
    }

	dados = {     
		'myip' : messager.getIp()
	}

	if request.method == 'POST':
		
		if request.POST['user_input'] == credentials['admin'] and request.POST['pswd_input'] == credentials['pswd']:
			
			print("Admin LOGADO!!!")
			return redirect('login_admin')
		
		if request.POST['user_input'] == credentials['user'] and request.POST['pswd_input'] == credentials['pswd']:
			print("User Logado!!!")
			return redirect('login')  
           
		else:		
			print("Autenticação Negada!")
			return render(request, 'index.html',dados)          
          
	else:
		return render(request, 'index.html',dados)

#render login page and scan wifi
def login(request):
    scan()
    dados = {
        'nome_das_redes' : redes,
        'myip' : messager.getIp()
    }
    
    return render(request, 'wifi.html', dados)

#render ADMIN login page and scan wifi
def login_admin(request):
    scan()
    r = subprocess.check_output('ls /dev/serial/by-id/*', shell=True)
    uc_addr = str(r)
    uc_addr = uc_addr[2:]
    uc_addr = uc_addr[:-3]
	
	
    dados = {
        'nome_das_redes' : redes,
        'serial' : uc_addr,
        'myip' : messager.getIp()

    }

    return render(request, 'wifi_admin.html', dados)



#called to receive values from page form
def connect(request):
    if request.method == 'POST':
        
        ssid = request.POST['net_ssid']
        pswd = request.POST['pswd_ssid'] 
        pswd2 = request.POST['pswd_ssid2']
        print(ssid)
        print(pswd)
        print(pswd2)

        if ssid == "" or pswd == "" or pswd2 == "":
            print("VALORES INVALIDOS")
            return redirect('login')
        else:    

            print("WIFI CHANGE")
            command_str1 = 'wpa_cli set_network 0 ssid ' + "'" + '"' + ssid + '"' + "'"
            print(command_str1)
            command_str2 = 'wpa_cli set_network 0 psk ' + "'" + '"' + pswd + '"' + "'"
            print(command_str2)

            r = subprocess.check_output('wpa_cli remove_network 0', shell=True)
            #print(r)
            r = subprocess.check_output('wpa_cli remove_network 1', shell=True)
            #print(r)
            r = subprocess.check_output('wpa_cli add_network', shell=True)
            #print(r)
            r = subprocess.check_output(command_str1, shell=True)
            #print(r)
            r = subprocess.check_output(command_str2, shell=True)
            #print(r)            
            r = subprocess.check_output('wpa_cli enable_network 0', shell=True)
            #print(r)
            r = subprocess.check_output('wpa_cli save_config', shell=True)
            #print(r)
            
            #old commands:
            #p1 = subprocess.Popen(["wpa_passphrase", ssid, pswd], stdout=subprocess.PIPE)
            #p2 = subprocess.Popen(["sudo","tee","-a","/etc/wpa_supplicant/wpa_supplicant.conf",">","/dev/null"], stdin=p1.stdout, stdout=subprocess.PIPE)
            #p1.stdout.close()  # Give p1 a SIGPIPE if p2 dies.
            #output,err = p2.communicate()    
                        

            remove_access_point()

            messager.wifi_configurated = 1
            messager.message1 = "Wifi configurado!"
            messager.message2 = "Reinicie a maquina!"
            messager.index_msg = 0
            #os.system('sudo reboot')

            return render(request, 'index.html')

    else:
        return redirect('login')


def success(request):

    return render(request, 'success.html')


def arduino(request):
	uc_addr = ""

	try:
		r = subprocess.check_output('ls /dev/serial/by-id/*', shell=True)
		uc_addr = str(r)
		uc_addr = uc_addr[2:]
		uc_addr = uc_addr[:-3]		
		uc_addr = 'make flash FLASH_DEVICE=' + uc_addr 		
		print("uc:")		
		print(uc_addr)		
		print("-------------------")
		r = subprocess.call(["/home/pi/dermyah_service/gravar.sh",uc_addr])
		print("--------andre----------")
		print(r)		
		return render(request, 'index.html')
 
	except Exception:
		print("ERRO EXCECAO!")
		return render(request, 'index.html')

def scan():

 try:
  command = ['sudo iwlist wlan0 scanning | grep ESSID']
  networks = subprocess.check_output(command,shell=True)

  nets = networks.decode("utf-8")
    
  netSplit = nets.split('ESSID:')
  #print(netSplit)
  
  index = 0

  for element in netSplit:      
      wifi = re.sub(r"\s+", "", element)
      wifi = wifi.replace('"', '')
      if wifi != None and wifi != "":     
        index += 1
        redes[index] = wifi
      #print(wifi)
  
  print(redes)   

 except:
  print("erro")    


