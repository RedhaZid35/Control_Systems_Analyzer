import control as ct
import numpy as np
from control import step_response, ss2tf, step_info
from matplotlib import pyplot as plt
from scipy.signal import TransferFunction

U = 25
I = 2.2
R = 1.91
Ke = 0.0603
Kc = 0.0603
L = 0.63e-3
Jr = 1e-4

C = ct.tf([1],[L, R], inputs='e', outputs='i')
P = ct.tf(Kc, [Jr, 0], inputs='w', outputs='theta')
disturbance = ct.summing_junction(['d', 'i'], 'w') # w = d+v

# interconnect everything based on signal names
sys = ct.interconnect([C, P, disturbance],inputs=['e', 'd'], outputs='theta')
sys = ct.feedback(sys[0, 0], Ke, sign=-1)
print(ss2tf(sys))
# sys = ct.rootlocus_pid_designer(sys,Kp0=1, Ki0=1000, plot=False)

T = np.linspace(0, 0.1, 1000)
t,y = step_response(sys,E=U, T=T)
# print(t,y)
# plt.plot(t,y)
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.title('Step response')
# plt.grid()
# plt.show()
# S = step_info(sys)


