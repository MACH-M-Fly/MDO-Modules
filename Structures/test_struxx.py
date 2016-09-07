import matplotlib.pyplot as plt
from aircraft_structure import *
import numpy as np

flange_dim = np.array([np.array([ 0.02, 0.05]),
					   np.array([ 0.02, 0.05])])

web_dim = np.array([np.array([ 0.02, 0.05]),
					   np.array([ 0.02, 0.01])])

X = np.array([0, 1])

Spar = cantIBeam(1, 10**6,flange_dim, web_dim, X)

Spar.addElipticalDistLoad(100)

# # w = [10, 15, 20, 25, 20, 10]
# # X =  [ 0, 0.2, 0.4, 0.6, 0.8, 1.0]
# # Spar.addDistLoad(w,X)
# # Spar.addPointLoad(30, 0.75)
# Spar.addPointMomment(30, 0.75)
Spar.calcDistLoad()
Spar.calcShearForce()
Spar.calcMomment()


Spar.calcI()
Spar.calcStress()

x = np.linspace(0,1, 50)



f = []
f2 = []
f3 = []
for i in x:
	f.append(Spar.shearForce(i))
	f2.append(Spar.momment(i))
	f3.append(Spar.distLoad(i))

# plt.plot(x,f , 'b-', x, f2, 'r-', x, f3, 'g-')
# plt.show()




print 'Spar.I(0) ', Spar.I(0)

stress = []
for i in x:
	stress.append(Spar.stress(i))

plt.plot(x,stress , 'b-')

plt.firgure(2)

plt.plot(x,f , 'b-', x, f2, 'r-', x, f3, 'g-')

plt.show()

# print(Spar.shearForce(0.8))