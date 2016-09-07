from scipy.integrate import quad
from scipy.interpolate import interp1d
import numpy as np
from math import sqrt


def stepFuncFactory(x_0, mag=1):
  def stepFunc(x):
    return   (0.5*(np.sign(x - x_0) + 1.0))*mag

  return stepFunc





class cantIBeam(object):          
  """
  A class for I beam definiation. 

  The purpose of the I Beam class is to provide a structural component
  that can be added to the aircraft class.


           Flange Width
      < ---------------- >
      ____________________
     |                    |  ^   Flange Height 
     |____________________|  v
            |      |  ^     
            |      |  |     
            |      |       
            |      |  | Web Height    
            |      |       
            |      |  |           
      ______|______|__v___            ^ Z
     |                    |           |
     |____________________|            ----> Y

            <----->
            Web Width


  Parameters
  ----------
  length : float
     lengh of the I beam in the X direction 

  E : float
      Youngs Modules of the material

  flange_dim : np.array
      list of the flange dimentions, [Flange Width, Flange Height] 

  web_dim : np.array
      list of the flange dimentions, [Flange Width, Flange Height]

  web_dim : np.array
    list of the flange dimentions, [Flange Width, Flange Height]  

    """

  def __init__(self, length, E, flange_dim, web_dim, X):
    self.length = length
    self.E = E
    self.flange_dim = flange_dim
    self.web_dim = web_dim
    self.Ry = 0.0
    self.Rm = 0.0
    self.X = X


    # self.BC = BC

    self.distLoadlist = []
    self.pointLoadFuncList = []
    self.pointMommentFuncList = []
    # print(self.distLoadlist)



    self.web_b = interp1d(self.X, self.web_dim[:,0])
    self.web_h = interp1d(self.X, self.web_dim[:,1])
    self.flange_b = interp1d(self.X, self.flange_dim[:,0])
    self.flange_h = interp1d(self.X, self.flange_dim[:,1])


  def addElipticalDistLoad(self,mag):
    # print(self.distLoadlist)
    def ellipticDist(x):
      B = mag/(np.pi*self.length)
      y = sqrt( (1 - (x/self.length)**2)*B**2 )
      return y
    self.distLoadlist.append(ellipticDist)



  def addDistLoad(self,W, X):
      # self.distLoadlist.append(np.poly1d(np.polyfit(X,W, 3)))

      self.distLoadlist.append(interp1d(X, W, kind='quadratic'))
      # return np.poly1d(np.polyfit(X,W, 4))

  def addPointLoad(self, mag, x_loc):
    self.pointLoadFuncList.append(stepFuncFactory(x_loc,mag=mag))
    self.Ry += mag

  def addPointMomment(self, mag, x_loc):
    self.pointMommentFuncList.append(stepFuncFactory(x_loc,mag=mag))
    self.Rm += mag

  def calcDistLoad(self):
    def distLoad(x):
      return sum( [func(x) for func in self.distLoadlist])

    self.distLoad = distLoad



  def calcShearForce(self):

    def pointLoadFunc(x):
      if self.pointLoadFuncList:
       return sum( [func(x) for func in self.pointLoadFuncList])
      else:
        return 0.0

    self.pointLoadFunc = pointLoadFunc

    self.Ry += quad(self.distLoad,0, self.length)[0] #+ self.__mag


    def shearForce(x):

      

      # return sum( self.pointLoadFunc(x), self.distLoad(x) )
      return  -(self.Ry - self.pointLoadFunc(x) - quad(self.distLoad,0, x)[0] )


    self.shearForce = shearForce

  
  def calcMomment(self):

    def pointMommentFunc(x):
      if self.pointMommentFuncList:
       return sum( [func(x) for func in self.pointMommentFuncList])
      else:
        return 0.0

    self.pointMommentFunc = pointMommentFunc

    self.Rm += -1*quad(self.shearForce,0, self.length)[0] #+ self.__mag


    def momment(x):

      # print x      

      # return sum( self.pointMommentFunc(x), self.distLoad(x) )
      return  (self.Rm - self.pointMommentFunc(x) + quad(self.shearForce,0, x)[0] )


    self.momment = momment



  def calcI(self):

    def I(x):
      return 1.0/12.0*(self.web_b(x)*self.web_h(x)**3 + 2*self.flange_b(x)*self.flange_h(x)**3)


    self.I = I


  def calcStress(self):
    # if Y==None:
    #   Y = (self.web_h(x)/2.0+self.flange_dim[1])

    # print(Y)


    def stress(x):
      Y = (self.web_h(x)/2.0+self.flange_h(x))
      # print(Y)

      sigma = self.momment(x)*Y/self.I(x)
      # print self.I(x)
      return sigma

    self.stress = stress


  # def C





  #   # calc reaction at 

  #   def shearForce(Ry, )


  #   self.shearForce = shearForce

  # def calcMomment(self):

  # def calcDist(self)




    

  # def addBC(self,beginning, end):

  #   if (beginning == 'clamped' and end == 'free'):


  #   return





# class cantCompositIBeam(IBeam):
#   def __init__(self, length, web_E, flange_E, flange_dim, web_dim):

#     # for theroy see 
#     # http://www.ecourses.ou.edu/cgi-bin/ebook.cgi?topic=me&chap_sec=06.1&page=theory


#     #Scalling according to equibalent Area Method 
#     web_dim[0] = web_E/flange_E * web_dim[0]

#     E = flange_E


#     super(compositIBeam, self).__init__(length, E, flange_dim, web_dim, BC)

    
#   # def 