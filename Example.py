#By: Santosh Katuwal
#RCrectSec.py should be saved in the same working directory

from openseespy.opensees import *
import openseespy.postprocessing.ops_vis as opsv
import numpy as np
import RCrectSec #Importing RCrectSec.py 


wipe()
#   model('BasicBuilder', '-ndm', ndm, '-ndf', ndf)
model('BasicBuilder', '-ndm', 3, '-ndf', 6)  # ndm: spatial dimension; ndf: DoF per node

#%% DEFINING MATERIALS

# Definition of materials IDs
C_unconf = 1
C_conf = 2
R_steel = 3

# Basic parameters for materials
#concrete parameters in compression
fc1 = -25000 #f'c of unconfined concrete; -ve sign indicates compression
fc2 = -28000 #f'c of confined concrete
epsc = -0.002#strain at maximum stress in compression
fu1 = fc1 * 0.2#ultimate stress for unconfined concrete
fu2 = fc2 * 0.2#ultimate stress for confined concrete
epsu = -0.02 #strain at ultimate stress of concrete
Lambda = 0.1 #unloading stiffness to initial stiffness ratio in comprssion
#Concrete parameters in tension
ft1 = fc1 * -0.1 #maximun tension stress for unconfined concrete; multipying it by 
                #negative sign creates positive value (+ve value represents tension)
ft2 = fc2 * -0.1 #maximun tension stress for confined concrete
Et1 = ft1 / 0.002 #Elastic modulus of unconfied concrete in tension
Et2 = ft2 / 0.002 #Elastic modulus of confined concrete in tension
#Rebar parameters
fy = 420000 #fy of steel
Es = 210000000 #Young's modulus of elasticity for steel
b = 0.005 #Strain hardening ratio
#smoothness coefficient for elastic to plastic transition of stress strain diagram of steel
R0 = 20 
cR1 = 0.925
cR2 = 0.15

# Define unconfined concrete material
uniaxialMaterial('Concrete02', C_unconf, fc1 , epsc , fu1, epsu, Lambda, ft1, Et1)

# Define confined concrete material
uniaxialMaterial('Concrete02', C_conf  , fc2 , epsc , fu2, epsu, Lambda, ft2, Et2)

# Define steel material
# uniaxialMaterial('Steel02', matTag, Fy, E0, b, R0, cR1, cR2)
uniaxialMaterial('Steel02', R_steel, fy, Es, b, R0, cR1, cR2)

#%% DEFINING SECTIONS
# Define sections IDs
Col300x400 = 1
Beam300x600 = 2

# Define dimensions
pi = np.pi
Rebar_25 = pi * 0.025 * 0.025 / 4  # area rebar 25mm
b_col = 0.3  # column base
h_col = 0.4  # column height
r_col = 0.04  # column cover
b_beam = 0.3  # beam base
h_beam = 0.6  # beam height
r_beam = 0.04  # beam cover
nfCoreY = 8
nfCoreZ = 8
nfCoverY = 8
nfCoverZ = 8

# Define the torsional stiffness
GJ_col = 10000  # Specify the torsional stiffness (modify with appropriate value)
GJ_beam = 10000 
# RCrectSec.py must be imported to execute this command
RCrectSec.buildRCrectsection(Col300x400, h_col, b_col,GJ_col, r_col, r_col, C_conf, C_unconf, R_steel, 3, Rebar_25, 3, Rebar_25, 4, Rebar_25, nfCoreY, nfCoreZ, nfCoverY,nfCoverZ)
RCrectSec.buildRCrectsection(Beam300x600, h_beam, b_beam, GJ_beam, r_beam, r_beam, C_conf, C_unconf, R_steel, 3, Rebar_25, 3, Rebar_25, 4, Rebar_25, nfCoreY, nfCoreZ, nfCoverY,nfCoverZ)
