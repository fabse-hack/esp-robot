# Overview from the programm - written in micropython
🚀 check micropython for more informations: [Micropython](https://micropython.org/)
🐫 check micropython libraries: [Micropython Libraries](https://docs.micropython.org/en/latest/library/index.html)

The Robot use this python scripts:
1. boot.py  
2. main.py  
3. hcsr04.py  
4. dsmotor.py  
***
## 1. boot.py

```
import network
import gc


ssid = 'your-SSID'                # here is your wifi ssid
password = 'dumdidum'             # here is your wifi password

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)   # connect to wifi

while station.isconnected() == False:
  pass

print('Connection successful')    # if it connected -> success
print(station.ifconfig())

gc.collect()                      # garbage collector
```
to-do:  
- [ ] Wifi connection fallback

***
## 2. main.py
