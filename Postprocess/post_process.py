import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from setup import getY
import numpy as np
from lib_spline import getPoints, getThickness
import string
from setup import points_initial, X
import shutil, os

def post_process_opt(Y, alpha):
	# ================= write airfoil file ======================

	Y = getY(Y)
	cv = np.concatenate((X.T, Y.T), axis = 1)
	points = getPoints(P=cv, n=3, V_type="clamped")


	f = open('airfoil_opt.dat', 'w')
	# f.write('opt airfoil\n')

	for i in range(0, len(points)):
	  # print(i)
	  f.write(str(points[i,0]) + ' ' + str(points[i,1]) + '\n')

	f.close()

	# ================= create aifoil plot =======================



	fig , ax = plt.subplots(figsize=[12,6])
	plt.plot(points[:,0], points[:,1], 'b')
	plt.xlim([0, 1])
	plt.ylim([-0.15,0.35])

	at = AnchoredText(str(alpha),prop=dict(size=17), frameon=True, loc=2 )
	at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
	ax.add_artist(at)

	plt.savefig('Xfoil_OPT.pdf', bbox_inches='tight')


	#================ create comparison plot ======================
	fig, ax = plt.subplots(figsize=[12,6])


	plt.xlim([0, 1])
	plt.ylim([-0.15,0.35])


	ax.plot(points[:,0], points[:,1],'b', label ='optimized result')
	ax.plot(points_initial[:,0], points_initial[:,1],'k--', label='Initial')
	# ax.plot(cv[:,0], cv[:,1],'o', label='cv')



	legend = ax.legend(loc='upper right', shadow=True)


	frame = legend.get_frame()
	frame.set_facecolor('0.90')

	# Set the fontsize
	for label in legend.get_texts():
	    label.set_fontsize('large')

	plt.savefig('OPT_Comparison.pdf', bbox_inches='tight')


	# ==================== organize files =================

	try:
		shutil.rmtree('./SOL_#')

	except:
		pass


	os.mkdir('./SOL_#')

	shutil.move('./OPT_Comparison.pdf', './SOL_#')
	shutil.move('./Xfoil_OPT.pdf', './SOL_#')

	shutil.move('./airfoil_opt.dat', './SOL_#')

	shutil.move('./hist.db', './SOL_#')
	shutil.move('./SNOPT_print.out', './SOL_#')
	shutil.move('./SNOPT_summary.out', './SOL_#')