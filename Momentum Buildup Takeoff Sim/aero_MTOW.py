'''
aero_MTOW.py: Runs takeoff simulation to determine MTOW



Still undershooting by A LOT (max payload around 5 lbs), but behaves normally
Think some units are wrong somewhere




'''

from __future__ import print_function
from openmdao.api import Component, Group, Problem

# Imported from Python standard
import sys
import os
import time
import math
import numpy
from  AVL_py import AVL

runway_length = 200 	#[ft]
rho = 0.0765 			#[lbm/ft^3]
g = 9.81 * 3.28 		#[ft/s^2]
mu = 0.005

import settings

class aero_MTOW(Component):
	""" Makes the appropriate run file and outputs the computed numbers """
	def __init__(self):

		super(aero_MTOW, self).__init__()

		self.add_param('CL', val = 0.0);
		self.add_param('CD', val = 0.0);
		#self.add_param('friction-coeff', val = 0.0)
		self.add_param('Sref', val = 0.0)
		self.add_param('EW', val = 2.0); # lbs
		# self.add_param('T0', val = 0.0)
		# self.add_param('T1', val = 0.0)
		# self.add_param('T2', val = 0.0)
		# self.add_param('T3', val = 0.0)
		# self.add_param('T4', val = 0.0)

		self.add_output('MTOW', val = 0.0)
		self.add_output('TO_time', val = 0.0)
		self.add_output('TO_length', val = 0.0)
		self.add_output('TO_vel', val = 0.0)
		self.add_output('PAYLOAD', val = 0.0)

		

	def solve_nonlinear(self, params, unknowns, resids):
		T0 = 12.756 
		T1 = -0.0941 * 3.28  
		T2 = 0.0023  *( 3.28 ** 2)
		T3 = -7*(10**-5) *( 3.28 ** 3)
		T4 = 4*(10**-7) * (3.28 ** 4)
		T_coeff = [T0, T1, T2, T3, T4] # All lbf

		#================================================
		# Function declarations
		#================================================
		def calc_total_force(v, CL, CD, Sref, mass, T_coeff, alpha):
			''' Calculates both the horizontal and vertical forces at specified conditions '''

			
			T0 = T_coeff[0]
			T1 = T_coeff[1]
			T2 = T_coeff[2]
			T3 = T_coeff[3]
			T4 = T_coeff[4]

			Ft = (T0 + T1 * v + T2 * v ** 2 + T3 * v ** 3 + T4 * v ** 4) 
			#print(str(Ft)+'\n')
			if  Ft < 0:
				Ft = 0

			# Lift	
			Fl = 0.5 * rho *( v ** 2) * Sref * CL

			# Drag 
			Fd = 0.5 * rho * (v ** 2) * Sref * CD

			# Wheel Friction
			Fw = mu * ( mass * g - Fl) * 0.225
			if Fw <= 0:
				Fw = 0


			# print('Ft: ' + str(Ft) + ' Fl: ' + str(Fl) + ' Fd: ' + str(Fd) + ' Fw: '+str(Fw) + '\n')
 
			F = []
			if Fw > (Ft + Fd):
				F.append(0)
			else:
				F.append(Ft - Fw - Fd)
			
			Fy = Fl - mass * g

			# print(str(Fl) + ' ' + str(mass*g))
			if Fy < 0:
				F.append(0)
			else:
				F.append(Fy)
				#print(Fy)
			# print('F: ' + str(F) + '\n')
			return F

		def calc_momentum_buildup(runway_length, mass, CL, CD, Sref, T_coef,T):
			''' Calculates the runway length of the aircraft w/ specified properties '''
			 # Mass is independent variable
			 # Runway length is dependent variable
			 # ALL VARIABLES HAVE TO BE IMPERIAL UNITS
			 # Newton's method step varying mass and getting runway length

			position = [0, 0] 	#[ft] X, Y
			velocity = [0, 0] 	#[ft/s] X, Y
			force = [] 		#[lbf] X, Y
			time = 0 			#[s]
			dt = 0.0001

			while  position[1] == 0 and time < 200:

				# print('Time: ' + str(time) + ' Position: ' + str(position) + ' Velocity: ' + str(velocity) + '\n')
				prev_velo = velocity
				#position[0] = position[0] + velocity[0] * dt
			 	#position[1] = position[1] + velocity[1] * dt
				
			 	force = calc_total_force(velocity[0], CL, CD,Sref, mass, T_coef, 0)
				temp_velocity = [0, 0]
				temp_velocity[0] = velocity[0] + force[0] * dt / mass
				temp_velocity[1] = velocity[1] + force[1] * dt / mass
				force2 = calc_total_force(temp_velocity[0], CL, CD, Sref, mass, T_coef, 0)
				
			 	velocity[0] = velocity[0] + (force[0]+force2[0]) * dt / mass /2
			 	velocity[1] = velocity[1] + (force[1]+force2[1]) * dt / mass /2
				
				position[0] = position[0] + (prev_velo[0]) * dt + 1/4 * (force[0] + force2[0]) / mass * (dt ** 2) 
				position[1] = position[1] + (prev_velo[1]) * dt + 1/4 * (force[1] + force2[1]) / mass * (dt ** 2) 
				#print(str(velocity)+'\n')
			 	time = time + dt

			set_all = {'time': time, 'length':position[0], 'vel_X':velocity[0]}
			print(set_all)
			return set_all

		#=================================
		# End of function declaring
		#=================================
		
		# #====================
		# # Secant Method w/ Modifications to limits
		# #====================
		# empty_mass = 2		# [lbs]
		# starting_payload = 2	# [lbs]

		# total_mass = empty_mass + starting_payload
		# starting_1 = calc_momentum_buildup(runway_length, total_mass, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
		# total_mass = total_mass + 0.001
		# starting_2 = calc_momentum_buildup(runway_length, total_mass, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
		
		# tol_MTOW = starting_2['length'] - runway_length 
		# deriv = starting_2['length'] - starting_1['length'] / 0.001
		# prev_mass = total_mass
		# previous = starting_2
		# # print('tol: ' + str(tol_MTOW) + '\n')

		# while abs(tol_MTOW) >  0.01:  
		# 	if previous['time'] >= 400:
		# 		next_mass = 0.001
		# 	# elif prev_mass == 0.001:
		# 	#  	next_mass = 0.002
		# 	# elif prev_mass == 0.0001:
		# 	# 	next_mass = 0.0002
		# 	else:
		# 		next_mass = prev_mass - (previous['length'] - runway_length)/deriv

		# 	if next_mass < 0:
		# 		next_mass = 0.01

		# 	if  next_mass > 1000:
		# 		next_mass = 100
		# 	# print(str(next_mass) + '\n')
		# 	next_total = calc_momentum_buildup(runway_length, next_mass, params['CL'], params['CD'], params['Sref'], T_coeff, T0)

		# 	deriv = (next_total['length'] - previous['length'])/(next_mass - prev_mass)
		# 	tol_MTOW = (next_total['length'] - runway_length)
		# 	prev_mass = next_mass
		# 	previous = next_total
		# 	print('Takeoff mass '+str(prev_mass) + '\n')
		# # while previous < 200:
		# # 	prev_mass = prev_mass + 0.001
		# # 	next_total = calc_momentum_buildup(runway_length, prev_mass, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
		# # 	previous = next_total['length']
		# # 	# print(previous)

		#=========================
		# Binary Search
		#=========================

		beg = 0.0001
		end = 20.0
		interval = end - beg

		# start1 = calc_momentum_buildup(runway_length, beg, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
		# start2 = calc_momentum_buildup(runway_length, end, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
		start_m = calc_momentum_buildup(runway_length, (beg + end)/2, params['CL'], params['CD'], params['Sref'], T_coeff, T0)

		tol_1 = start_m['length'] - runway_length
		# tol_2 = start2['length'] - runway_length

		while abs(tol_1) > 0.01:
			if start_m['length'] < 200:
				beg = beg + interval / 2.0
				# start1 = calc_momentum_buildup(runway_length, beg, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
			else:
				end = end - interval / 2.0
				
			start_m = calc_momentum_buildup(runway_length, (beg + end)/2.0, params['CL'], params['CD'], params['Sref'], T_coeff, T0)
			
			
			interval = end - beg


			print('B: '+str(beg)+' E: '+str(end)+' INT: '+str(interval)+' B_m: '+str(start_m['length'])+ '\n')
			
			
			tol_1 = start_m['length'] - runway_length
			
		prev_mass = (beg + end)/2.0
#		log_A = open('AGP_Part.csv', 'a')
#		log_A.write(str(params['taper']) + ',' + str(params['chord_w']) + ',' + str(params['b_w']) + ',' + str(params['prev_mass']) + '\n' )
#		log_A.close()
		previous = start_m
		# if abs(tol_1) > 0.001:
		# 	prev_mass = beg
		# 	previous = start1
		# else:
		# 	prev_mass = end
		# 	previous = start2







		# End
		payload = prev_mass - params['EW']

		
		unknowns['MTOW'] = prev_mass
		unknowns['TO_time'] = previous['time']
		unknowns['TO_length'] = previous['length']
		unknowns['TO_vel'] = previous['vel_X']
		unknowns['PAYLOAD'] = payload

		







			 	
