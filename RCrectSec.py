	#Build fiber rectangular RC section, 1 steel layer top, 1 bot, 1 skin, confined core
	# Import 'RCrectSec.py' file which generates a rectangular reinforced concrete section
	# with one layer of steel at the top & bottom, skin reinforcement and a 
	# confined core.
    #Modified By: Santosh Katuwal
    #Adopted from: 1. Silvia Mazzoni, 2006 & 2. Michael H. Scott, 2003


    #                        y
	#                        ^
	#                        |     
	#             ----------------------     .---
	#             |   o     o      o   |     |-- cover_depth
	#             |                    |     |
	#             |   o            o   |     |
	#      z <--- |          +         |     D
	#             |   o            o   |     |
	#             |                    |     |
	#             |   o  o   o  o  o   |     |-- cover_depth
	#             ---------------------      .---
	#             |--------- B --------|
	#             |---| cover_width|---|
	#
	#                       y
	#                       ^
	#                       |    
	#             ----------------------
	#             |\      cover        /|
	#             | \------Top--------/ |
	#             |c|                 |c|
	#             |o|                 |o|
	#  z <-----   |v|       core      |v|  d
	#             |e|                 |e|
	#             |r|                 |r|
	#             | /-------Bot------ \ |
	#             |/      cover        \|
	#             ---------------------

#    secTag - identifier for the section generated by this procedure
#    D - section depth along the local y-axis
#    B - section width along the local z-axis
#    GJ- linear-elastic torsional stiffness
#    cover_depth- distance from the section boundary to the neutral axis of reinforcement
#    cover_width - distance from the section boundary to the side of reinforcement
#    coreMatTag - material identifier for the core patch
#    coverMatTag - material identifier for the cover patches
#    steelMatTag - material identifier for the reinforcing steel
#    numBarsTop - number of reinforcing bars in the top layer
#    numBarsBot - number of reinforcing bars in the bottom layer
#    numBarsIntTot - total number of reinforcing bars on the intermediate layers, symmetric about the z-axis with 2 bars per layer (must be an even integer)
#    barAreaTop - cross-sectional area of each reinforcing bar in the top layer
#    barAreaBot - cross-sectional area of each reinforcing bar in the bottom layer
#    barAreaInt - cross-sectional area of each reinforcing bar in the intermediate layer
#    nfCoreY - number of fibers in the core patch in the y-direction
#    nfCoreZ - number of fibers in the core patch in the z-direction
#    nfCoverY - number of fibers in the cover patches with long sides in the y-direction
#    nfCoverZ - number of fibers in the cover patches with long sides in the z-direction



from openseespy.opensees import *
import openseespy.postprocessing.ops_vis as opsv

def buildRCrectsection(secTag, D, B,GJ, cover_depth, cover_width, coreMatTag, coverMatTag, steelMatTag, numBarsTop, barAreaTop, numBarsBot, barAreaBot, numBarsIntTot, barAreaInt, nfCoreY, nfCoreZ, nfCoverY, nfCoverZ):

    coverY = D / 2.0
    coverZ = B / 2.0
    coreY = coverY - cover_depth
    coreZ = coverZ - cover_width
    numBarsInt = numBarsIntTot / 2

    # Define the fiber section
    section('Fiber', secTag,'-GJ', GJ)

    # Define the core patch
    patch('quad', coreMatTag, nfCoreZ, nfCoreY, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)

    # Define the four cover patches
    patch('quad', coverMatTag, 2, nfCoverY, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    patch('quad', coverMatTag, 2, nfCoverY, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    patch('quad', coverMatTag, nfCoverZ, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    patch('quad', coverMatTag, nfCoverZ, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    
    # Define reinforcing layers
    layer('straight', steelMatTag, numBarsInt, barAreaInt, -coreY, coreZ, coreY, coreZ)  # intermediate skin reinf. +z
    layer('straight', steelMatTag, numBarsInt, barAreaInt, -coreY, -coreZ, coreY, -coreZ)  # intermediate skin reinf. -z
    layer('straight', steelMatTag, numBarsTop, barAreaTop, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    layer('straight', steelMatTag, numBarsBot, barAreaBot, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement
    
    #preparing fiber section for plotting
    global fib_sec,matcolor
    fib_sec=[['section', 'Fiber', secTag, '-GJ', GJ],
             ['patch', 'quad',coreMatTag, nfCoreZ, nfCoreY, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ],
             ['patch', 'quad',coverMatTag, 2, nfCoverY, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ],
             ['patch', 'quad',coverMatTag, 2, nfCoverY, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ],
             ['patch', 'quad',coverMatTag, nfCoverZ, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ],
             ['patch', 'quad',coverMatTag, nfCoverZ, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ]]
    matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
    opsv.plot_fiber_section(fib_sec, matcolor=matcolor)