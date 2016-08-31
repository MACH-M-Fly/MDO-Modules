from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# from forces import thrust, tail_CL, gross_lift, g, mu_k, Sref_tail, Rho, inced_ang

Rho = 1.225 # make global
Sref_tail = 0.212
g = 9.81
mu_k = 0.005

inced_ang = -5.0 *np.pi/180.0
max_rot_ang = 10*np.pi/180.0


def runway_sim_tiny(CL, CD, CM, Sref_wing, Sref_tail, weight, boom_len, dist_LG, MAC, Iyy):

	Flapped = 0
	max_rot_ang = 10*np.pi/180.0


	#declare functions for kinimatic varibles (F = ma and M = I*ang_a)

	# super trivail func, but it helped me organize my thoughts
	def velocity(vel):
		return vel

	def acceleration(vel, ang):
		N =  weight - gross_lift(vel,ang, Sref_wing, Sref_tail, Flapped,CL)
		if N < 0:
			N = 0
		accel = (g/weight)*(thrust(vel, ang)[0] - 0.5*vel**2*Rho*CD(ang)*Sref_wing - mu_k*N)
		return accel

	def ang_velocity(a_vel, ang):
		if (ang <= 0.0 and a_vel < 0.0) :
			a = 0
		elif (ang >= max_rot_ang and a_vel > 0.0):
			a = 0
		else:
			a = a_vel


		return a

	def ang_acceleration(vel, ang, v_ang):
		q = 0.5*Rho*vel**2
		moment_tail = - q*tail_CL(ang, Flapped)*Sref_tail*(boom_len - dist_LG)
		moment_wing = q*(CM(ang)*Sref_wing*MAC+ CL(ang)*Sref_wing*dist_LG)
		# damping_moment =  -np.sign(a_vel)*0.5*Rho*a_vel**2*50*Sref_wing
		ang_accel = 1.0/(Iyy + (weight/g)*dist_LG**2)*(moment_wing+moment_tail) # +damping_moment)
		
		if (ang <= 0.0 and ang_accel < 0.0) :
			ang_accel = 0
		elif (ang >= max_rot_ang and v_ang >= 0.0):
			ang_accel = -30*v_ang
			if (abs(ang_accel) < 10**-27 and Flapped):
				ang_accel = 0

		else:

			pass

		return ang_accel

	# main loop
	i = 0

	dist = [0.0]
	vel = [0.0]
	ang = [0.0]
	ang_vel = [0.0]

	# accel = [acceleration(vel[i], ang[i ])]
	# ang_accel = [ ang_acceleration(vel[i], ang[i], ang_vel[i]) ]


	v_stall = np.sqrt(2*weight/(Rho*Sref_wing*1.7))


	time = [0.0]
	dt = 0.2
	time_elap = 0

	# DT =[dt]

	sum_y =  gross_lift(vel[i],ang[i], Sref_wing, Sref_tail, Flapped, CL) - weight

	while (sum_y <= 0.0 and time_elap < 20) :

		# F = ma yeilds two second order equations => system of 4 first order
		# runge Kutta 4th to approximate kinimatic varibles at time = time + dt
		k1_dist = dt*velocity(vel[i])
		k1_vel = dt*acceleration(vel[i],ang[i])
		k1_ang = dt*ang_velocity(ang_vel[i], ang[i])
		k1_ang_vel = dt*ang_acceleration(vel[i], ang[i], ang_vel[i])

		k2_dist = dt*velocity(vel[i] + 0.5*k1_vel)
		k2_vel = dt*acceleration(vel[i] + 0.5*k1_vel, ang[i] + 0.5*k1_ang)
		k2_ang = dt*ang_velocity(ang_vel[i] + 0.5*k1_ang, ang[i] + 0.5*k1_ang)
		k2_ang_vel = dt*ang_acceleration(vel[i] + 0.5*k1_vel, ang[i] + 0.5*k1_ang, ang_vel[i] + 0.5*k1_ang_vel)

		k3_dist = dt*velocity(vel[i] + 0.5*k2_vel)
		k3_vel = dt*acceleration(vel[i] + 0.5*k2_vel, ang[i] + 0.5*k2_ang)
		k3_ang = dt*ang_velocity(ang_vel[i] + 0.5*k2_ang, ang[i] + 0.5*k2_ang)
		k3_ang_vel = dt*ang_acceleration(vel[i] + 0.5*k2_vel, ang[i] + 0.5*k2_ang, ang_vel[i] + 0.5*k2_ang_vel)

		k4_dist = dt*velocity(vel[i] +  k3_vel)
		k4_vel = dt*acceleration(vel[i] + k3_vel, ang[i] + k3_ang)
		k4_ang = dt*ang_velocity(ang_vel[i] + k3_ang, ang[i] + k3_ang)
		k4_ang_vel = dt*ang_acceleration(vel[i] + k3_vel, ang[i] + k3_ang, ang_vel[i] + k3_ang_vel)

		dist.append(dist[i] + 1.0/6*(k1_dist + 2*k2_dist + 2*k3_dist + k4_dist))
		vel.append(vel[i] + 1.0/6*(k1_vel + 2*k2_vel + 2*k3_vel + k4_vel))
		ang.append(ang[i] + 1.0/6*(k1_ang + 2*k2_ang + 2*k3_ang + k4_ang)) 
		ang_vel.append(ang_vel[i] + 1.0/6*(k1_ang_vel + 2*k2_ang_vel + 2*k3_ang_vel + k4_ang_vel))
		# accel.append(acceleration(vel[i + 1], ang[i + 1]))
		# ang_accel.append(ang_acceleration(vel[i + 1], ang[i+ 1], ang_vel[i+1]))


		i = i + 1

		if abs(ang_vel[i])< 10**-8 and Flapped:
			ang_vel[i] = 0.0

		if ang[i] > max_rot_ang:
			ang[i] = max_rot_ang
		elif ang[i] < 0.0:
			ang[i] = 0.0


		if (vel[i] < 0.92*(v_stall+2.0)) or (abs(ang_vel[i]) == 0.0 and (ang[i] < 10**-10 or ang[i] >=max_rot_ang)) :
			dt = 0.2
		else:
			dt = 0.05
		# DT.append(dt)
		
		time.append(time[i -1] + dt)
		time_elap = time[i]

		sum_y =  gross_lift(vel[i],ang[i], Sref_wing,Sref_tail, Flapped, CL) - weight


		if vel[i] > v_stall+2.0:
			Flapped = 1
		


	# runway_len = 200 #meters

	if (sum_y > 0.0 and dist[i] <= 200.0):
		takeoff = 1
	else:
		takeoff = 0

	# ============== Ploting ===============

	# plt.figure(1)
	# plt.subplot(711)
	# plt.ylabel('Angle)')
	# plt.xlabel('time')
	# plt.plot(time, ang, 'b')

	# plt.subplot(712)
	# plt.ylabel('ang velocity')
	# plt.xlabel('time')
	# plt.plot(time, ang_vel, 'b')

	# # plt.subplot(713)
	# # plt.ylabel('ang acceleration')
	# # plt.xlabel('time')
	# # plt.plot(time, ang_accel, 'b')

	# plt.subplot(714)
	# plt.ylabel('distance')
	# plt.xlabel('time')
	# plt.plot(time, dist, 'b')

	# plt.subplot(715)
	# plt.ylabel('Velocity')
	# plt.xlabel('time')
	# plt.plot(time, vel, 'b')

	# # plt.subplot(716)
	# # plt.ylabel('Acceleration')
	# # plt.xlabel('time')
	# # plt.plot(time, accel, 'b')

	# # plt.subplot(717)
	# # plt.ylabel('dt')
	# # plt.xlabel('time')
	# # plt.plot(time, DT, 'b')
	# plt.show()

	
	# print('Takeoff:' + str(takeoff))
	# print('Distance: ' + str(dist[i]))
	# print('vel: ' + str(vel[i]))
	# print('ang: ' + str(ang[i]*180.0/np.pi) + ' max_rot_ang: ' + str(max_rot_ang*180.0/np.pi))
	# print('ang_vel: ' + str(ang_vel[i]))
	# print('time: ' + str(time[i]))
	# print('steps: ' + str(len(time)))
	# print('\n')

	return (takeoff, dist[i], vel[i], ang[i], ang_vel[i], time[i])




















































































































































































































































































































































































































































































































































































































































































































