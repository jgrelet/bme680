import network
import socket
import time
from machine import Pin

from config import ssid, password


def set_wlan(oled):
    #Connect to WLAN
   
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Connecting...')
        oled.text('Connecting...', 0, 12)
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connection successful')
    print(f'Connected on {ip}')
    oled.text('Connection successful', 0, 24)
    oled.text(f'Connected on {ip}', 0, 36)
    oled.show()
