'''
Work that still needs to be done:

- Fueselage (slender body)
- Fueselage (collection of surfaces)
- Component surfaces
- Control surfaces
- Mass declaration
- Any other geometric calculation
- Optimization of AVL runs





'''



import os
import sys
import math
from AVL_py import AVL

class AC():
	''' Aircraft Configuration class, abstraction of aircraft config'''
	# SECTION = WING/AIRFOIL CROSS SECTION
	def __init__(self, name):

		# proper contains the following info in the following order:
		# MACH, IYSym, IZsym, ZSym, Sref, Cref, Bref, Xref, Yref, Zref
		self.name = name
		self.proper = {'MACH' : 0, 'IYsym' : 0, 'IZsym' : 0, 'Zsym' : 0, 'Sref' : 0, 'Cref': 0, 'Bref': 0, 'Xref' : 0, 'Yref' : 0, 'Zref' : 0}
		self.wing = {'Num' : 0} 
		self.h_tail = {'Num' : 0}
		self.v_tail = {'Num' : 0}
		self.fuselage = {'Num' : 0}
		self.boom = {'Num': 0}
		self.other_surfaces = {'Num' : 0}
		self.AVL = AVL(name)

	def update_prop(self):
		# Update properties such as Sref and Bref

		#------------Sref-------------------------
		self.proper['Sref'] = 0.0
		print(self.wing['Num']) 
		for num_wing in range(self.wing['Num']):
			wing_sref = 0.0
			key_start = 'wing_' + str(num_wing+1)
			height = self.wing[key_start]['wingspan']/(self.wing[key_start]['num_sections']-1)
			for i in range(self.wing[key_start]['num_sections']-1):
				taper1 = self.wing[key_start]['taper'][i] * self.wing[key_start]['root_chord']
				taper2 = self.wing[key_start]['taper'][i+1] * self.wing[key_start]['root_chord']
				area = (taper1 + taper2) * height
				wing_sref = wing_sref + area
			self.proper['Sref'] = self.proper['Sref'] + wing_sref

		#------------Bref-------------------------
		self.proper['Bref'] = 0.0
		for num_wing in range(self.wing['Num']):
			if num_wing == 0:
				key_start = 'wing_' + str(num_wing+1)
				self.proper['Bref'] = self.wing[key_start]['wingspan']

	def add_wing(self, name, airfoil, root_chord, wingspan, num_sections , offset):
		''' Assumes symmetric wing '''
		# proper contains the following info in the following order:
		# Num_sections, Nchordwise, Cspace, Nspanwise, Sspace, COMPONENT, YDUPLICATE, ANGLE, SCALEX, SCALEY, SCALEZ, TRANSX, TRANSY, TRANSZ]
		# All airfoil, sweep, dihedral, and taper variables need to be arrays size of the number of sections
		# wingspan and root_chord is a single word
		# In the future: Control surfaces
		size_array_1 = []
		for num in range(num_sections):
			size_array_1.append(1)
		size_array_0 = []
		for num in range(num_sections):
			size_array_0.append(0)
		size_array_offset = []
		for num in range(num_sections):
			size_array_offset.append(offset)
		size_array_airfoil = []
		if not (isinstance(airfoil, list)):
			for num in range(num_sections):
				size_array_airfoil.append(airfoil)
		else:
			size_array_airfoil = airfoil


		new_wing = {'name' : name}
		new_wing['num_sections'] = num_sections
		new_wing['proper'] = [10, 1.0, 30, -2.0, 1, 0, 0, 1, 1, 1, 0, 0, 0]
		new_wing['root_chord'] = root_chord
		new_wing['airfoil'] = size_array_airfoil # if constant, only put in one, otherwise put in entire array
		new_wing['angle'] = size_array_0
		new_wing['X_offset'] = size_array_offset
		new_wing['wingspan'] = wingspan
		new_wing['taper'] = size_array_1
		new_wing['dihedral'] = size_array_0

		wing_key = 'wing_' + str(self.wing['Num'] + 1)

		self.wing[wing_key] = new_wing
		self.wing['Num'] = self.wing['Num'] + 1

	def add_h_tail(self, name, airfoil, root_chord, wingspan, num_sections, offset ):
		''' Assumes symmetric h_tail '''
		# proper contains the following info in the following order:
		# Num_sections, Nchordwise, Cspace, Nspanwise, Sspace, COMPONENT, YDUPLICATE, ANGLE, SCALEX, SCALEY, SCALEZ, TRANSX, TRANSY, TRANSZ]
		# All airfoil, sweep, and taper variables need to be arrays size of the number of sections
		# wingspan and root_chord is a single word
		# In the future: Control surfaces
		size_array_1 = []
		for num in range(num_sections):
			size_array_1.append(1)
		size_array_0 = []
		for num in range(num_sections):
			size_array_0.append(0)
		size_array_airfoil = []
		if not isinstance(airfoil, list) == 1:
			for num in range(num_sections):
				size_array_airfoil.append(airfoil)
		else:
			size_array_airfoil = airfoil
		size_array_offset = []
		for num in range(num_sections):
			size_array_offset.append(offset)


		new_wing = {'name' : name}
		new_wing['num_sections'] = num_sections
		new_wing['proper'] = [10, 1.0, 30, -2.0, 1, 0, 0, 1, 1, 1, 0, 0, 0]
		new_wing['root_chord'] = root_chord
		new_wing['airfoil'] = size_array_airfoil
		new_wing['angle'] = size_array_0
		new_wing['X_offset'] = size_array_offset
		new_wing['wingspan'] = wingspan
		new_wing['taper'] = size_array_1
		new_wing['dihedral'] = size_array_0
		wing_key = 'h_tail_' + str(self.h_tail['Num'] + 1)

		self.h_tail[wing_key] = new_wing
		self.h_tail['Num'] = self.h_tail['Num'] + 1

	def add_v_tail(self, name, airfoil, root_chord, wingspan, num_sections, offset, offset_y ):
		''' Assumes symmetric h_tail '''
		# proper contains the following info in the following order:
		# Num_sections, Nchordwise, Cspace, Nspanwise, Sspace, COMPONENT, YDUPLICATE, ANGLE, SCALEX, SCALEY, SCALEZ, TRANSX, TRANSY, TRANSZ]
		# All airfoil, sweep, and taper variables need to be arrays size of the number of sections
		# wingspan and root_chord is a single word
		# In the future: Control surfaces

		size_array_1 = []
		for num in range(num_sections):
			size_array_1.append(1)
		size_array_0 = []
		for num in range(num_sections):
			size_array_0.append(0)
		size_array_offset = []
		for num in range(num_sections):
			size_array_offset.append(offset)
		size_array_offset_y = []
		for num in range(num_sections):
			size_array_offset_y.append(offset_y)
		size_array_airfoil = []
		if not isinstance(airfoil, list):
			for num in range(num_sections):
				size_array_airfoil.append(airfoil)
		else:
			size_array_airfoil = airfoil

		# print('Offset: '+str(offset)+"\n")
		# print('Offset Y: '+str(offset_y)+"\n")

		new_wing = {'name' : name}
		new_wing['num_sections'] = num_sections
		new_wing['proper'] = [10, 1.00, 10, -2.0, 1, 0, 0, 1, 1, 1, 0, 0, 0]
		new_wing['root_chord'] = root_chord
		new_wing['airfoil'] = size_array_airfoil # if constant, only put in one, otherwise put in entire array
		new_wing['angle'] = size_array_0
		new_wing['X_offset'] = size_array_offset
		new_wing['wingspan'] = wingspan
		new_wing['taper'] = size_array_1
		new_wing['dihedral'] = size_array_0
		new_wing['Y_offset'] = size_array_offset_y
		wing_key = 'v_tail_' + str(self.v_tail['Num'] + 1)

		self.v_tail[wing_key] = new_wing
		self.v_tail['Num'] = self.v_tail['Num'] + 1

	def add_boom(self, density, length):

		self.boom['Boom_'+str(self.boom['Num']+1)] = {'boom_length' : length, 'density': density}
		self.boom['Num'] = self.boom['Num'] + 1


	def create_AVL_geometry(self):
		with open('Output/'+str(self.name)+'.avl', 'w') as geo:
			geo.write(str(self.name))
			#Initial first 4 lines
			geo.write('\r\n#Mach\r\n')
			geo.write(str(self.proper['MACH'])+'\r\n')
			geo.write('#IYsym\tIZsym\tZsym\r\n')
			geo.write(str(self.proper['IYsym'])+' '+str(self.proper['IZsym'])+' '+str(self.proper['Zsym']) + '\r\n\r\n')
			geo.write('#Sref\tCref\tBref\r\n')
			geo.write(str(self.proper['Sref'])+' '+str(self.proper['Yref'])+' '+str(self.proper['Bref']) + '\r\n\r\n')
			geo.write('#Xref\tYref\tZref\r\n')
			geo.write(str(self.proper['Xref'])+' '+str(self.proper['Yref'])+' '+str(self.proper['Zref'])+'\r\n\r\n')
			geo.write('#---------------------------------------------------------\r\n')

			geo.write('#---------------------------------------------------------\r\n')
			geo.write('# WING(s)                                                    \r\n')
			geo.write('#---------------------------------------------------------\r\n')

			for i in range(self.wing['Num']):
				geo.write('SURFACE\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['name']))
				geo.write('\r\n')
				geo.write('#Nchordwise\tCspace\tNspanwise\tSspace\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][0])+' '+str(self.wing['wing_'+str(i+1)]['proper'][1])+' '+str(self.wing['wing_'+str(i+1)]['proper'][2])+' '+str(self.wing['wing_'+str(i+1)]['proper'][3])+'\r\n')
				geo.write('COMPONENT\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][4])+'\r\n')
				geo.write('YDUPLICATE\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][5])+'\r\n')
				geo.write('ANGLE\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][6])+'\r\n')
				geo.write('SCALE\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][7])+'\t'+str(self.wing['wing_'+str(i+1)]['proper'][8])+'\t'+str(self.wing['wing_'+str(i+1)]['proper'][9])+'\r\n')
				geo.write('TRANSLATE\r\n')
				geo.write(str(self.wing['wing_'+str(i+1)]['proper'][10])+'\t'+str(self.wing['wing_'+str(i+1)]['proper'][11])+'\t'+str(self.wing['wing_'+str(i+1)]['proper'][12])+'\r\n')

				wingspan = self.wing['wing_'+str(i+1)]['wingspan']
				num_sections = self.wing['wing_'+str(i+1)]['num_sections']
				for j in range(num_sections):
					taper_sec = 1.0
					for k in range(j):
						taper_sec = taper_sec * self.wing['wing_'+str(i+1)]['taper'][k]
					geo.write('SECTION\r\n')
					geo.write('#Xle\tYle\tZle\tChord\tAinc\tNspanwise\tSspace\r\n')
					geo.write(str(self.wing['wing_'+str(i+1)]['X_offset'][j])+' '+str(wingspan* j / (num_sections - 1))+' '+str(math.sin(self.wing['wing_'+str(i+1)]['dihedral'][j]) * wingspan / (num_sections - 1)) +' '+str(taper_sec * self.wing['wing_'+str(i+1)]['root_chord'])+' '+str(self.wing['wing_'+str(i+1)]['angle'][j])+'\r\n')
					geo.write('AFILE\r\n')
					geo.write('Airfoil/'+str(self.wing['wing_'+str(i+1)]['airfoil'][j])+'\r\n\r\n')

			geo.write('#---------------------------------------------------------\r\n')
			geo.write('# Horizontal Tail(s)                                                    \r\n')
			geo.write('#---------------------------------------------------------\r\n')

			for i in range(self.h_tail['Num']):
				geo.write('SURFACE\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['name']))
				geo.write('\r\n')
				geo.write('#Nchordwise\tCspace\tNspanwise\tSspace\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][0])+' '+str(self.h_tail['h_tail_'+str(i+1)]['proper'][1])+' '+str(self.h_tail['h_tail_'+str(i+1)]['proper'][2])+' '+str(self.h_tail['h_tail_'+str(i+1)]['proper'][3])+'\r\n')
				geo.write('COMPONENT\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][4])+'\r\n')
				geo.write('YDUPLICATE\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][5])+'\r\n')
				geo.write('ANGLE\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][6])+'\r\n')
				geo.write('SCALE\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][7])+'\t'+str(self.h_tail['h_tail_'+str(i+1)]['proper'][8])+'\t'+str(self.h_tail['h_tail_'+str(i+1)]['proper'][9])+'\r\n')
				geo.write('TRANSLATE\r\n')
				geo.write(str(self.h_tail['h_tail_'+str(i+1)]['proper'][10])+'\t'+str(self.h_tail['h_tail_'+str(i+1)]['proper'][11])+'\t'+str(self.h_tail['h_tail_'+str(i+1)]['proper'][12])+'\r\n')

				wingspan = self.h_tail['h_tail_'+str(i+1)]['wingspan']
				num_sections = self.h_tail['h_tail_'+str(i+1)]['num_sections']
				for j in range(num_sections):
					print(self.h_tail['h_tail_'+str(i+1)]['X_offset'])
					geo.write('SECTION\r\n')
					geo.write('#Xle\tYle\tZle\tChord\tAinc\tNspanwise\tSspace\r\n')
					geo.write(str(self.h_tail['h_tail_'+str(i+1)]['X_offset'][j])+' '+str(wingspan* j / (num_sections - 1))+' '+str(math.sin(self.h_tail['h_tail_'+str(i+1)]['dihedral'][j]) * wingspan / (num_sections - 1)) +' '+str(self.h_tail['h_tail_'+str(i+1)]['taper'][j] * self.h_tail['h_tail_'+str(i+1)]['root_chord'])+' '+str(self.h_tail['h_tail_'+str(i+1)]['angle'][j])+'\r\n')
					geo.write('AFILE\r\n')
					geo.write('Airfoil/'+str(self.h_tail['h_tail_'+str(i+1)]['airfoil'][j])+'\r\n\r\n')

			geo.write('#---------------------------------------------------------\r\n')
			geo.write('# Vertical Tail(s)                                                    \r\n')
			geo.write('#---------------------------------------------------------\r\n')

			for i in range(self.v_tail['Num']):
				geo.write('SURFACE\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['name']))
				geo.write('\r\n')
				geo.write('#Nchordwise\tCspace\tNspanwise\tSspace\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][0])+' '+str(self.v_tail['v_tail_'+str(i+1)]['proper'][1])+' '+str(self.v_tail['v_tail_'+str(i+1)]['proper'][2])+' '+str(self.v_tail['v_tail_'+str(i+1)]['proper'][3])+'\r\n')
				geo.write('COMPONENT\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][4])+'\r\n')
				geo.write('YDUPLICATE\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][5])+'\r\n')
				geo.write('ANGLE\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][6])+'\r\n')
				geo.write('SCALE\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][7])+'\t'+str(self.v_tail['v_tail_'+str(i+1)]['proper'][8])+'\t'+str(self.v_tail['v_tail_'+str(i+1)]['proper'][9])+'\r\n')
				geo.write('TRANSLATE\r\n')
				geo.write(str(self.v_tail['v_tail_'+str(i+1)]['proper'][10])+'\t'+str(self.v_tail['v_tail_'+str(i+1)]['proper'][11])+'\t'+str(self.v_tail['v_tail_'+str(i+1)]['proper'][12])+'\r\n')

				wingspan = self.v_tail['v_tail_'+str(i+1)]['wingspan']
				num_sections = self.v_tail['v_tail_'+str(i+1)]['num_sections']
				for j in range(num_sections):
					geo.write('SECTION\r\n')
					geo.write('#Xle\tYle\tZle\tChord\tAinc\tNspanwise\tSspace\r\n')
					geo.write(str(self.v_tail['v_tail_'+str(i+1)]['X_offset'][j])+' '+str(self.v_tail['v_tail_'+str(i+1)]['Y_offset'][j]) +' '+str(wingspan* j / (num_sections - 1))+' '+str(self.v_tail['v_tail_'+str(i+1)]['taper'][j] * self.v_tail['v_tail_'+str(i+1)]['root_chord'])+' '+str(self.v_tail['v_tail_'+str(i+1)]['angle'][j])+'\r\n')
					geo.write('AFILE\r\n')
					geo.write('Airfoil/'+str(self.v_tail['v_tail_'+str(i+1)]['airfoil'][j])+'\r\n\r\n')
		return

#	def add_fuselage(self):# Treat fuselage as 3 surfaces: Vertical top, vertical bottom, horizontal X-section
#	def add_other_surface(self):


	

