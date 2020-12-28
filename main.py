# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:42:11 2020

@author: Christian Faßbender

This script and its subfunctions aim to calculate the motion and most importantly
the resulting force for a climbing fall.

Simplifications:
    - climber modelled as point mass
    - rope attachement point = COG of climber
    - no rope drag
    - simplified rope length calculation
    - rope considered as 1D linear elastic
    - quickdraw & carabiner modelled as singular attachment point (infinite stiffness)
    - static belay (for now) --> belay attachment modelled as fix point
    - simulation stops when contact to the wall is detected and outputs the present velocity
    
Input parameters:
    - heigt of highest quickdraw
    - height of climber
    - mass of climber
    - angle of wall to the vertical plane
    - Stiffness modulus of rope (Young's modulus * crossectional area)
    - rope slack (additionall length)                                 
                                 
Output:
    - force at quickdraw over time
    - animation
"""
## Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Plotting import plot_background
from Plotting import animate
import math



plt.close('all')
## Input parameters
m = 60  # kg
h_c = 3.5 # m
h_q = 2.5
angle_wall = 30  # deg
slack = 1  # m, must be >0
modulus_rope = 25000 # N, equal to young time s crossectional area

## Constants
g = -9.81
t_end = 3  # s
t_step = 0.001  # s
t = np.arange(0, t_end, t_step)
pos_c = np.zeros((2, len(t)))
vel_c = np.zeros_like(pos_c)
acc_c = np.zeros_like(pos_c)
acc_c[:, 0] = [0, g]


## Plot Background


## Initialize
pos_c[:, 0] = np.array([math.tan(math.radians(angle_wall)) * h_c, h_c])
pos_q =np.array([math.tan(math.radians(angle_wall)) * h_q, h_q])
length_qc = np.linalg.norm(pos_c[:, 0] - pos_q) # rope leength between climber and quickdraw at start
lr_0 = np.linalg.norm(pos_q) + length_qc + slack  # length of rope, other end is fixed at origin
lr = np.ones_like(t) * lr_0
strain = np.zeros_like(t)
F_r = np.zeros_like(t)
F_r_vec = np.zeros((2, len(t)))  # on attachment point of climber
F_q_vec = np.zeros_like(F_r_vec)

def check_freefall(pos_c, pos_q, slack, length_qc):
    """ At first the climber falls in a straigth line until he reaches the same distance
    as at his starting point form the quickdraw (but now below it).
    Additionally, if there is slack, the climber can fall freely for this distance 
    as well
    Returns True if climber is in free fall state, false otherwise
    """
    distance_qc = np.linalg.norm(pos_c - pos_q)
    if distance_qc < length_qc + slack:
        return True
    else:
        return False
    
    
def check_impact(pos_c, pos_q, t, i):  # pos_C on the left of wall...
    # does not work for straigt walls!
    
    # calculate slope form of wall
    # y = mx +b, where b =0 since it starts at the origin
    slope = pos_q[1] / pos_q[0]
    
    """slope = np.arctan(math.radians(90-angle_wall))
    print(slope)"""
    # test line point and actual point at same x location
    # if actual is above --> point is on the left and vice versa
    """y_line = slope * pos_c[0]
    res = y_line - pos_c[1] 
    print("yline: " + str(y_line) + " pos_c[1]: "  + str(pos_c[1]) + " .")
    if res < 0:
        return True
    else:
        return False
    """
    #print(slope)
    x_line = pos_c[1] / slope # for the given height
    #print(str(t[i]) + " xline: " + str(x_line) + " pos_c[0]: "  + str(pos_c[0]) + " .")
    if x_line > pos_c[0]:
        return True
    else:
        return False

## Main loop
tmp = 0
for i in range(len(t)-1):
    if  check_freefall(pos_c[:, i], pos_q, slack, length_qc):
        # Simple explicit Euler scheme for freefall phase
        acc_c[:, i+1] = [0, g]
        vel_c[:, i+1] = vel_c[:, i] + acc_c[:, i+1] * t_step
        pos_c[:, i+1] = pos_c[:, i] + vel_c[:, i] * t_step  # i+1 for velocity works as well
        lr[i+1] = lr_0
    else:
        if tmp == 0:  # announcement
            print("Freefall phase finished after " + str(t[i]) + "s.")
            print("The climber is now at height " + str(pos_c[1, i]) + ".")
            tmp += 1
       
        # force equilibrium if rope gets stretched and excerts force
        # calculate rope length
        lr[i] = np.linalg.norm(pos_q) + np.linalg.norm(pos_c[:, i] - pos_q)
        strain[i] = np.log(lr[i] / lr_0)
        F_r[i] = strain[i] * modulus_rope
        # vectorial force at climber, multiply scalar force by direction to quickdraw
        direction = pos_q - pos_c[:, i]
        direction = direction / np.linalg.norm(direction)
        F_r_vec[:, i] = direction * F_r[i]
        acc_c[:, i+1] = [0, g] + F_r_vec[:, i] / m
        vel_c[:, i+1] = vel_c[:, i] + acc_c[:, i+1] * t_step
        pos_c[:, i+1] = pos_c[:, i] + vel_c[:, i+1] * t_step
        
        # calculate resulting force on quickdraw
        # summs forces from q to origin and force from to q to c
        F_left =  F_r[i] * pos_q / np.linalg.norm(pos_q)
        F_right = - F_r[i] * direction
        F_q_vec[:, i] = - (F_left + F_right)
        
    if pos_c[1, i+1] < 0:
        print("Attention ground fall with velocity " + str(vel_c[1,i+1]) + "m/s.")
        break
    # stop when climber's cure would interset wall and give out impack velocity
    if  check_impact(pos_c[:, i+1], pos_q, t, i):
        impact_vel = np.linalg.norm(vel_c[:, i+1])
        print("The climber has impacted the wall @ " + str(t[i]) + "s with a velocity of " + str(impact_vel) + "m/s.")
        break
    
        
         
        
print("Time integration finished.")

#anim = animation.FuncAnimation(fig, animate,  fargs=(pos_c, plot_c, ax, width_bg, h_bg))    
#+plt.show()
## Ppostprocessing
fig, plot_c, width_bg, h_bg = plot_background(h_c, h_q, angle_wall)
ax = fig.gca()
plt.plot(pos_c[0,0:i], pos_c[1,0:i])

fig2 = plt.figure(2)
ax2 = fig2.gca()
ax2.plot(t[0:i], F_r[0:i])

fig3 = plt.figure(3)
ax3 = fig3.gca()
ax3.plot(t[0:i], F_q_vec[0, 0:i])    
ax3.plot(t[0:i], F_q_vec[1, 0:i])   
ax3.plot(t[0:i], np.linalg.norm(F_q_vec[:, 0:i], axis=0))
plt.grid()
ax3.legend(["x Force", "y Force", "total Force"])
 


    