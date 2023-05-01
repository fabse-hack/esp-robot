import network
import gc


ssid = 'idontknow'
password = 'dumdidum'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected():
  pass

print('Connection successful')
print(station.ifconfig())


if station.ifconfig()[0] == '0.0.0.0':
  access_point = network.WLAN(network.AP_IF)
  access_point.active(True)
  access_point.config(essid='ESP-Robot', password='12345678')

gc.collect()