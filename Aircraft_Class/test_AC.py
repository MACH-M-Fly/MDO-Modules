from Aircraft_class import *

# defult_tail_horz = Surface( Sref=0.125, MAC=0.25, Bref=0.5, Chord=np.array([0.3, 0.2]), Xle=np.array([1.0, 1.0]) )
# defult_tail_horz = Surface( Sref=0.125, MAC=0.25, Bref=0.5, Chord=np.array([0.3, 0.2]), Xle=np.array([1.0, 1.0]), Yle=np.array([0.0, 0.0]), Zle=np.array([0.0, 0.25]) )

defult_wing = Surface( Sref=0.5, MAC=0.5, Bref=1.0, Chord=np.array([0.6, 0.4]) )


M_8 = Aircraft()

M_8.Wing = defult_wing

print 'M_8.Wing.Afiles: ', M_8.Wing.Afiles
print 'M_8.Wing.Xle: ', M_8.Wing.Xle
print 'M_8.Wing.Yle: ', M_8.Wing.Yle
print 'M_8.Wing.Zle: ', M_8.Wing.Zle
