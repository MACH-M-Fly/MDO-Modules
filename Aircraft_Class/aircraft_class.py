import numpy as np



class Surface():
  """Surface"""
  def __init__(self, Sref, MAC, Bref,  numSections= None,\
               Afiles=[], Chord = np.array([]), Xle = np.array([]), Yle = np.array([]), Zle = np.array([]), Ainc=np.array([]), ):
    # super(Surface, self).__init__()

    if (numSections is None ) and (Afiles or Chord.any() or  Xle.any() or  Yle.any() or  Zle.any() or  Ainc.any() ):
      numSections = max(len(Chord), len(Xle),  len(Yle),  len(Zle),  len(Ainc))


    print    (Xle.any())   

    if Afiles == []:
      Afiles = ['NACA2412']*numSections
    if not(Chord.any()):
      Chord = np.ones(numSections)
    if not(Xle.any()):
      Xle = np.zeros(numSections)
    if not(Yle.any()):
      Yle = np.linspace(0.0, Bref/2.0 , num=numSections)
    if not(Zle.any()):
      Zle = np.zeros(numSections)
    if not(Ainc.any()):
      Ainc=np.zeros(numSections)


    if Sref is None:
      Sref = self.calcSref()

    self.Sref = Sref
    self.MAC = MAC
    
    self.Bref = Bref
    self.Afiles = Afiles

    self.Chord = Chord

    self.Xle = Xle
    self.Yle = Yle
    self.Zle = Zle

    self.Ainc = Ainc



  def calcSref(self, norm='z'):
    dirct = { 'x':[self.Yle,  self.Zle],
              'y':[self.Zle,  self,Xle],
              'z':[self.Xle,  self.Yle]}

    self.Sref = 0
    for i in xrange(len(numSections-1)):
      self.Sref += (dirct[norm][0][i+1] - sdirct[norm][0][i])/2.0*(dirct[norm][1][i] + dirct[norm][1][i+1])

    return

  def calcMAC(self, norm='z'):
    dirct = { 'x':[self.Zle],
              'y':[self,Xle],
              'z':[self.Yle]}


    def shape_func(y,A,B):
      return ( A**2*y - A*(A-B)/(self.Bref/4)*y**2 + (A - B)**2/(3*(self.Bref/4)**2)*y**3)

    self.MAC = 0
    for i in xrange(len(numSections)):
      self.MAC += 2.0/Sref_wing*(shape_func(dirct[norm][0][i+1], self.Chord[i], self.Chord[i+1]) - shape_func(dirct[norm][0][i], self.Chord[i], self.Chord[i+1]))
      # print(MAC)

    return

  def calcChord_from_taper(self, Taper):

    for i in range(1, len(numSections)):
      self.Chord[i] = self.Chord[i - 1]*Taper[i]

    return

  def addControlSurface(self, secStart, secEnd, hvec, name):

    self.controlSurf = name
    self.control_secStart = secStart
    self.control_secEnd = secEnd
    self.control_hvec = hvec

    return

  def addSpar(self):
    pass


class Body():
  def __init__(self, Bfile, translate = [0, 0, 0], scale = [1, 1, 1] ):

    self.Bfile
    self.translate
    self.scale

  def getVolume(self):
    pass 
    return


class Aircraft():
  def __init__(self):

                     # Wing= defult_wing, Tail_Horz=defult_tail_horz, Tail_Vert=defult_tail_vert,\
                     # X_cg=0.0, Y_cg=0.0, Z_cg=0.0, CD_p=0.0):

    self.CD_p = 0.0

    # self.Wing = Wing
    # self.Tail_Horz = Tail_Horz                
    # self.Tail_Vert = Tail_Vert

  def  convertUints(self):
    pass
    return

  def calcMass(self):
    pass
    return

  def calcI(self):
    pass
    return





# defult_wing = Surface( Sref=0.5, MAC=0.5, Bref=1.0, Chord=np.array([0.6, 0.4]) )
# defult_tail_horz = Surface( Sref=0.125, MAC=0.25, Bref=0.5, Chord=np.array([0.3, 0.2]), Xle=np.array([1.0, 1.0]) )
# defult_tail_horz = Surface( Sref=0.125, MAC=0.25, Bref=0.5, Chord=np.array([0.3, 0.2]), Xle=np.array([1.0, 1.0]), Yle=np.array([0.0, 0.0]), Zle=np.array([0.0, 0.25]) )


# print(defult_wing.Yle)


