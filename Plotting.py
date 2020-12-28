# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

def plot_background(h_c, h_q, angle_wall):
    
    fig = plt.figure()
    ax = fig.gca()
    if h_c > h_q:
        h_bg = h_c + 1 # Total background (wall) height
    else:
       h_bg = h_q + 1
    
    width_bg = math.tan(math.radians(angle_wall)) * h_bg + 1
    ax = plt.axes(ax, xlim=(0, width_bg), ylim=(0, h_bg))
    ax.set_aspect('equal', adjustable='box')
    plt.grid()

    # climber and quickdraw position
    pos_q = [math.tan(math.radians(angle_wall)) * h_q, h_q]
    pos_c = [math.tan(math.radians(angle_wall)) * h_c, h_c]
    ax.scatter(pos_q[0], pos_q[1]) 
    plot_c = ax.scatter(pos_c[0], pos_c[1]) 
    
    # wall
    end_w = [math.tan(math.radians(angle_wall)) * h_bg, h_bg]
    ax.plot([0, end_w[0]], [0, end_w[1]],'k')
    return fig, plot_c, width_bg, h_bg

    
   """ 
def animate(i, pos_c, plot_c, ax, width_bg, h_bg):
    #point_c = plt.plot(pos_c[0, i], pos_c[1, i],"k")
    #plot_c = plot_c[0]
    #plot_c.set_data(pos_c[0, i], pos_c[1, i])
    #point_c.set_xdata(pos_c[0, i])
    #point_c.set_ydata(pos_c[1, i])

    ax = plt.axes(ax, xlim=(0, width_bg), ylim=(0, h_bg))
    ax.set_aspect('equal', adjustable='box')
    plt.scatter(pos_c[0, i], pos_c[1, i], color="black") ## TODO: keine Ahnung, warum die andere, bessere Methode nicht funktioniner
    return plot_c

#anim = animation.FuncAnimation(fig, animate, init_func=plot_background(h_c, h_q, angle_wall))
"""