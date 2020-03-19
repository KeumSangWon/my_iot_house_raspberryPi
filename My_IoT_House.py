import paho.mqtt.client as mqtt
import socket 
import time 

#UDP
from contextlib import closing 
host1 = '192.168.0.100' 
port1 = 4210

host2 = '192.168.0.101' 
port2 = 4211
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 #プログラム終了時にソケットを自動的に閉じる

#MQTT
MQTT_SERVER = "13.124.231.98"
MQTT_PATH = "test"


message = ""
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
 
    message = msg.payload.decode("utf-8")
    print(type(message))
    print(message)
    
    if message == "open":
        sock.sendto(message.encode('utf-8'), (host1, port1)) #ソケットにUDP送信
        print("OK1")
    else:
        sock.sendto(message.encode('utf-8'), (host2, port2)) #ソケットにUDP送信
        print("OK2")
    #message.decode('ascii')
    # more callbacks, etc
    
##    print(msg.topic+" "+message)
##    print(type(message))
    
    
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
