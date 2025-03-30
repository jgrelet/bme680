# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details: https://RandomNerdTutorials.com/raspberry-pi-pico-bme680-micropython/

from machine import Pin, I2C
import time
import network
import socket
import ntptime
from bme680 import *
from ssd1306 import SSD1306_I2C
from config import ssid, password
#from wlan import set_wlan
import gc
gc.collect()

# Connect to WLAN
def set_wlan(oled):
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Connecting...')
        oled.text('Connecting...', 0, 0)
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connection successful')
    print(f'Connected on {ip}')
    oled.text('Succesful', 0, 12)
    oled.text('Connected on:', 0, 24)
    oled.text(f'{ip}', 0, 36)
    oled.show()

def web_page(date_time, temp, pres, hum, gas):
  # HTML page to be served
  
  html = """<html><head><title>Pico 2w with BME680 sensor</title><meta http-equiv="refresh" content="5">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
  table { border-collapse: collapse; margin-left:auto; margin-right:auto; }
  th { padding: 12px; background-color: #0043af; color: white; }
  tr { border: 1px solid #ddd; padding: 12px; }
  tr:hover { background-color: #bcbcbc; }
  td { border: none; padding: 12px; }
  .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
  </style></head><body><h1>ESP with BME680</h1>
  <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>
  <tr><td>Time</td><td><span class="sensor">""" + date_time + """</span></td></tr>
  <tr><td>Temp. Celsius</td><td><span class="sensor">""" + temp + """</span></td></tr>
  <tr><td>Pressure</td><td><span class="sensor">""" + pres + """</span></td></tr>
  <tr><td>Humidity</td><td><span class="sensor">""" + hum + """</span></td></tr>
  <tr><td>Gas</td><td><span class="sensor">""" + gas + """</span></td></tr></body></html>"""
  return html

def main():
  # Display dimensions
  WIDTH =128 
  HEIGHT= 64

  # RPi Pico - Pin assignment
  i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))

  # Initialize SSD1306 display with I2C interface
  oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

  # Initialize BME680 sensor with I2C interface
  # BME680 I2C address is 0x76 or 0x77
  bme = BME680_I2C(i2c=i2c)
  led_onboard = Pin("LED", Pin.OUT)

  # Clear the display
  oled.fill(0)
  print("Initializing...,")
  oled.text("Initializing...,", 0, 0) 
  oled.show()

  led_onboard.value(1)
  # oled.fill(0)
  # oled.text('go to wlan...', 0, 0)
  # oled.show()
  set_wlan(oled)
  # oled.text('return wlan...', 0, 12)
  # oled.show()

  # Synchroniser l'heure avec un serveur NTP
  ntptime.settime()
  oled.text("NTP Ok...", 0, 48) 
  oled.show()
  time.sleep(2)
  oled.fill(0)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)

  while True:
    try:

      led_onboard.value(1)
      # Clear the display
      oled.fill(0)

      year, month, day, hour, minute, second, weekday, yearday = time.localtime()
      date_time = f"{hour:02d}:{minute:02d}:{second:02d} {month}/{day}/{year-2000:02d} "

      temp = f"{bme.temperature:.1f} C"
      #temp = str(round(bme.temperature, 2)) + ' C'
      #temp = (bme.temperature) * (9/5) + 32
      #temp = str(round(temp, 2)) + 'F'
      
      #hum = str(round(bme.humidity, 2)) + ' %'
      hum = f"{bme.humidity:.0f} %"
      pres =f"{bme.pressure:.1f} hPa"
      #pres = str(round(bme.pressure, 2)) + ' hPa'
      gas = f"{bme.gas/1000:.2f} KOhms"
      #gas = str(round(bme.gas/1000, 2)) + ' KOhms'

      print(f"{date_time}")
      print('Temperature:', temp)
      print('Humidity:', hum)
      print('Pressure:', pres)
      print('Gas:', gas)
      print('-------')
      oled.text(f"{date_time}", 0, 0)
      oled.text(f"Temp: {temp}", 0, 12)
      oled.text(f"Pres: {pres}", 0, 24)
      oled.text(f"Humi: {hum}", 0, 36)
      oled.text(f"Gas: {gas}", 0, 48)
      # Show the updated display
      oled.show()
      led_onboard.value(0)
    except OSError as e:
      print('Failed to read sensor.')
    
    """ try:
      if gc.mem_free() < 102000:
        gc.collect()
      conn, addr = s.accept()
      conn.settimeout(3.0)
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      conn.settimeout(None)
      request = str(request)
      print('Content = %s' % request)
      response = web_page(date_time, temp, pres, hum, gas)
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: text/html\n')
      conn.send('Connection: close\n\n')
      conn.sendall(response)
      conn.close()
    except OSError as e:
      conn.close()
      print('Connection closed') """
  
    time.sleep(1)

# The use of main() and the if __name__ == "__main__" idiom is optional, 
# and it's only needed when the code is intended to be used both as a standalone 
# script and as a module.
if __name__ == "__main__":
  main()
