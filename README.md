# Option-pricing-on-assets

This is a simple work I did where I examine the analytical solution for the Black-Scholes equation and compare it with a numerical solution, using a Monte Carlo method. I apply it using the parameters extracted from the real evolution of the assets of IBEX35 of the last three months in the moment I did the work. Finally I make further considerations on the SDE proposed by Black and Scholes, so to make it more realistic, thus including stochastic volatilities and jumps, and then compare the numerical solutions of these models. The comments are mixed in English and Spanish, sorry for that.

##Materials

 - SSMprojectRAMONMARCGARCIASEUMA.pdf : A summary of all I did and the important explanations and results.
 - black_functions.py : The functions for doing the stochastic simulations and extract volatilities and prices.
 - black_analysis.py : Where I use these functions to take results and doing analysis.
