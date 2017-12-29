#!/usr/bin/python
# -*- coding:UTF-8 -*-
from bluepy import btle
from bluepy.btle import DefaultDelegate
import time
import binascii
import struct

class NotifyDelegate(DefaultDelegate):
    def __init__(self):
            DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        val = binascii.b2a_hex(data)
        #val = binascii.unhexlify(val)
        #val = struct.unpack('f', val)[0]
        #print "notify from %s = %s\n" % (str(cHandle),str(val))
        val=str(val)
        val=val.replace("2450434c","")
        if(len(val)==32):
            type=val[0:2]
            value=val[26:28]
            print "value:%s" % value
            #hex 2 10
            value=float(int(value,16))
            if(type=="41"): #glu
                 value=value/18
            if(type=="51"): #ua
                 value=value/16.81*0.1
            if(type=="61"): #chol
                 value=value/38.66
            print "type: %s\n value: %.2f mmol/L" % (type,value)
        else:
            print "err"

dev=btle.Peripheral("00:15:83:00:47:B4").withDelegate(NotifyDelegate())

time.sleep(0.5)

for ser in dev.getServices():
    print(str(ser))
    for chara in ser.getCharacteristics():
        print(str(chara))
        print("Handle is "+str(chara.getHandle()))
        print("properties is "+chara.propertiesToString())
        if(chara.supportsRead()):
            print(type(chara.read()))
            print(chara.read())
    print("\n")

try:
  while(True):
      if(dev.waitForNotifications(1)):
        #if(i>1000):
        #    break
        #continue
          print "ok"
      else:
          print "Waiting...";
      time.sleep(0.5)
finally:
    dev.disconnect()
