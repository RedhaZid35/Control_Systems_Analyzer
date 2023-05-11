import control as ct
import numpy as np
from control import step_response, ss2tf, step_info, forced_response
from matplotlib import pyplot as plt
from scipy.signal import TransferFunction
import datetime as dt
import matplotlib.animation as animation
import time 
# import tmp102

sys = ct.tf([1], [1, 3, 20])
sys = ct.feedback(sys, sign=-1)
# print(sys)



# plt.plot(response.t,response.y[0])
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.title('Step response')
# plt.grid()
# plt.show()
# S = step_info(sys)



# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
# tmp102.init()

# This function is called periodically from FuncAnimation
# def animate(i, xs, ys):

#     # Read temperature (Celsius) from TMP102
#     temp_c = round(tmp102.read_temp(), 2)

#     # Add x and y to lists
#     xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
#     ys.append(temp_c)

#     # Limit x and y lists to 20 items
#     xs = xs[-20:]
#     ys = ys[-20:]

#     # Draw x and y lists
#     ax.clear()
#     ax.plot(xs, ys)

#     # Format plot
#     plt.xticks(rotation=45, ha='right')
#     plt.subplots_adjust(bottom=0.30)
#     plt.title('TMP102 Temperature over Time')
#     plt.ylabel('Temperature (deg C)')

T = []
def animate(i):
    U = np.ones_like(T)
    response = forced_response(sys,U=U, T=T)
    # print(response.t,response.y)
    T.append(T[-1]+0.01)


    # Draw x and y lists
    ax.clear()
    ax.grid()
    ax.plot(response.t,response.y[0])

    # Format plot
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)') 

# Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, interval=0.1)

# plt.show()



print(time.time())