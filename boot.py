import network
import gc
#import webrepl


ssid = 'idontknow'
password = 'dumdidum'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


#webrepl.start()
gc.collect()