import requests

import socket 


#message = "Maquina Iniciada"
#type_mode = "Conexao: Local"
#ip_address = "IP: 192.168.1.1"
#internet = "Internet: Offline"

wifi_configurated = 0

message1 = "-"
message2 = "-"
type_mode = "--"
ip_address = "--"
internet1 = "---"
internet2 = "---"

index_msg = 0

localIp = ""


def sendPost(myurl, mydata):
    myheader ={
        'X-Api-Key': 'E83C0A7C190D4A1DB3C78C38FAC76202',
        'Content-Type': 'application/json'
    }
    response = requests.post(url=myurl, json=mydata, headers=myheader)
    print(response.text)
    return response.text


def sendGet(myurl):
    myheader ={
        'X-Api-Key': 'E83C0A7C190D4A1DB3C78C38FAC76202',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=myurl, headers=myheader)        
    print(response.json())
    return response.text


def getIp():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '192.168.1.1'
    finally:
        st.close()
    return IP


def refreshMessage():
    global ip_address
    
    all_messages = [
        message1,
        message2,
        message1,
        message2,
        type_mode,                
        ip_address,
        internet1,
        internet2
    ]

    print("REFRESH MESSAGE!")

    myurl = 'http://localhost:8002/api/printer/command'

    global index_msg
    #print("all messages:")
    #print(len(all_messages))

    if(index_msg == 4):
        localIp = str(getIp())
        ip_address = localIp
        print("MEU IP E")
        print(ip_address)

    if index_msg < (len(all_messages) -1):
        index_msg += 1
    else:
        index_msg = 0

    msg = "M117 " + str(all_messages[index_msg])

    myData = {
          "command": msg
    }

    sendPost(myurl,myData)



