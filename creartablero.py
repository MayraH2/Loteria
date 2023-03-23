# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 11:58:44 2020

@author: May50HX
"""
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import sqlite3
import io
import pyttsx3

engine=pyttsx3.init()
engine.setProperty('rate', 120)


def crear_conexion(base_datos):
    try:
        conexion =sqlite3.connect(base_datos)
        # print('Se ha creado la conexion')
        return conexion
    except sqlite3.Error as error:
        print('Se ha producido un error en la conexion :(',error)



def recuperar_carta(id):
    conexion=crear_conexion('CartasLoteria.db')
    sql ="SELECT * FROM Carta WHERE id =?;"
    
    cursor = conexion.cursor()
    cursor.execute(sql,(id,)) 
    
    registros = cursor.fetchall()  
        
    return registros


def crear_lista(numero):
    jugadores = []
    a= 1       
    while a <= numero:
        n = 1
        tablero= [rand.randint(1,54)]
        while n < 16:
            nuevo = rand.randint(1,54)
            if nuevo not in tablero:
                tablero.append(nuevo)
                n +=1   
        jugadores +=tablero
        a +=1 
    paso2 = np.array(jugadores).reshape(numero,16)
   
    return paso2

def gritar_nombre(numero):
    cartitas=list(range(10,54))
    if numero==1:
        engine.say('el gallo')
        engine.runAndWait()
    elif numero ==2:
        engine.say('el diablito')
        engine.runAndWait()
    elif numero ==3:
        engine.say('la dama')
        engine.runAndWait()
    elif numero ==4:
        engine.say('el catrin')
        engine.runAndWait()
    elif numero ==5:
        engine.say('el paraguas')
        engine.runAndWait()
    elif numero ==6:
        engine.say('la sirena')
        engine.runAndWait()
    elif numero ==7:
        engine.say('la escalera')
        engine.runAndWait()
    elif numero ==8:
        engine.say('la botella')
        engine.runAndWait()
    elif numero ==9:
        engine.say('el barril')
        engine.runAndWait()
    elif numero in cartitas:
        registro=recuperar_carta(numero)
        nombre=registro[0][1]
        engine.say(nombre)
        engine.runAndWait()
    else:
        print('no es un numero válido')
               
    
def verificar_ganador(mascara):
    opciones=[[0,1,2,3],[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,5,6,7],[8,4,10,11],[12,13,14,15],[0,5,10,15],[3,6,9,12]]
    n=0
    p=0
    comparar=mascara
    for i in range(len(comparar)):
        paso=comparar[i]
        for j in range(len(opciones)):
            muestra=opciones[j]
            for z in range(len(muestra)):
                if muestra[z] in paso:
                    n +=1
                if n==4:
                    engine.say('Jugador #'+str(i+1)+' gano el juego, Felicidades')
                    engine.runAndWait()
                    print('Jugador #'+str(i+1)+' gano el juego yeiiiii')
                    p=4
            n=0           
                
    return p


def crear_tablero(num):    
    lista=crear_lista(num)     
    tableros=[0]*num
    Nombres=[0]*num
    ID=[0]*num
    No2=[0]*16
    id2=[0]*16
    for i in range(num):
        matriz=np.ones((700,500,3))
        matriz[3:697,3:497]=255
        mot=lista[i]    
        No2=[0]*16
        id2=[0]*16
        for j in range (16):
            # carta=escoger_imagen(mot[j])  
            listat=recuperar_carta(np.int(mot[j]))#mot[j])
            No2[j]=listat[0][1]
            id2[j]=listat[0][2]
            binario=listat[0][3]

            carta= plt.imread(io.BytesIO(binario),format='jpeg')
            if j==0:
                matriz[19:169,19:119]=carta
            if j==1:
                matriz[19:169,139:239]=carta
            if j==2:
                matriz[19:169,259:359]=carta
            if j==3:
                matriz[19:169,379:479]=carta
            if j==4:
                matriz[189:339,19:119]=carta
            if j==5:
                matriz[189:339,139:239]=carta
            if j==6:
                matriz[189:339,259:359]=carta
            if j==7:
                matriz[189:339,379:479]=carta
            if j==8:
                matriz[359:509,19:119]=carta
            if j==9:
                matriz[359:509,139:239]=carta
            if j==10:
                matriz[359:509,259:359]=carta
            if j==11:
                matriz[359:509,379:479]=carta
            if j==12:
                matriz[529:679,19:119]=carta
            if j==13:
                matriz[529:679,139:239]=carta
            if j==14:
                matriz[529:679,259:359]=carta
            if j==15:
                matriz[529:679,379:479]=carta
        
        Nombres[i]=No2
        ID[i]=id2
        tableros[i]=matriz
        plt.figure(i,figsize=(6,8),dpi=100)
        plt.title('Jugador #'+str(i+1),fontsize=15)
        plt.axis('off')
        plt.tight_layout()        
        plt.imshow(np.uint8(tableros[i]))
        plt.pause(1)
    plt.pause(2)
        
    return tableros, lista, Nombres, ID


def poner_maiz(tablero,lista,num,num_carta,mascara,Nombres,ID):
    # gritar_nombre(Nombres, ID, num_carta)
    gritar_nombre(num_carta)
    Maiz = plt.imread('C:/Users/May50HX/Pictures/loteria/grano.jpg')    
    matriz2=tablero
    lista2=lista
    mascaras=mascara
    p=[52,87,77,112,172,207,247,282,292,327,412,447,417,452,587,622]   
    lista3=[0]*num    
    for i in range(len(lista2)):
        revision=lista2[i]
        tab_ma=matriz2[i]
        masc=mascaras[i]
        for j in range(len(revision)):
            if num_carta == revision[j]:
                indice=j
                if indice==0:
                    tab_ma[p[2]:p[3],p[0]:p[1]]=Maiz
                    masc.append(indice)
                elif indice==1:
                    tab_ma[p[2]:p[3],p[4]:p[5]]=Maiz
                    masc.append(indice)
                elif indice==2:
                    tab_ma[p[2]:p[3],p[8]:p[9]]=Maiz
                    masc.append(indice)
                elif indice==3:
                    tab_ma[p[2]:p[3],p[10]:p[11]]=Maiz
                    masc.append(indice)
                elif indice==4:
                    tab_ma[p[6]:p[7],p[0]:p[1]]=Maiz
                    masc.append(indice)
                elif indice==5:
                    tab_ma[p[6]:p[7],p[4]:p[5]]=Maiz
                    masc.append(indice)
                elif indice==6:
                    tab_ma[p[6]:p[7],p[8]:p[9]]=Maiz
                    masc.append(indice)
                elif indice==7:
                    tab_ma[p[6]:p[7],p[10]:p[11]]=Maiz
                    masc.append(indice)
                elif indice==8:
                    tab_ma[p[12]:p[13],p[0]:p[1]]=Maiz
                    masc.append(indice)
                elif indice==9:
                    tab_ma[p[12]:p[13],p[4]:p[5]]=Maiz
                    masc.append(indice)
                elif indice==10:
                    tab_ma[p[12]:p[13],p[8]:p[9]]=Maiz
                    masc.append(indice)
                elif indice==11:
                    tab_ma[p[12]:p[13],p[10]:p[11]]=Maiz
                    masc.append(indice)
                elif indice==12:
                    tab_ma[p[14]:p[15],p[0]:p[1]]=Maiz
                    masc.append(indice)
                elif indice==13:
                    tab_ma[p[14]:p[15],p[4]:p[5]]=Maiz
                    masc.append(indice)
                elif indice==14:
                    tab_ma[p[14]:p[15],p[8]:p[9]]=Maiz
                    masc.append(indice)
                elif indice==15:
                    tab_ma[p[14]:p[15],p[10]:p[11]]=Maiz
                    masc.append(indice)
        
        
        mascara[i]=masc         
        lista3[i]=tab_ma
        plt.figure(i)
        plt.imshow(np.uint8(lista3[i]))
        plt.pause(1)
    # print(mascara)
    
    p=verificar_ganador(mascara)       
    
    plt.pause(2)   
    return lista3,mascara,p
                

    

        
