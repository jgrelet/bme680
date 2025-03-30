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

  while True:
    try:

      led_onboard.value(1)
      # Clear the display
      oled.fill(0)

      year, month, day, hour, minute, second, weekday, yearday = time.localtime()
      date_time = f"{hour:02d}:{minute:02d}:{second:02d} {month}/{day}/{year-2000:02d} "

      temp = str(round(bme.temperature, 2)) + ' C'
      #temp = (bme.temperature) * (9/5) + 32
      #temp = str(round(temp, 2)) + 'F'
      
      hum = str(round(bme.humidity, 2)) + ' %'
      pres = str(round(bme.pressure, 2)) + ' hPa'
      gas = str(round(bme.gas/1000, 2)) + ' KOhms'

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
  
    time.sleep(1)

# The use of main() and the if __name__ == "__main__" idiom is optional, 
# and it's only needed when the code is intended to be used both as a standalone 
# script and as a module.
if __name__ == "__main__":
  main()
