# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:54:16 2020

@author: May50HX
"""
from skimage import io, filters, color, measure,morphology
import matplotlib.pyplot as plt
from skimage.filters import rank, threshold_otsu
import numpy as np
import cv2
import pytesseract, imutils
import matplotlib as pp

N_COEF = 15
coeficientes = np.load("coeficientes.npy")


plt.close("all")

def rotar_imagen(imagen):
    
    [fil,col]= imagen.shape
    new= imutils.rotate_bound(imagen, 90)
    [fi,co]=new.shape
    # print(fi)
    # print(co)
    recorte1=new[239:1690,88:1000]
    plt.figure(5)
    plt.axis('off')
    plt.imshow(recorte1,cmap='gray')
    plt.pause(1) 
    # pp.image.imsave('cartaprueba'+str(n)+'.jpg',recorte1)
    
    return recorte1 
 
def segmentacion(imagen):
    ima2=cv2.resize(imagen,(1400,2300))   
    # plt.figure()
    # plt.imshow(ima2,cmap='gray')
       
    ima3=ima2[120:285,65:280]
    ima5=ima2[1976:2150,55:1280]
    
    binario = ima3 <= threshold_otsu(ima3)   
    dilatada=morphology.binary_dilation(binario)
    erosion=morphology.binary_erosion(dilatada)
    erosion2=morphology.binary_erosion(erosion)
    peque2=morphology.remove_small_holes(erosion2, 550).astype(int)
    
    binario2 = ima5 <= threshold_otsu(ima5)
    dilatada= morphology.binary_dilation(binario2)
        
    return peque2

def elimina_bordes(imagen):
    filas, columnas = imagen.shape
    xmax = 0
    xmin = filas
    ymax = 0
    ymin = columnas
    for ki in range(filas):
        for kj in range(columnas):
            if imagen[ki, kj]:
                if ki > xmax:
                    xmax = ki
                if ki < xmin:
                    xmin = ki
                if kj > ymax:
                    ymax = kj
                if kj < ymin:
                    ymin = kj
    imagen = imagen[xmin:(xmax+1), ymin:(ymax+1)]
    return imagen, ymin    


def generar_polinomio(coeficientes):
    tpol = np.linspace(0, 1, 100)
    pol = np.ones(100)*coeficientes[-1]
    exponente = 1
    for c in range(len(coeficientes)-2, -1, -1):
        pol += tpol**exponente * coeficientes[c]
        exponente += 1
    return pol, tpol


def generar_comparador(coeficientes, t):
    tpol = t
    comparador = np.ones(len(t))*coeficientes[-1]
    exponente = 1
    for c in range(len(coeficientes)-2,-1,-1):
        comparador += tpol**exponente * coeficientes[c]
        exponente += 1
    return comparador


def gen_perfiles(imagen):
    filas, columnas = imagen.shape
    perfil = []
    t = []
    # Obtenermos perfil desde la izquierda
    n = 0
    for i in range(filas):
        for j in range(columnas):
            if imagen[i,j]:
                perfil.append(j)
                t.append(n)
                n = n+1
                break
    # Obtenemos perfil desde la derecha
    for i in range(filas):
        for j in range(columnas-1,-1,-1):
            if imagen[i,j]:
                perfil.append(j)
                t.append(n)
                n = n+1
                break    
    perfil = np.array(perfil)/max(perfil)
    t = np.array(t)/(len(t)-1)
    return perfil, t


def error_absoluto(comparador,prueba):
    ea=0
    for i in range(len(comparador)):
        ea += abs(comparador[i]-prueba[i])
    # print(ea)
    error_total=ea/len(comparador)
    # print(error_total)
    return error_total

def find_object(imagen1):
    separados, objetos = measure.label(imagen1, return_num = True, connectivity=2)
    print(objetos)
    # plt.figure()
    # plt.imshow(separados,cmap='gray')
    # plt.pause(1)
    ordenar = []
    
    identificados = []
    for obj in range(objetos):
        num=np.where(separados == obj + 1, 1, 0)
        num, x_pos= elimina_bordes(num)
        
        limite=int(np.add.reduce(num,None))
        if limite >1900: 
           # plt.figure()
           # plt.imshow(num)
           # plt.pause(1)
           ordenar.append(x_pos)
           perfil, t = gen_perfiles(num)
           coef_nuevo = np.polyfit(t,perfil, 15)
           pol, tpol = generar_polinomio(coef_nuevo)
           
           errores = []
           for i in range(10):
               comp = generar_comparador(coeficientes[i], tpol)
               errores.append(error_absoluto(comp,pol))
               
           seleccionado = np.argmin(errores)
           identificados.append(seleccionado)
           print(f'El objeto {obj+1} es un {seleccionado}')
           print(ordenar)
    for n1 in range(len(ordenar)):
        for n2 in range(n1+1,len(ordenar)):
            if n1 == n2:
                continue
            if ordenar[n1] > ordenar[n2]:
                aux = ordenar[n1]           
                ordenar[n1] = ordenar[n2]*1
                ordenar[n2] = aux*1
                aux = identificados[n1]*1            
                identificados[n1] = identificados[n2]*1
                identificados[n2] = aux*1
            else:
                identificados=identificados
    print("Números identificados conforme a la carta")
    print(identificados)
    
    if len(identificados)==1:
        numerito=identificados[0]
        print('El número es: ',numerito)
    elif len(identificados)==2:
        letra1=str(identificados[0])
        letra2=str(identificados[1])
        numerito=int(letra1+letra2)
        print('El número es: ',numerito)
    else:
        numerito=0
        print('no hay numero')
           
    return numerito
        

def capturar_imagen():   
    url='http://192.168.0.22:8080/shot.jpg'
    cap=cv2.VideoCapture(url)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)        
    cap.release()
    
    return gray 
       
def prueba_imagen():
    imagen=capturar_imagen()
    ima2=rotar_imagen(imagen)
    ima3=segmentacion(ima2)
    plt.imshow(ima3,cmap='gray')
    plt.pause(1)
        
# prueba_imagen()


       




