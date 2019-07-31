import numpy as np
import random
import matplotlib.pyplot as plt
from time import time
from histogramaker import hist
from scipy.special import erf


#FUNCION PLOT DE LA EVOLUCION REAL DE LAS ACCIONES
def tray_real(texto):
    with open(texto) as f:
        n=0
        dias=[]
        precio=[]
        for linea in f:
            #linea.split("/n")
            precio.append(float(linea))
            dias.append(n)
            n=n+1
    return dias,precio

#SOLUCION EXACTA DE BLACK-STOCKES
def black(tiempo,S,T,k,r,sigma):
    d1=(np.log(S/k)+(r+sigma**2/2)*(T-tiempo))/(sigma*np.sqrt(T-tiempo))
    d2=d1-sigma*np.sqrt(T-tiempo)
    N1= 0.5*(erf(d1/np.sqrt(2))+1)
    N2= 0.5*(erf(d2/np.sqrt(2))+1)
    c = S*N1 - k*np.exp(-r*(T-tiempo))*N2
    return c


#FUNCION TRAYECTORIAS ESTOCASTICAS GBM
def tray_b(r,sigma,s0,intervalo,n):
    s=[s0]
    t=[0.]
    delta_t = 1./n
    for j in range(int(intervalo*n)):
        s_next = s[-1]*np.exp((r-sigma**2/2)*delta_t+np.random.normal()*sigma*delta_t**(1/2))
        s.append(s_next)
        t.append(t[-1]+delta_t)
    return t,s

#FUNCION TRAYECTORIAS ESTOCASTICAS CON STOCHASTIC UNCORRELATED VOLATILITY
def tray_volat(r,xi,s0,sigma0,a,sigma_asterisco,intervalo,n):
    mu=a*(sigma_asterisco-sigma0)
    s=[s0]
    t=[0.]
    v=[sigma0**2]
    delta_t = 1./n
    for j in range(int(intervalo*n)):
        v_next = v[-1]*np.exp((mu-xi**2/2)*delta_t+np.random.normal()*xi*delta_t**(1/2))
        s_next = s[-1]*np.exp((r-v[-1]/2)*delta_t+np.random.normal()*(v[-1]*delta_t)**(1/2))
        mu = a*(sigma_asterisco-v_next**(1/2))
        v.append(v_next)
        s.append(s_next)
        t.append(t[-1]+delta_t)
    return t,s

#FUNCION TRAYECTORIAS ESTOCASTICAS CON STOCHASTIC UNCORRELATED VOLATILITY
def tray_jump(r,xi,s0,sigma0,a,sigma_asterisco,landa,epsilon,Y0,intervalo,n):
    mu=a*(sigma_asterisco-sigma0)
    s=[s0]
    t=[0.]
    v=[sigma0**2]
    Y=1.
    k=epsilon*(Y-1.)
    delta_t = 1./n
    for j in range(int(intervalo*n)):
        dados=random.random()
        if dados<landa:
            posionega=random.random()
            if posionega < 0.95:
                Y=Y*Y0
            if posionega > 0.95:
                Y=Y*(2.05-Y0)
                
        if dados>landa:
            Y=1.
            #print("salto")
            
        v_next = v[-1]*np.exp((mu-xi**2/2)*delta_t+np.random.normal()*xi*delta_t**(1/2))
        #s_next = s[-1]*Y*np.exp((r-v[-1]/2-landa*k)*delta_t+np.random.normal()*(v[-1]*delta_t)**(1/2))
        s_next = s[-1]*Y*np.exp((r-v[-1]/2)*delta_t+np.random.normal()*(v[-1]*delta_t)**(1/2))
        mu = a*(sigma_asterisco-v_next**(1/2))
        v.append(v_next)
        s.append(s_next)
        t.append(t[-1]+delta_t)
    return t,s



#RETORNOS DE PRECIOS
def returns(prices):
    totaldays=len(prices)
    retornos=[]
    for i in range(totaldays):
        if i > 0:
            retornos.append(np.log(prices[i]/prices[i-1]))
            
    """todo directo, 1 ponderacion
    retorno_medio=sum(retornos)/float(len(retornos))
    
    sumas=0.
    for i in range(len(retornos)):
        sumas=sumas+(retornos[i]-retorno_medio)**2
    desviacion=np.sqrt(sumas/(len(retornos)-1))
    """
    desviacionesmeds=[]
    for j in range(len(retornos)-10):
        retornomedio=0.
        for k in range(10):
            retornomedio=retornomedio+retornos[j+k]
        retornomedio=retornomedio/10.
        desviacionmedia=0
        for k in range(10):
            desviacionmedia=desviacionmedia+(retornos[j+k]-retornomedio)**2
        desviacionmedia=np.sqrt(desviacionmedia/(9))
        
        desviacionesmeds.append(desviacionmedia)
    
    desviacion_media=sum(desviacionesmeds)/float(len(desviacionesmeds))   
    
    v=[n*n for n in desviacionesmeds]
    retornosv=[]
    for i in range(len(v)):
        if i>0:
            retornosv.append(np.log(v[i]/v[i-1]))
            
    ##extraer a##
    ases=[]
    for l in range(len(retornosv)):
        ases.append(retornosv[l]/(desviacion_media-desviacionesmeds[l+1]))
    a=sum(ases)/float(len(ases))
    
    ##extraer xi##
    retornov_medio=sum(retornosv)/float(len(retornosv))
    sumas=0.
    for i in range(len(retornosv)):
        sumas=sumas+(retornosv[i]-retornov_medio)**2
    xi=np.sqrt(sumas/(len(retornos)-1))
    
    
    return retornos,desviacion_media, a, xi
    
    