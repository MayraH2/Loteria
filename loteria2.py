# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 10:46:08 2020

@author: May50HX
"""

import numpy as np
import random as rand
import matplotlib.pyplot as plt
import sqlite3
import creartablero as ct
import nitidez as nt
import time,io,cv2
import pyttsx3

plt.ion()

def paso1():
    plt.close('all')
    num_jugadores= int(input("Cuantos jugadores son: "))
    (tablero1,lista,Nombres,ID) = ct.crear_tablero(num_jugadores)
    # print(lista)
    # print(Nombres)
    # print(ID)
              
    return tablero1,lista,num_jugadores,Nombres,ID


def paso2(tablero1,lista,num_jugadores,Nombres,ID):
    mascara=[0]*num_jugadores
    
    for i in range(num_jugadores):
        mascara[i]=[]
    op=0
    op=(input('Quiere mostrar una carta: '))
    while op != 'no':
        #Si quiere usar el modo manual, descomente la linea 42 y comente de la 52 a 55
        numero_carta=int(input('Ingrese un numero de carta: '))
        
        #Si quiere usar el modo manual pero con una imagen descomente la linea 46 a la
        #49 y comente de la linea 52 a 55
        # ima2=plt.imread('img/cartaprueba1.jpg')# es del 1 al 4 en cartaprueba#
        # ima2=cv2.cvtColor(ima2,cv2.COLOR_BGR2GRAY)  
        # ima3=nt.segmentacion(ima2)
        # numero_carta=nt.find_object(ima3)
        
        #Si quiere usar la cámara dejelo así como esta, no toque nadita, nadita
        # imagen=nt.capturar_imagen()
        # ima2=nt.rotar_imagen(imagen)
        # ima3=nt.segmentacion(ima2)
        # numero_carta=nt.find_object(ima3)
        (prueba,ganador,final)=ct.poner_maiz(tablero1,lista,num_jugadores,numero_carta,mascara,Nombres,ID)
        if final==4:
            break
        op=(input('Quiere mostrar otra carta: '))    
    
    return prueba        
   

opciones=int(input('Quiere hacer una prueba de imagen (1-si) o (2-no): '))
while opciones == 1:
    nt.prueba_imagen()
    opciones=int(input('Quiere hacer otra prueba de imagen (1-si) o (2-no): '))
(tablero1,lista,num_jugadores,Nombres,ID)=paso1()
time.sleep(4)
paso2(tablero1,lista,num_jugadores,Nombres,ID)





 