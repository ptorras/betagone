# -*- coding: utf-8 -*-
#import numpy as np

import cv2
import matplotlib.pyplot as plt

def mov(posi,posf):
   rec=[]
   j=posi[1] 
   for i in range(posi[0],posf[0]+1):
        rec.append([i,j])
   for j in range(posi[1],posf[1]+1):
        rec.append([i,j])
   #rec.append([i,j]) 
   return rec


#####ir a buscar la pieza#####
def buscarpeca(posi):
    rec=[]
    i=0
    j=0
    for i in range(0,posi[0]+1):
        rec.append([i,j])
    for j in range(1,posi[1]+1):
        rec.append([i,j])
    
    return rec

def cami(rec):
    cont=0
    first=0
    img = cv2.imread("tablero.jpeg")
    print(rec)
    for i in (rec):
        cont=cont+1
        if(cont<len(rec)):
            
            if(i[1]==rec[cont][1]):
                print(i)
                x1=(i[1]*100)+50
                y1=(i[0]*110)
                x2=x1
                y2=y1+110
                cv2.line(img, (x1,y1),(x2,y2),(255,255,255),2)
            else:
                #print(i)
                if(first==0):
                    print(i)
                    first=1
                    x1=(i[1]*100)+50
                    y1=(i[0]*110)
                    x2=x1
                    y2=y1+110
                    cv2.line(img, (x1,y1),(x2,y2),(255,255,255),2)
                    x2=x2+110
                    y1=y2
                    cv2.line(img, (x1,y1),(x2,y2),(255,255,255),2)
                    
                else:
                    
                        print(i)
                        x1=(i[1]*100)+50
                        y1=(i[0]*110)+110
                        x2=x1+110
                        y2=y1
                        cv2.line(img, (x1,y1),(x2,y2),(255,255,255),2)
                    
    x1=(i[1]*100)+50
    y1=(i[0]*110)+110
    x2=x1+110
    y2=y1
    cv2.line(img, (x1,y1),(x2,y2),(255,255,255),2)
    
    cv2.line(img, (x2,y2),(x2-50,y2-50),(255,255,255),2)
    
    plt.imshow(img)
 


posi=[0,1]
posf=[2,2]
rec=(buscarpeca(posi))
print(cami(rec))

rec1=mov(posi,posf)
print(cami(rec1))

