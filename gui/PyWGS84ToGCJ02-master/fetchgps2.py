from pynmea import nmea
import serial
import os
from WGS84ToGCJ02 import transform
from WGS84Distance import distance
from selenium import webdriver
import pygame
import sys
from pygame.locals import *

#import threading

#class ThreadWorker(threading.Thread):
    #def __init__(self, callable, *args, **kwargs):
        #super(ThreadWorker, self).__init__()
        #self.callable = callable
        #self.args = args
        #self.kwargs = kwargs

    #def run(self):
        #self.callable(*self.args, **self.kwargs)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def decodeNMEAStream(serialport,GCJ02=False):
    while True:
        try:
            line = serialport.readline()
            line = line.decode('ascii')
            #print(line)
            if(line[4] == 'G'): # $GPGGA
                if(len(line) > 50):
                    #print line
                    gpgga = nmea.GPGGA()
                    gpgga.parse(line)
                    lats = gpgga.latitude
                    longs = gpgga.longitude
                    
                    #convert degrees,decimal minutes to decimal degrees 
                    _lat = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
                    lat = (float(lats[0]+lats[1])+_lat)+0.00623
                    _long = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
                    longs = (float(longs[0]+longs[1]+longs[2])+_long)+0.00643

                if GCJ02:
                    return transform(lat,longs)
                else:
                    return (lat,longs)
        except:
            continue
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)
    
if __name__ == "__main__":
    ser = serial.Serial("COM9",115200)

    origin_position = ()
    current_position = ()
    pre_position = ()
    pre =()
    cur = ()

    _avg = 5
    print('Average %d origin position'%_avg)
    _x = 0
    _y = 0
    for i in range(_avg):
        _p = decodeNMEAStream(ser,GCJ02=True)
        _x += _p[0]
        _y += _p[1]
        print('.')
    x = _x / _avg
    y = _y / _avg 
    origin_position = (x,y)
    print('done')

    pygame.init()
    # 获得当前显示器支持的分辨率
    size = pygame.display.list_modes()
    size_i = 3
    width, height = size[size_i]
    # 设置透明度
    transparent = 255

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([800,600])
    pygame.display.set_caption("Trace Test")
    fullscreen = False
    bg = (255, 255, 255) # RGB
    oturtle = pygame.image.load("driverless.jpg")
    turtle = oturtle
    oturtle_rect = oturtle.get_rect()
    position = turtle_rect = oturtle_rect
    screen.fill(bg)
    startflag = 0
    while True:
        if startflag == 0:
            current_position = decodeNMEAStream(ser,GCJ02=True)
            startflag = 1
        else:
            pre_position = current_position
            current_position = decodeNMEAStream(ser,GCJ02=True)
            print(current_position)
            print("distance:",distance(origin_position,current_position)*1000,'m')
            print(str(current_position[0])[0:10])
            print(str(current_position[1])[0:11])
            if abs(pre_position[0] - current_position[0])>0.0001 or abs(pre_position[1] - current_position[1])>0.0001:
                continue
            pre = ((pre_position[0]-31.8923415)*10000000+200,(pre_position[1]-118.8218435)*10000000+200)
            cur = ((current_position[0]-31.8923415)*10000000+200,(current_position[1]-118.8218435)*10000000+200)
            position.center = cur
            blit_alpha(screen, turtle, position, transparent)
            pygame.draw.aaline(screen, (255,255,0), pre, cur, 20)
            pygame.display.flip()
            #time.sleep(1)
