import numpy as np
import random
import matplotlib.pyplot as plt
from time import time
from histogramaker import hist
from scipy.special import erf
from black_functions import tray_real,tray_b,black,tray_volat,tray_jump,returns


##------------------------------------------------##
##------------------------------------------------##
##           SIMULACIONES Y RESULTADOS            ##
##------------------------------------------------##
##------------------------------------------------##
 
##--------------------------------------##
##       EXTRACT REAL PARAMETERS        ##
##--------------------------------------##

##DATOS IBEX35 3 MESES, 62 DIAS HABILES##
#dia,precio=tray_real("ibex35.txt")

##DATOS BITCOIN 3 MESES, 90 DIAS HABILES##
#dia,precio=tray_real("bitcoin.txt")

##DATOS IBEX35 1 AÑO, 252 DIAS HABILES##
dia,precio=tray_real("ibex1year.txt")



#--------------------##
#PLOT REAL TRAJECTORY##
#--------------------##
"""
plt.figure(1);
plt.plot(dia,precio,'-')
plt.xlabel("t(days)", fontsize=10);
plt.ylabel("closing value", fontsize=10);         plt.axis('tight');
plt.show()
"""

##----------##
##VOLATILITY##
##----------##

retornos,desviacion,a,xi=returns(precio)
#volatility=desviacion*np.sqrt(len(precio))  #periodo para el que quiero la volatilidad: 3 meses son 63 dias habiles
volatility=desviacion
print("sigma=",volatility)
print("a=",a)
print("xi=",xi)

#print(retorno_medio)
#print(desviacion)
#print(volatility)

##--------------------------------------##
##            MY PARAMETERS             ##
##--------------------------------------##
s0=precio[-1]
k=precio[-1]
T=62
sigma=volatility
r=-0.0012
tiempo=0
intervalo=62
n=25


##--------------------------------------##
##   PROVING SOME ALEATORY PARAMETER    ##
##--------------------------------------##
"""
#
s0=150
k=155
T=3
#
sigma=0.2
r=0.05
tiempo=0
intervalo=3
n=1000
#
sigma0=0.2
xi=1.
a=10.
sigma_asterisco=0.2
#
"""



##--------------------------------------##
##         CALCULO DE OPCIONES          ##
##--------------------------------------##

##----------------##
##TRAJECTORY PLOTS##
##----------------##
"""
#normal form
for i in range(10):
    t,s = tray_b(r,sigma,s0,intervalo,n)
    plt.figure(2);
    plt.plot(t,s,'-')

plt.xlabel("t", fontsize=10);
plt.ylabel("S(t)", fontsize=10);         plt.axis('tight');
plt.show()
"""
##tienes dada en returns   a, xi
sigma_asterisco=volatility
sigma0=volatility
#stochastic volatility form
"""
for i in range(10):
    t,s = tray_volat(r,xi,s0,sigma0,a,sigma_asterisco,intervalo,n)
    plt.figure(3);
    plt.plot(t,s,'-')

plt.xlabel("t", fontsize=10);
plt.ylabel("S(t)", fontsize=10);         plt.axis('tight');
plt.show()
"""

landa=0.0005
epsilon=1
Y0=0.9
#stochastic volatility form
for i in range(20):
    t,s = tray_jump(r,xi,s0,sigma0,a,sigma_asterisco,landa,epsilon,Y0,intervalo,n)
    plt.figure(4);
    plt.plot(t,s,'-')

plt.xlabel("t", fontsize=10);
plt.ylabel("S(t)", fontsize=10);         plt.axis('tight');
plt.show()


###
###
###
###

print(" ")
print("BS exacta= ",black(tiempo,s0,T,k,r,sigma))



##------------------------##
##BLACKSCHOLES NORMAL FORM##
##------------------------##

"""
c_suma=0
rango=100000
for i in range(rango):
    t,s=tray_b(r,sigma,s0,intervalo,n)
    ci=np.exp(-r*(T-tiempo))*max([s[-1]-k,0])
    c_suma=c_suma+ci
c_suma=c_suma/rango

print("montecarlo_normal=",c_suma)


##------------------------##
##INCLUDE STOCH VOLATILITY##
##------------------------##
c_suma=0
rango=100000
for i in range(rango):
    t,s = tray_volat(r,xi,s0,sigma0,a,sigma_asterisco,intervalo,n)
    ci=np.exp(-r*(T-tiempo))*max([s[-1]-k,0])
    c_suma=c_suma+ci
c_suma=c_suma/rango

print("montecarlo_stocvol=",c_suma)
"""

##-------------##
##INCLUDE JUMPS##
##-------------##
c_suma=0
rango=100000
for i in range(rango):
    t,s = tray_jump(r,xi,s0,sigma0,a,sigma_asterisco,landa,epsilon,Y0,intervalo,n)
    ci=np.exp(-r*(T-tiempo))*max([s[-1]-k,0])
    c_suma=c_suma+ci
c_suma=c_suma/rango

print("montecarlo_jumps=",c_suma)




